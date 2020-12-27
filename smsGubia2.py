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



erroresParaMantenimiento = 0


config = yaml.safe_load(open('configuracion.yml'))
logger = Logger(config['logger'])
maximoErrores = config['erroresParaMantenimiento']


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

            #obtiene mensajes a enviar
            mensajes = DAO.obtenerMensajes()

            logger.info("Mensajes a enviar por WhatsApp -> {}".format(len(mensajes)))


            for mensaje in mensajes:
                contactos.agregarContacto(mensaje[2])
                esperaWhatsApp()
                resultado = whatsApp.enviarWhats(mensaje)
                print(resultado)
                print(resultado["success"])

                   
            erroresParaMantenimiento = 0
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

    #resultado = contactos.agregarContacto("2223178965", "Andres")

    #resultados = contactos.listarContactos()
    #print resultados

    #for resultado in resultados:
    #    print resultado
    #    contactos.eliminarContacto(resultado)

    #resultados = contactos.listarContactos()
    #print resultados

    #whatsApp = Whatsapp(config['whatsApp'], logger)
    #whatsApp = Whatsapp()
    #resultado = whatsApp.enviarWhats("2223178965" , "Este mensaje es automatico desde el sms V2 pero eso no te quita lo puto, ni que los pumas esten en la final, voy ver el futbol mañana sigo")
    #print resultado

    #


    #print len(mensajes)

    #resultado = DAO.eliminarMensajeEntrada(mensajes[0])

    #mensajes = DAO.obtenerMensajesNoEnviados()

    #resultado = DAO.actualizarIntento(mensajes[1])

    #resultado = DAO.eliminarMensajeNoEnviado(mensajes[0])

    #print resultado

    #resultado = DAO.eliminarMensajeEntrada(mensajes[0][0])

    #print resultado

    #resultado = DAO.agregarWhatsCorrecto(mensajes[0])
    #print resultado

    #resultado = DAO.agregarMensajeNoEnviado(mensajes[0])
    #print resultado





