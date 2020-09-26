#!/usr/bin/python2
# -*- coding: utf-8 -*-

import urllib 
import urllib2 
import csv
import sys

uid = "5217971111248"

class Whatsapp:

	def escribirincrementar(self, modo = 0):
		incrementa = 0;
		if modo == 0:
			archivo = open('whats.log','r+')
			incrementa = int(archivo.read()) +1
			archivo.seek(0)
			archivo.write(str(incrementa))
		else:
			archivo = open('token.log','r')
			incrementa = archivo.read()
		archivo.close()
		return incrementa

	def enviarWhats(self,numero):
		result = ""
		try:
			print(numero)
			if (len(numero)==10):
				numero = "521" + numero
				print(numero)
			else:
				return "Eror numero incorrecto"

			print(numero)
			
			url = 'http://sistemagubia.gubia.mx/imagenes/img10.jpeg'
			caption = "Gubia agradece su preferencia"
			description = "! Vigilando Tu Salud ¡ " 
			claveUnica = "mens-"+ str(self	.escribirincrementar())
			token = str(self.escribirincrementar(modo = 1))
			#print(token)
			data = urllib.urlencode({"token":token,"uid":uid,"to":numero,"custom_uid":claveUnica,"url":url,"caption":caption,"description":description}) 
			req = urllib2.Request('https://www.waboxapp.com/api/send/image', data) 
			response = urllib2.urlopen(req) 
			result = response.read()
			print("El resultado es : " + result)
			print("Mensaje a numero {} enviado".format(numero))
		except:
			result = "Error " + sys.exc_info()
			print(result)
		finally:
			print(result)
			return result
