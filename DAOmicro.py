#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pymssql
import traceback

host = ""
username = ""
password = ""
database = ""
tablaEntrada = ""
logger = ""
numeroRegistros = ''

class DAOmicro():

    def __init__(self, config, loggerEntrada):
        global logger
        global host
        global username
        global password
        global database
        global tablaEntrada
        global numeroRegistros
        logger = loggerEntrada
        host = config['host']
        username = config['username']
        password = config['password']
        database = config['database']
        tablaEntrada = config['tablaEntrada']
        numeroRegistros = config['numeroRegistros']

	def consulta(self):
		global logger
        global host
        global username
        global password
        global database
        global numeroRegistros
        try:
            conn = pymssql.connect(host, username, password, database)
            cursor = conn.cursor()  
            logger.logInfo("Base conectada")
            registros= []
            consulta = "Select TOP("+numeroRegistros+") * from " + tablaEntrada  
            logger.logInfo(consulta)
            cursor.execute(consulta)
            for row in cursor.fetchall():
                lista= []
                for col in row:
                    lista.append(col)
                registros.append(lista)
            conn.close()
            logger.logInfo("Registros obtenidos ->" + registros.lenght)
            return registros
        except:
            error = traceback.format_exc()
            logger.logError("Error en la base de datos")
            logger.logError(error)
            return "Error"

    def eliminacion(self, id):
		
		global host
		global username
		global password
		global database
		try:
			conn = pymssql.connect(host, username, password, database)
			cursor = conn.cursor()		

			query = "DELETE FROM tbSmsSalida WHERE id = '{}'".format(id) 
			#print(query)
			#cursor.execute("INSERT INTO tbSmsSalida  (fecha, numero, mensaje) VALUES ('2018-08-10','5554374058','PRUEBA DESDE SERVIDOR GUBIA X');")
			cursor.execute(query)
			conn.commit()

			conn.close()
			return "OK"
		except:
			return "Error"
	
    def agregar(self, fecha, numero, mensaje):
		global host
		global username
		global password
		global database
		try:
			
			conn = pymssql.connect(host, username, password, database)
			cursor = conn.cursor()		

			query = "INSERT INTO tbSmsSalida (fecha, numero, mensaje) values ('{}', '{}', '{}')".format(fecha,numero,mensaje) 
			print(query)
			
			cursor.execute(query)
			conn.commit()

			conn.close()
			return "OK"
		except:
			error = traceback.format_exc()
			print(error)
			return "Error"
