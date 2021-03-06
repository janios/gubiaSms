#!/usr/bin/python2
# -*- coding: utf-8 -*-

import urllib 
import urllib2 
import csv
from formateaWhats import FormateaWhatsapp
import sys

uid = "527971416893"

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

	def enviarWhats(self,numero,texto):
		result = ""
		try:
			print(numero)
			if (len(numero)==10):
				numero = "521" + numero
				print(numero)
			else:
				return "Eror numero incorrecto"

			print(numero)
			formato = FormateaWhatsapp()

			if "prueba" in texto:
				texto2 = formato.mensajePrueba(texto)
			elif "Hola" in texto:
				texto2 = formato.mensajePacientes(texto)
			elif "paciente" in texto:
				texto2  = formato.mensajeMedicos(texto)
			else:
				texto2 = formato.mensajePromo(texto) 

			print(texto2)

			claveUnica = "mens-"+ str(self	.escribirincrementar())
			token = str(self.escribirincrementar(modo = 1))
			#print(token)
			data = urllib.urlencode({"token":token,"uid":uid,"to":numero,"custom_uid":claveUnica,"text":texto2}) 
			req = urllib2.Request('https://www.waboxapp.com/api/send/chat', data) 
			response = urllib2.urlopen(req) 
			result = response.read()
			print("Mensaje a numero {} enviado".format(numero))
		except:
			result = "Error " + sys.exc_info()
			print(result)
		finally:
			print(result)
			return result
