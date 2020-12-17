#!/usr/bin/python2
# -*- coding: utf-8 -*-

import yaml
from telegramNotificaciones import TelegramNotificaciones
from logger import Logger
from datetime import datetime
from DAO import DAO
from contactosV2 import Contactos
from whatsappV2 import Whatsapp


config = yaml.safe_load(open('configuracion.yml'))

logger = Logger(config['logger'])
#telegram = TelegramNotificaciones(config['gubiaBoot'], logger)
#telegram.enviarMensaje("Hola Mundo Grupo desde YAML refactorizado actual " + str(datetime.now()) )
#logger.logInfo("Prueba")


#contactos = Contactos(config['peopleApi'], logger)
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

DAO = DAO(config['baseDatos'], logger)
mensajes = DAO.obtenerMensajes()

print len(mensajes)
print mensajes[0][0]

#resultado = DAO.eliminarMensajeEntrada(mensajes[0][0])

#print resultado

resultado = DAO.agregarWhatsCorrecto(mensajes[0])
print resultado

resultado = DAO.agregarMensajeNoEnviado(mensajes[0])
print resultado



