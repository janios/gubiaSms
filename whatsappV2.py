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
        
        print archivoContador
        incrementa = 0
        archivo = open(archivoContador,'r+')
        incrementa = int(archivo.read()) +1
        archivo.seek(0)
        archivo.write(str(incrementa))
        logger.info("Mensaje de WhatsApp # {}".format(incrementa))
        return incrementa

    def enviarWhats(self,numero,texto):
        global logger
        global token
        global diferenciador
        global uid

        result = ""
        try:
            print(numero)
            if (len(numero)==10):
                numero = "521" + numero
                logger.info("Se enviara mensaje a {}".format(numero))
            else:
                logger.error("Eror numero incorrecto {}".format(numero))
                return "Eror numero incorrecto"

            print(numero)
            claveUnica = diferenciador+ str(self.escribirincrementar())
            data = urllib.urlencode({"token":token,"uid":uid,"to":numero,"custom_uid":claveUnica,"text":texto}) 
            print(data)
            req = urllib2.Request('https://www.waboxapp.com/api/send/chat', data) 
            response = urllib2.urlopen(req) 
            result = response.read()
            logger.info("Mensaje a numero {} enviado".format(numero))
        except:
            result = "Error " + sys.exc_info()
            logger.error(result)
        finally:
            print(result)
            logger.info("Resultado del envio {}".format(result))
            return result
