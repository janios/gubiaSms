#!/usr/bin/python2
# -*- coding: utf-8 -*-
from whatsappImagen import Whatsapp
import csv


archivo = raw_input("Que archivo? ")

nombre = archivo + ".csv"

whats = Whatsapp()

contador = 0

with open(nombre) as File:  
	reader = csv.reader(File)
	for row in reader:
		contador += 1
		print(contador)
		numero = row[0]
		print(numero)
		resultado = whats.enviarWhats(numero)
		









