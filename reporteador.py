#!/usr/bin/python2
# -*- coding: utf-8 -*-
import mysql.connector
import csv
import openpyxl
import sys
import pdb


config_mysql = {
		'user': 'root',
		'password': 'gubia',
		'host': 'localhost',
		'database': 'smsGubia',
	}

class Reporteador():
	# conectamos al servidor MySql
	def force_text(self, text):
		if (isinstance(text, unicode)):
			return text.encode("utf-8")
		return str(text)

	def ejecutarbd(self, query):
		try:	
			#db = MySQLdb.connect("localhost", "root", "gubia", "smsGubia")
			db = mysql.connector.connect(**config_mysql)
			# cursor, clase para el manejo del SQL ???
			cursor = db.cursor()
			#Ejecutamos la consula SQL
			cursor.execute(query)
			# Cerramos cursor
			res = cursor.fetchall()
			cursor.close()
			# Cerramos la conexion
			db.close()
			print("lectura en base de datos correcta")
			return res
		except:
			return "Error"

	def llenarArchivo(self,resultado,doc,modo):
		#selecciona el archivo de Excel
		
		archivos = ['Detalle', 'Mes','Dia', 'Hora', 'Ciclos']
		if (modo != 0):
			hoja = doc[archivos[modo-1]]
		else:
			hoja = doc[archivos[0]]
		letras= ['A','B','C','D','E','F','G', 'H','I','J']
		meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
		largo= len(resultado[0])
		contador = 0;
		#modo 1 encabezados de Detalle mensajes
		for registro in resultado:
			valor = 1
			for reg in range(0,largo):
				celda = letras[reg]+str(contador+2)
				if (modo== 0 or modo == 1 or modo == 5):
					if (reg ==0):
						hoja[celda] = contador + 1
					else:
						hoja[celda] = registro[valor-1]
				else: 
					if(reg== 0):
						hoja[celda] = contador + 1
						celda = letras[reg+1]+str(contador+2)
						dato = self.force_text(registro[valor-1])
						recortado = dato[0:2]
						hoja[celda] = dato[0:4]
						celda = letras[reg+2]+str(contador+2)
						hoja[celda] = meses[int(dato[6:7])-1]
						if (modo ==3 or modo ==4):
							celda = letras[reg+3]+str(contador+2)
							hoja[celda] = dato[8:11]
						if (modo==4):
							celda = letras[reg+4]+str(contador+2)
							hoja[celda] = dato[11:]
					else:
						if (modo == 2):
							reg+=1
						elif (modo == 3):
							reg+=2
						else:
							reg+=3
						celda = letras[reg+1]+str(contador+2)
						hoja[celda] = registro[valor-1]
						
				
				valor+=1
			contador +=1
		doc.save("reporte.xlsx")
		
		#print("entro modo {}".format(modo))
		

	def escribirArchivo(self, archivo, contenido): 
		detalle = open(archivo,'w')
		detalle.write(contenido)			
		detalle.close()

	def reporteDetalleMensajes(self, query = None):
		try:
			doc = openpyxl.load_workbook('reportesBase.xlsx')
			modo = 0
			if (query == None):
				query = ["SELECT * FROM detalleMensajes WHERE remitente != 'escamilla.cristian@gmail.com'",
						 "SELECT DISTINCT SUBSTRING(fecha,1,7), COUNT(SUBSTRING(fecha,1,7)) FROM detalleMensajes GROUP BY (SUBSTRING(fecha,1,7))",
						 "SELECT DISTINCT fecha , COUNT(fecha)  FROM detalleMensajes GROUP BY (fecha)",
						 "SELECT DISTINCT SUBSTRING(CONCAT(fecha, ' ' ,horaIntento),1,13), COUNT(SUBSTRING(CONCAT(fecha, ' ' ,horaIntento),1,13)) FROM detalleMensajes GROUP BY SUBSTRING(CONCAT(fecha, ' ' ,horaIntento),1,13)",
						 "SELECT * FROM registroTotal"] 					 
				modo = 1
			
			if (modo == 0):
				resultado = self.ejecutarbd(query)
				if resultado != "Error":
					doc = openpyxl.load_workbook('reportesBaseUnico.xlsx')
					#modo 1 encabezados de Detalle mensajes modo 2 Registro Total
					contenido = self.llenarArchivo(resultado,doc,0)
					#self.escribirArchivo('reporteDetalleMensajes.csv', contenido)
						#print("{},{},{},{},{}".format(contador,registro[1],registro[2],registro[3],registro[4]))#,registro[5],registro[6]))
				else:
					resultado = "Error instruccion sql incorrecta, la tabla se llama 'detalleMensajes' y los campos 'id','fecha','remitente','numero','mensaje','horaIntento','enviado'" 
					print(resultado)
				return resultado
			else:
				for iterador in range(1,6):
					#print("EL ciclo es {}".format(iterador))
					#print(query[iterador-1])
					#print(modo) 
					resultado = self.ejecutarbd(query[iterador-1])
					contenido = self.llenarArchivo(resultado,doc,iterador)
					#print("salido del ciclo iterador {}".format(iterador))
		except:
			print("Se genero un error durante la ejecución de los reportes {}".format(sys.exc_info()) )
		finally:
			doc.close()
		return resultado

	def reporteRegistroTotal(self):
		query = "SELECT * FROM registroTotal" 
		resultado = self.ejecutarbd(query)
		#modo 1 encabezados de Detalle mensajes modo 2 Registro Total
		#contenido = self.llenarArchivo(resultado,2)
		#self.escribirArchivo('reporteRegistroTotal.csv', contenido)
			#print("{},{},{},{},{}".format(contador,registro[1],registro[2],registro[3],registro[4]))#,registro[5],registro[6]))
		return resultado

	def escribirSmsSalida(self, id , fecha, numero, mensaje, enviado):
		query = "INSERT INTO smsSalida(id, fecha, numero, mensaje, enviado) VALUES ('{}','{}','{}','{}','{}')".format(id, fecha, numero, mensaje, enviado)
		try:	
			#db = MySQLdb.connect("localhost", "root", "gubia", "smsGubia")
			db = mysql.connector.connect(**config_mysql)
			# cursor, clase para el manejo del SQL ???
			cursor = db.cursor()
			#Ejecutamos la consula SQL
			cursor.execute(query)
			# Cerramos cursor
			db.commit()
			cursor.close()
			# Cerramos la conexion
			db.close()
			print("Escritura en base de datos correcta")
			return res
		except:
			return "Error"
