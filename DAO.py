#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pymssql
import traceback

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
        global numeroRegistros
        global conn
      
        logger = loggerEntrada
        host = config['host']
        username = config['username']
        password = config['password']
        database = config['database']
        tablaEntrada = config['tablaEntrada']
        tablaWhatsAppCorrecto = config['whatsAppSalida']
        tablaNoEnviados = config['tablaNoEnviados']
        numeroRegistros = config['numeroRegistros']
        try:
            conn = pymssql.connect(host, username, password, database)
            logger.info("Base de Datos conectada")
        except:
            error = traceback.format_exc()
            logger.logError("Error en la base de datos {}".format(error))
        

    def obtenerMensajes(self):
        global logger
        global conn

        try:
            cursor = conn.cursor()  
            registros= []
            consulta = "Select TOP("+str(numeroRegistros)+") * from " + tablaEntrada + " order by id"  
            logger.logInfo(consulta)
            cursor.execute(consulta)
            for row in cursor.fetchall():
                lista= []
                for col in row:
                    lista.append(col)
                registros.append(lista)
            logger.logInfo("Registros obtenidos ->" + str(len(lista)))
            return registros
        except:
            error = traceback.format_exc()
            logger.logError("Error en la base de datos {}".format(error))
            return "Error"

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
            return "ERROR"
    
    def desconectar(self):
        global conn
        global logger
        logger.info("Coneccion cerrada")
        conn.close()
    
    def eliminarMensajeEntrada(self, id):
        global tablaEntrada
        return self.eliminar(tablaEntrada, id)
    
    def agregarWhatsCorrecto(self, mensaje):
        global tablaWhatsAppCorrecto
        global logger
        global conn

        try:
            cursor = conn.cursor()
            query = "INSERT INTO {} (telefono, mensaje, fecha, Sucursal) values ('{}', '{}', '{}', {})".format(tablaWhatsAppCorrecto, mensaje[2], mensaje[3],mensaje[1],mensaje[5])
            logger.info(query)
            cursor.execute(query)
            conn.commit()
            logger.info("registro agregado a tabla {}".format(tablaWhatsAppCorrecto))
            return "Registro Agregado"
        except:
            error = traceback.format_exc()
            logger.logError("Error {} en la eliminacion de la tabla {} ".format(error, tablaWhatsAppCorrecto))
            return "ERROR"   

