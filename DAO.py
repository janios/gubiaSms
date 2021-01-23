#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pymssql
import traceback
from datetime import datetime

host = ""
username = ""
password = ""
database = ""
tablaEntrada = ""

numeroRegistros = ""

class DAO():

    def __init__(self, config, loggerEntrada):
        global logger
        global host
        global username
        global password
        global database
        global tablaEntrada
        global tablaWhatsAppCorrecto
        global tablaNoEnviados
        global tablaMantenimiento
        global tablaErrores
        global numeroRegistros
        global numeroReintentos
        global conn
      
        logger = loggerEntrada
        host = config['host']
        username = config['username']
        password = config['password']
        database = config['database']
        tablaEntrada = config['tablaEntrada']
        tablaWhatsAppCorrecto = config['whatsAppSalida']
        tablaNoEnviados = config['tablaNoEnviados']
        tablaMantenimiento = config['tablaMantenimiento']
        tablaErrores = config['tablaErrores']
        numeroRegistros = config['numeroRegistros']
        numeroReintentos = config['numeroReintentos']
        try:
            conn = pymssql.connect(host, username, password, database)
            logger.info("Base de Datos conectada")
        except:
            error = traceback.format_exc()
            logger.logError("Error en la base de datos {}".format(error))
            raise ValueError("Error en la base de datos {}".format(error))
  
    def obtener(self, query, tabla):
        global logger
        global conn
        try:
            cursor = conn.cursor()  
            registros= []
            logger.logInfo(query)
            cursor.execute(query)
            for row in cursor.fetchall():
                lista= []
                for col in row:
                    lista.append(col)
                registros.append(lista)
            return registros
        except:
            error = traceback.format_exc()
            logger.logError("Error en la base de datos {}".format(error))
            raise ValueError("Error en la base de datos {}".format(error)) 

    def eliminar(self, tabla, id):
        global conn
        global logger
        try:
            cursor = conn.cursor()
            query = "DELETE FROM {} WHERE id = '{}'".format(tabla, id)
            logger.info("Ejecutando query -> {}".format(query))
            cursor.execute(query)
            conn.commit()
            logger.info("Registro {} eliminado".format(id))
            return "Registro {} eliminado".format(id)
        except:
            error = traceback.format_exc()
            logger.logError("Error {} en la eliminacion de la tabla {} con el id {}".format(error, tabla, id))
            raise ValueError("Error {} en la eliminacion de la tabla {} con el id {}".format(error, tabla, id))
    
    def agregar(self, query, tabla):
        global logger
        global conn
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            logger.info("registro agregado a tabla {}".format(tabla))
            return "Registro Agregado"
        except:
            error = traceback.format_exc()
            logger.logError("Error {} agregando archivo de la tabla {} ".format(error, tabla))
            raise ValueError("Error {} agregando archivo de la tabla {} ".format(error, tabla))  
    
    def eliminarSaltoDeLinea(self, texto):
        texto = texto.replace("\n","!n")
        return texto
    
    def force_text(self, text):
        if (isinstance(text, unicode)):
            return text.encode("utf-8")
        return str(text)

    def actualizar(self, query, tabla):
        global logger
        global conn

        try:
            logger.info(query)
            cursor = conn.cursor()
            cursor.execute(query)
            conn.commit()
            logger.info("registro actualizado en la tabla {}".format(tabla))
            return "Registro Actualizado"
        except:
            error = traceback.format_exc()
            logger.logError("Error {} actulizando archivo de la tabla {} ".format(error, tabla))
            raise ValueError("Error {} actulizando archivo de la tabla {} ".format(error, tabla))  

    def desconectar(self):
        global conn
        global logger
        logger.info("Coneccion cerrada")
        conn.close()
    
    def eliminarMensajeEntrada(self, mensajes):
        global tablaEntrada
        return self.eliminar(tablaEntrada, mensajes[0])
    
    def eliminarMensajeNoEnviado(self, mensajes):
        global tablaNoEnviados
        return self.eliminar(tablaNoEnviados, mensajes[0]) 
   
    def agregarWhatsCorrecto(self, mensaje):
        global tablaWhatsAppCorrecto
        global logger
        formateado = self.force_text(mensaje[3])
        formateado = self.eliminarSaltoDeLinea(formateado)
        query = "INSERT INTO {} (telefono, mensaje, fecha, Sucursal, fechaEnvio) values ('{}', '{}', '{}', {}, '{}')".format(tablaWhatsAppCorrecto, mensaje[2], formateado,mensaje[1],mensaje[5],str(datetime.now())[:19] ) 
        logger.info(query)
        return self.agregar(query, tablaWhatsAppCorrecto)
    
    def agregarWhatsCorrectoNoEnviado(self, mensaje):
        global tablaWhatsAppCorrecto
        global logger
        formateado = self.force_text(mensaje[5])
        formateado = self.eliminarSaltoDeLinea(formateado)
        query = "INSERT INTO {} (telefono, mensaje, fecha, Sucursal, fechaEnvio) values ('{}', '{}', '{}', {}, '{}')".format(tablaWhatsAppCorrecto, mensaje[2], formateado,mensaje[1],mensaje[6],str(datetime.now())[:19] ) 
        logger.info(query)
        return self.agregar(query, tablaWhatsAppCorrecto)
    

    def agregarMensajeNoEnviado(self, mensaje):
        global tablaNoEnviados
        global logger
        formateado = self.force_text(mensaje[3])
        formateado = self.eliminarSaltoDeLinea(formateado)
        query = "INSERT INTO {} (telefono, mensaje, mensajeSms, fecha, Sucursal, intento, fechaIntento ) values ('{}', '{}', '{}', '{}', {}, 1, '{}')".format(tablaNoEnviados, mensaje[2], formateado,  mensaje[4],str(mensaje[1])[:19],mensaje[5], str(datetime.now())[:19] ) 
        logger.info(query)
        return self.agregar(query, tablaNoEnviados)

    def agregarMensajeError(self, mensaje):
        global tablaErrores
        global logger
        formateado = self.force_text(mensaje[3])
        formateado = self.eliminarSaltoDeLinea(formateado)
        query = "INSERT INTO {} (telefono, mensaje, mensajeSms, fecha, Sucursal, fechaIntento ) values ('{}', '{}', '{}', '{}', {}, '{}')".format(tablaErrores, mensaje[2], formateado,  mensaje[4],mensaje[1],str(mensaje[5])[:19], str(datetime.now())[:19]) 
        logger.info(query)
        return self.agregar(query, tablaNoEnviados)

    def actualizarIntento(self, mensaje):
        global tablaNoEnviados
        query = "UPDATE {} SET intento = {}, fechaIntento = '{}' WHERE id = {}".format(tablaNoEnviados, mensaje[4] + 1, str(datetime.now())[:19] ,mensaje[0])
        return self.actualizar(query, tablaNoEnviados)

    def obtenerMensajes(self):
        global tablaEntrada
        query = "Select TOP("+str(numeroRegistros)+") * from " + tablaEntrada + " order by id"
        return self.obtener(query, tablaEntrada)

    def obtenerMensajesNoEnviados(self):
        global tablaNoEnviados
        global numeroReintentos
        query = "Select TOP({}) * from {} where intento <={} order by id".format(str(numeroRegistros), tablaNoEnviados, numeroReintentos )
        return self.obtener(query, tablaNoEnviados)
    
    def obtenerMantenimiento(self):
        global tablaMantenimiento
        query = "Select TOP(1) * from {} order by id".format(tablaMantenimiento)
        mantenimiento = self.obtener(query, tablaMantenimiento)[0][1]
        logger.info("Periodo de mantenimiento -> {}".format(mantenimiento))
        return mantenimiento
    
    def ponerMantenimiento(self):
        global tablaMantenimiento
        query = "update {} SET Mantenimiento = 1 WHERE id = 1".format(tablaMantenimiento)
        return self.actualizar(query, tablaMantenimiento)