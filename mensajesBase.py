#!/usr/bin/python2
# -*- coding: utf-8 -*-

import pymssql
import traceback

host = "sql5007.site4now.net"
username = "DB_9AE2E9_bdGubia_admin"
password = "gubia123..."
database = "DB_9AE2E9_bdGubia"

class MensajesBase():

	def consulta(self):
		global host
		global username
		global password
		global database
		try:
			conn = pymssql.connect(host, username, password, database)
			cursor = conn.cursor()
			print("Base conectada")
			registros= []
			cursor.execute("Select * from tbSmsSalida")
			for row in cursor.fetchall():
			    lista= []
			    for col in row:
			    	#print(col)
			    	lista.append(col)
			    registros.append(lista)
			conn.close()
			 
			return registros

		except:
			
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
