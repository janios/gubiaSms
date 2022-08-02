
#!/usr/bin/python2
# -*- coding: utf-8 -*-

import logging
from datetime import datetime


logger = logging.getLogger('logger_gubia')

class Logger():

    def __init__(self, config):
        global logger    
        logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(config['archivo'])
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)

     #Elimina codigo unicode
    def force_text(self, text):
        if (isinstance(text, unicode)):
            return text.encode("utf-8")
        return str(text)

    def formatText(self, text):
        mensaje = self.force_text(text)
        return str(datetime.now()) + " - " + mensaje

    def logInfo(self, text):
        global logger
        logger.info(self.formatText(text))
    
    def info(self, text):
        self.logInfo(text)
    
    def logError(self, text):
        global logger
        logger.error(self.formatText(text))
    
    def error(self,text):
        self.logError(text)        
    
    def logWarning(self, text):
        global logger
        logger.warning(self.formatText(text))