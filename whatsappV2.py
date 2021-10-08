#!/usr/bin/python2
# -*- coding: utf-8 -*-

import urllib 
import urllib2 
import sys

uid = ""
logger = ""
token = ""
archivoContador = ""
diferenciador = ""

class Whatsapp():

    def __init__(self, config, loggerEntrada):
        global token
        global archivoContador
        global diferenciador
        global uid
        global logger

        logger = loggerEntrada
        token = config['token']
        archivoContador = config['archivoContador']
        diferenciador = config['diferenciador']
        uid = config['uid']
        logger.info("WhatsApp iniciado")

    def escribirincrementar(self):
        global logger
        global archivoContador
        incrementa = 0
        archivo = open(archivoContador,'r+')
        incrementa = int(archivo.read()) +1
        archivo.seek(0)
        archivo.write(str(incrementa))
        logger.info("Mensaje de WhatsApp # {}".format(incrementa))
        return incrementa
    
    def force_text(self, text):
        if (isinstance(text, unicode)):
            return text.encode("utf-8")
        return str(text)

    def enviar(self,numero,texto):
        global logger
        global token
        global diferenciador
        global uid

        result = ""
        try:
            logger.info("Telefono recibido {}".format(numero))
            if (len(numero)==10):
                numero = "521" + numero
                logger.info("Se enviara mensaje a {}".format(numero))
            else:
                logger.error("Eror numero incorrecto {}".format(numero))
                return "Eror numero incorrecto"

            claveUnica = diferenciador+ str(self.escribirincrementar())
            mensaje = self.force_text(texto)
            mensaje = mensaje.replace("!n", "\n")
            data = urllib.urlencode({"token":token,"uid":uid,"to":numero,"custom_uid":claveUnica,"text":mensaje}) 
            logger.info("Datos enviados al servicio {}".format(data))
            req = urllib2.Request('https://www.waboxapp.com/api/send/chat', data) 
            response = urllib2.urlopen(req) 
            result = response.read()
            logger.info("Mensaje a numero {} enviado".format(numero))
            return result
        except Exception as e:
            result = "Error en WhatsApp {} ".format(e.read())
            logger.error(result)
            raise ValueError(result)

    def enviarWhats(self,mensaje):
        return self.enviar(mensaje[2],mensaje[3])