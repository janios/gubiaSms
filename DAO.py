#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pymssql
import traceback

logger = ""
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
        global numeroRegistros
        logger = loggerEntrada
        host = config['host']
        username = config['username']
        password = config['password']
        database = config['database']
        tablaEntrada = config['tablaEntrada']
        numeroRegistros = config['numeroRegistros']
        print("LOCO LOCO")
        print(host)

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
            consulta = "Select TOP("+str(numeroRegistros)+") * from " + tablaEntrada + " order by id"  
            logger.logInfo(consulta)
            cursor.execute(consulta)
            for row in cursor.fetchall():
                lista= []
                for col in row:
                    lista.append(col)
                registros.append(lista)
            conn.close()
            logger.logInfo("Registros obtenidos ->" + str(len(lista)))
            return registros
        except:
            error = traceback.format_exc()
            logger.logError("Error en la base de datos")
            logger.logError(error)
            return "Error"

