#!/usr/bin/python2
# -*- coding: utf-8 -*-

class SeparaTexto():


	def separa(self, mensaje):
		#mensaje = "Hola PRUEBA ya puede pasar por sus resultados a Gubia o descargalos aqui bit.ly/2Sdwlr6 -Aproveche en Febrero Chequeo Gold $699"
		dividido = mensaje.split()

		resultado = -1
		contador = 0
		for palabra in dividido:
			encontrado = palabra.find("/")
			if(encontrado!=-1):
				#print("Entro")
				resultado = contador
			contador=contador + 1
			#print(palabra)
		#print(resultado)
		if(resultado !=-1):
			dividido.pop(resultado)
			dividido.pop(resultado -1)
			dividido.pop(resultado -2)
			dividido.pop(resultado -3)

			base = " "
			unido = base.join(dividido)
		else:
			unido = mensaje
		return unido
