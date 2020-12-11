#!/usr/bin/python2
# -*- coding: utf-8 -*-

import json 
import requests

url = ""
chatId  = 0
logger = ""

class TelegramNotificaciones():

    
    def __init__(self, config, loggerExterno):
        global url
        global chatId
        global logger
        logger = loggerExterno
        chatId = config['chatIdGrupo']
        url = "https://api.telegram.org/bot{}/".format(config['token'])
    
    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content
      
    def enviarMensaje(self,mensaje):
        global url
        global logger
        ruta = url + "sendMessage?text={}&chat_id={}".format(mensaje, chatId)
        logger.logInfo("Mensaje enviado a " + ruta)
        self.get_url(ruta)
