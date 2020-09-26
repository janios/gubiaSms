#!/usr/bin/python2
# -*- coding: utf-8 -*-

import gammu
import mysql.connector
import sys


config_mysql = {
	'user': 'root',
	'password': 'gubia',
	'host': 'localhost',
	'database': 'smsGubia',
}

class RecibirMensajes():

	def force_to_unicode(text):
	   #"If text is unicode, it is returned as is. If it's str, convert it to Unicode using UTF-8 encoding"
	    return text if isinstance(text, unicode) else text.decode('utf8')


	def ejecutarbd(self, query):
		#print(query)
		# conectamos al servidor MySql
		conector = mysql.connector.connect(**config_mysql)
		# cursor, clase para el manejo del SQL ???
		cursor = conector.cursor()
		# Ejecutamos la consula SQL
		cursor.execute(query)
		conector.commit()
		# Cerramos cursor
		cursor.close()
		# Cerramos la conexion
		conector.close()
		print("Escritura en base de datos correcta")

	def recibir(self):
		contador = 0
		try:
		    sm = gammu.StateMachine()
		    sm.ReadConfig()
		    sm.Init()
		    status = sm.GetSMSStatus()
		    remain = status['SIMUsed'] + status['PhoneUsed'] + status['TemplatesUsed']
		    destino = 0
		    if remain >0:
		    	print("Hay {} mensajes por recibir".format(remain))
		        for numero in range(0,remain):
		            sms = sm.GetNextSMS(Start=True, Folder=0)
		            telefono = sms[0]['Number']
		            print(telefono)
		            texto = sms[0]['Text']
		            print(texto)
		            telefono = telefono.encode("utf-8")
		            texto = texto.encode("utf-8") 
		            print("Mensaje en la fecha {}, del numero {} con texto{} y el id {} ".format(sms[0]['DateTime'],telefono,texto,sms[0]['Location']))
		            query = "INSERT INTO `recibidos`(`fecha`, `telefono`, `texto`, `destino`) VALUES ('{}','{}','{}',{})".format(sms[0]['DateTime'],telefono,texto,destino)   
		            #print(query)
		            self.ejecutarbd(query)
		            idMensaje = sms[0]['Location']
		            sm.DeleteSMS(Location=idMensaje, Folder=0)
		            contador += 1
		    else:
		    	print("No hay mensajes en el telefono")		            
		except:
		    print("Error en la recepcion de mensajes" , sys.exc_info())

		finally:
		    sm.Terminate()
		    return contador