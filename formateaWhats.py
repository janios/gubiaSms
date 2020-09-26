#!/usr/bin/python2
# -*- coding: utf-8 -*-

mensajeFin = " \n  \n*--Mensaje* *generado* *de* *manera* *automática* *favor* *de* *no* *contestar.* \n _--Si no puede acceder a sus resultados agregue este numero a sus contactos._"



class FormateaWhatsapp:
	global mensajeFin

	def mensajeMedicos(self, texto):
		dividido = texto.split(" ")
		unido = "*" + dividido[0].upper() + "* "
		largoNombre = len(dividido)-21 
		#print (len(dividido))
		#print(largoNombre)
		contador = 1 
		for palabra in dividido:
			#print(palabra)
			#print contador
			

			if palabra == "Gubia":
				continue
			
			if palabra == "ya":
				unido = unido + "  \n \n "	
			
			if palabra =="GUBIA.MX":
				unido = unido + "http://www."

			
			if "bit" in palabra:
				unido += " \n \n http://www."

			if "paciente" in palabra:
				palabra  = palabra + ": \n \n"

			if contador == 9:
				palabra = "*" + palabra

			if contador == (9 + largoNombre - 1):
				palabra = palabra + "*"
			#punto de antes o despues
			unido = unido + palabra
			

			unido = unido + " "
		
			contador += 1
		unido = unido + mensajeFin	#print(unido)
		return unido
	
	def mensajePacientes(self, texto):
		dividido = texto.split(" ")
		
		unido = ""
		tamano = len(dividido)
		#print(largoNombre)
		contador = 1 
		for palabra in dividido:
			
			if contador == 2:
				palabra = "*" + palabra + "*"
			
			if "aqu" in palabra:
				palabra  = palabra + ":  \n \n "	
			
						
			if "goo" in palabra:
				palabra  = " http://www." + palabra + " \n \n"

			if contador == 15:
				palabra = "*" + palabra
			
			if contador == tamano:
				palabra = palabra + ".*"

			unido = unido + palabra
			unido = unido + " "


			
			contador += 1
		unido = unido + mensajeFin	
		#print(unido)
		return unido


	def mensajePromo(self, texto):
		dividido = texto.split(" ")
		
		unido = ""
		tamano = len(dividido)
		#print(largoNombre)
		contador = 1 
		for palabra in dividido:
			
			if "-" in palabra:
				palabritas = palabra.split("-")
				palabra = palabritas[0] + ". " + " \n \n *" + palabritas[1]

			if contador == tamano:
				palabra = palabra + ".*"

			unido = unido + palabra
			unido = unido + " "


			
			contador += 1
		unido = unido + mensajeFin	
		#print(unido)
		return unido

	def mensajePrueba(self, texto):
		dividido = texto.split(" ")
		
		unido = ""
		tamano = len(dividido)
		#print(largoNombre)
		contador = 1 
		for palabra in dividido:
			
			if "goo" in palabra:
				palabra  = " \n\n http://www." + palabra + " \n \n"
			
			unido = unido + palabra
			unido = unido + " "


			
			contador += 1
		unido = unido + mensajeFin	
		#print(unido)
		return unido
