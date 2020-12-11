#!/usr/bin/python2
# -*- coding: utf-8 -*-

import yaml
from telegramNotificaciones import TelegramNotificaciones
from logger import Logger
from datetime import datetime
from DAO import DAO
from contactosV2 import Contactos

config = yaml.safe_load(open('configuracion.yml'))

logger = Logger(config['logger'])
telegram = TelegramNotificaciones(config['gubiaBoot'], logger)
#telegram.enviarMensaje("Hola Mundo Grupo desde YAML refactorizado actual " + str(datetime.now()) )
#logger.logInfo("Prueba")
#DAO = DAO(config['baseDatos'], logger)
#mensajes = DAO.consulta()

contactos = Contactos(config['peopleApi'], logger)
resultado = contactos.agregarContacto("5554374010", "Pedrito")

resultados = contactos.listarContactos()
print resultados

for resultado in resultados:
    print resultado
    contactos.eliminarContacto(resultado)

resultados = contactos.listarContactos()
print resultados
	

