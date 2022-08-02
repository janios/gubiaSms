#!/usr/bin/python2
# -*- coding: utf-8 -*-

import yaml
from telegramNotificaciones import TelegramNotificaciones
from logger import Logger
from datetime import datetime
from DAO import DAO
from contactosV2 import Contactos
from whatsappV2 import Whatsapp
import time
from random import randint


#iniciar instancias

def isMantenimiento():
    mantenimiento = DAO.obtenerMantenimiento()
    return mantenimiento

def esperaWhatsApp():
    espera = randint(config['esperaWhatsMenor'],config['esperaWhatsMayor'])
    logger.info("Espera de envio de WhatsApp de {}".format(espera))
    time.sleep(espera)

def enviarMensajeWhatsApp(mensaje):
    logger.info("Enviando mensaje {}".format(mensaje))
    contactos.agregarContacto(mensaje[2])
    esperaWhatsApp()
    resultado = whatsApp.enviarWhats(mensaje)
    logger.info("Resultado del envio de WhatsApp {}".format(resultado))
    return resultado

def enviarPrueba():
    logger.info("Enviado mensajes de prueba")
    for telefono in telefonosPrueba:
        logger.info("Enviado mensaje a {}".format(telefono))
        contactos.agregarContacto(telefono)
        esperaWhatsApp() 
        texto = mensajePrueba.format(datetime.now())
        texto = texto.replace("!n", "\n")
        resultado = whatsApp.enviar(telefono,texto)
        logger.info("Resultado del envio de WhatsApp {}".format(resultado))


erroresParaMantenimiento = 0
fechaPrueba = ''

config = yaml.safe_load(open('configuracion.yml'))
logger = Logger(config['logger'])
maximoErrores = config['erroresParaMantenimiento']
mensajePrueba = config['mensajePrueba']
telefonosPrueba = config['telefonosPrueba']
horaPrueba = config['horaPrueba']

try:

    telegram = TelegramNotificaciones(config['gubiaBoot'], logger)
    contactos = Contactos(config['peopleApi'], logger)
    DAO = DAO(config['baseDatos'], logger)
    whatsApp = Whatsapp(config['whatsApp'], logger)
     


    logger.info("Iniciado SMSGUBIA 2")
    telegram.enviarMensaje("Iniciando SMS GUBIA 2 en {}".format(datetime.now()))

    #CICLO INFINITO
    while True:

        try:
            #ValidaMantenimiento
            if (isMantenimiento() == "1"):
                logger.info("Se encuentra en periodo de Mantenimiento")
                telegram.enviarMensaje("SMS se encuenta en periodo de mantenimiento favor de validar")
                logger.info("Se realizara espera de mantenimiento de {} segundos".format(config['esperaMantenimiento']))
                time.sleep(config['esperaMantenimiento'])
                continue

            if fechaPrueba != str(datetime.now())[:10]:
                if int(str(datetime.now())[11:13])>=horaPrueba:
                    enviarPrueba()
                    fechaPrueba = str(datetime.now())[:10]    


            #obtiene mensajes a enviar
            mensajes = DAO.obtenerMensajes()

            logger.info("Mensajes a enviar por WhatsApp -> {}".format(len(mensajes)))

            #envio de mensajes 
            for mensaje in mensajes:
                resultado = enviarMensajeWhatsApp(mensaje)
                if "Eror numero incorrecto" in resultado:
                    DAO.agregarMensajeError(mensaje)
                    DAO.eliminarMensajeEntrada(mensaje)
                    continue
                
                if '"success":true' in resultado:
                    DAO.agregarWhatsCorrecto(mensaje)
                    DAO.eliminarMensajeEntrada(mensaje)
                    
                    continue
                else:
                    DAO.agregarMensajeNoEnviado(mensaje)
                    DAO.eliminarMensajeEntrada
                    
            erroresParaMantenimiento = 0
                                  
            
            mensajes = DAO.obtenerMensajesNoEnviados()

            for mensaje in mensajes:
                resultado = enviarMensajeWhatsApp(mensaje)

                if '"success":true' in resultado:
                    DAO.agregarWhatsCorrectoNoEnviado(mensaje)
                    DAO.eliminarMensajeNoEnviado(mensaje)
                    
                    continue
                else:
                    DAO.actualizarIntento(mensaje)



        except Exception as e:
            logger.error("Ocurrio un error {}".format(e))
            if (erroresParaMantenimiento == maximoErrores):
                telegram.enviarMensaje("Ocurrio error fatal  {}".format(e))
                telegram.enviarMensaje("Entrando a modo de mantenimiento")
                logger.error("Entrando en modo de mantenimiento")
                DAO.ponerMantenimiento()
            erroresParaMantenimiento =  erroresParaMantenimiento + 1

except Exception as e:
    logger.error("Ocurrio error {}".format(e))
    telegram.enviarMensaje("Ocurrio error fatal  {}".format(e))    

   





