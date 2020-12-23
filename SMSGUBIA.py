#!/usr/bin/python2
# -*- coding: utf-8 -*-

import imaplib
import email
from email.header import decode_header
from email.header import make_header
import gammu
import time 
import smtplib 
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
import os
import urllib
import sys
import csv
import traceback
from random import randint
import psutil
import mysql.connector
from reporteador import Reporteador
from mensajesBase import MensajesBase
import commands
from recibirMensajes import RecibirMensajes
from whatsapp import Whatsapp
from separaTexto import  SeparaTexto
from contactos import Contactos



def pruebaContactos():
	contactos= Contactos()
	resultado = contactos.agregarContacto("5554374058", "Cristian")
	print("Termina Prueba")
	return "OK"

def unicode2txt(mensaje):
	return mensaje.encode('ascii','ignore')

def verificaCorreo(de):
	archivo = open('muestra.csv','r')
	texto = archivo.read()
	archivo.close();
	cadena = texto.split(",");
	correoCorrecto = 0
	for correo in cadena:
		#print("se va a checar {} no este en {}".format(correo, prueba))
		if correo in de:
			#print("esta")
			correoCorrecto = 1
	return correoCorrecto

def muestra(telefono):
	meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
	indice = int(time.strftime('%m'))

	texto1 = "Gubia le informa que los resultados de su paciente ANDRES GORDILLO CORTES ya se encuentran en su portal en GUBIA.MX o en  goo.gl/wxat3U"
	texto2 = "Hola ANDRES ya puede pasar por sus resultados a Gubia o descargalos aquí goo.gl/wxat3U -Aproveche en {} Chequeo Premium $599".format(meses[indice -1])


	textos = [texto1, texto2]

	for texto in textos:
                enviarWhats(texto, telefono)

def resagado(tabla):

	print(separador)
	conector = mysql.connector.connect(**config_mysql)
	# cursor, clase para el manejo del SQL ???
	cursor = conector.cursor()
	# Ejecutamos la consula SQL
	registros= []
	cursor.execute("Select * from {}".format(tabla))
	for row in cursor.fetchall():
	    lista= []
	    for col in row:
	   	#print(col)
		   	lista.append(col)
	    registros.append(lista)
	print("Existen {} mensajes de {} resgados".format(len(registros), tabla))
	cursor.close()
	conector.close()
	return registros

def resagadosSms():
	tabla = "mensajesAtrasados"
	#obtiene los mensajes atrasados
	registros = resagado("mensajesAtrasados")

	if len(registros)==0:
		print("No existen SMS resagados")
		print(separador)
		return 0

	contador = 0
     
	ultimoEnviado = leerArchivo('ultimoEnviado.csv')
	

	for men in registros:
		

		#si sobrepasa el numero maximo de intentos  y el id es menor al ultimo enviado elimina el mensaje
		if ((men[4] > intentosSms) and (men[0] < ultimoEnviado )):
			print("Sobrepaso el numero de intentos permitidos se borrara el mensaje")
			query = "DELETE FROM `{}` WHERE `id` = '{}'".format(tabla,men[0])
			ejecutarbd(query)
			query = "INSERT INTO `mensajesAtrasados`(`id`, `fecha`, `numero`, `mensaje`, `intento`) VALUES ({},{},{},{},{})".format(men[0],men[1],men[2],men[3],men[4])
			ejecutarbd(query)
		else:
			#sms_send(texto, numero)	
			resultado = sms_send(force_to_unicode(men[3]),force_to_unicode(men[2]))
			if resultado == 1:
				query = "DELETE FROM `{}` WHERE `id` = '{}'".format(tabla,men[0])
				ejecutarbd(query)
				
				fechaconsulta = "{}-{}-{}".format(time.strftime('%Y'),time.strftime('%m'),time.strftime('%d'))
				horamensaje = time.strftime('%H:%M:%S')
				mensaje = unicode2txt(men[3]) 
				numero = unicode2txt(men[2])
				query="INSERT INTO `detalleMensajes`(`fecha`, `remitente`, `numero`, `mensaje`, `horaIntento`, `enviado`) VALUES ('{}','{}','{}','{}','{}','{}')".format(fechaconsulta,"Resagados SMS",numero,mensaje,horamensaje,"1")
				#print(query)
				ejecutarbd(query)
				print(separador)

				contador += 1
			else:
				intentos = int(men[4]) + 1
				print(" Mensaje no enviado, el mensaje del numero {} tiene {} intentos de envio".format(men[3], intentos))
				query = "UPDATE `{}` SET `intento`={}} WHERE 1".format(tabla, intentos)
	print("{} mensajes sms resagados enviados".format(contador))
	print(separador)
	return contador

def resagadosWhats():
	registros = resagado("whatsapp")

	if len(registros)==0:
		print("No existen mensajes resagados de Whatsapp")
		print(separador)
		return 0

	contador = 0
	for men in registros:
		contador +=1
		resultado = enviarWhats(men[2].encode('utf-8'),men[1],2)
		espera = randint(20,45)
		print ("la espera sera de: {}".format(espera))
		time.sleep(espera) 


		if resultado == "Whatsapp enviado correctamente":
			query = "DELETE FROM `whatsapp` WHERE `id` = '{}'".format(men[0])
			ejecutarbd(query)
		if (contador == 5):
			break;
	print("Mensajes resagados de whatsapp enviados")
	print("separador")
	return contador

def enviarWhats(texto, telefono, modo = 1):
	#agrega contactos
	contactos = Contactos()
	#agrega el contacto
	contactoAgregado = contactos.agregarContacto(telefono, "PacieneGubiaa"+ telefono)
	time.sleep(17)
	restultado = ""
	print(separador)
	if ("Creado" in contactoAgregado) or ("Existente" in contactoAgregado): 
		manejardorWhats = Whatsapp()
		resultado2 = manejardorWhats.enviarWhats(telefono, texto)
		print(resultado2)
         	#elimina el contacto
		#contactos.eliminarContacto(telefono.encode('utf-8'))
		if  "success" in resultado2:
			resultado = "Whatsapp enviado correctamente"
			print(separador)
		else: 
			print("Error al enviar mensaje verificar Whatsapp")
			print(separador)
			resultado = "Error al enviar mensaje verificar Whatsapp"
			#envia mensaje de error a los telefonos predefinidos
			for error in telefonosError:
				sms_send('ERROR DE Whatsapp CHECAR POR FAVOR',error)
			if (modo == 1):
				fecha = "{}-{}-{}".format(time.strftime('%Y'),time.strftime('%m'),time.strftime('%d'))
				query="INSERT INTO `whatsapp`(`telefono`, `mensaje`, `fecha`) VALUES ('{}','{}','{}')".format(telefono, texto, fecha)
				print(query)
				ejecutarbd(query)
				print("Mensaje guardado para posterior envio")
				print(separador)
	else:
		fecha = "{}-{}-{}".format(time.strftime('%Y'),time.strftime('%m'),time.strftime('%d'))
		query="INSERT INTO `whatsapp`(`telefono`, `mensaje`, `fecha`) VALUES ('{}','{}','{}')".format(telefono, texto, fecha)
		print(query)
		ejecutarbd(query)
		print("Mensaje guardado para posterior envio")
		print(separador)

	return resultado
	
def force_to_unicode(text):
   #"If text is unicode, it is returned as is. If it's str, convert it to Unicode using UTF-8 encoding"
    return text if isinstance(text, unicode) else text.decode('utf8')

def mensajesDesdeBase():
	contador = 0
	print(separador)
	print("Mensajes desde la Base de datos")
	#crea un objeto MensajesBase
	manejador = MensajesBase()
	#obtiene los mensajes de la Base MSSQL
	mensajes = manejador.consulta()
	#si se genera un error manda mensaje
	#resulados[total en base, enviados]
	listaMensajes=[0,0]

	if mensajes == "Error":
		print("Error leyendo MSSQL")
	else:
		#verifica que exista algun mensaje
		listaMensajes[0] = len(mensajes)
		if len(mensajes)!=0:
			
			cuenta = 1
			#itera en los mensajes para enviarlos
			for mensaje in mensajes:
				print(separador)
				if (cuenta == mensajesCiclo + 1):
					break
				numero = str(mensaje[2])
				#nueva basse
				texto = force_to_unicode(mensaje[4]).encode('utf-8')
				#envia SMS desde la base texto, numero
				
				resultado = sms_send(texto, numero) 
				fechaconsulta = "{}-{}-{}".format(time.strftime('%Y'),time.strftime('%m'),time.strftime('%d'))
				

				textoWhats = force_to_unicode(mensaje[3]).encode('utf-8')
				enviarWhats(textoWhats, numero)
				#genera hora de envio del mensaje
				horamensaje = time.strftime('%H:%M:%S')	
				#en caso de que el mensaje se envio agrega 1 al contador de enviados
				if resultado == 1:
					contador = contador +1
					#m.store(i, '-FLAGS', r'(\Seen)')
					print ("Mensaje Enviado de la Base de datos")
					#genera la fecha del mensaje
					#agrega registo al detalleMensajes
					query="INSERT INTO `detalleMensajes`(`fecha`, `remitente`, `numero`, `mensaje`, `horaIntento`, `enviado`) VALUES ('{}','{}','{}','{}','{}','{}')".format(fechaconsulta,"Base de Datos",mensaje[2],texto,horamensaje,str(resultado))
					#print(query)
					ejecutarbd(query)
					#agrega a la base de respaldo de la mensajes	
					query= "INSERT INTO smsSalida(fecha, numero, mensaje, enviado) VALUES ('{}','{}','{}','{}')".format(mensaje[1],mensaje[2],texto,str(resultado))
					#print(query)
					ejecutarbd(query)
					#escribe el valor del ultimo archivo enviado en ultimoEnviado.csv
					escribirarchivo('ultimoEnviado.csv',mensaje[0])
					#elimina el registro de la base MSSQl
					manejador.eliminacion(mensaje[0])
					
					print(separador)
				#si el mensaje no es enviado lo manda a la tabla mensajesAtrasados con numero de intento 1, para posterior envio
				else:
					print("Error al mandar el mensaje se enviara en mensajesAtrasados")
					#lo envia a mensajes atrasados
					query = "INSERT INTO `mensajesAtrasados`(`id`, `fecha`, `numero`, `mensaje`, `intento`) VALUES ('{}','{}','{}','{}','{}')".format(mensaje[0], mensaje[1], numero, texto,1)
					ejecutarbd(query)
					#lo elimina de la base de MSSQL
					manejador.eliminacion(mensaje[0])

				cuenta += 1
		else:
			print("No existen Mensajes en la BD para enviar")
	print(separador)
	listaMensajes[1] = contador
	return listaMensajes

def reportes(direccionreportes, codsql=None):
	#crea un objeto de la clase reporteador
	reporteador = Reporteador()
	#verifica el parametro de la consulta
	if codsql ==None:
		#si no hay consulta se se genera un reporte sin sql
		reporte = reporteador.reporteDetalleMensajes()	
	else:
		print(codsql)
		#en caso de que se pase un parametro se verifica si la consulta es correcta
		reporte = reporteador.reporteDetalleMensajes(codsql)

	if "Error" in reporte:
		return "Error"
	else:
		mensajereportes = "Envio de reportes " + time.strftime('%H:%M:%S')
		reporte2 = reporteador.reporteRegistroTotal()
		#crea una lista de los reportes generados	
		lista = ["reporte.xlsx"]
		for archivo in lista:
			solicitud_reportes(direccionreportes, mensajereportes, archivo)			
		print("Reportes Enviados")
		return "OK"	

def ejecutarbd(query):
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

def pruebaDirecta():
	with open('contenido.txt') as csvarchivo2:
		entrada2 = csv.reader(csvarchivo2)
		for reg2 in entrada2:
			contenido = reg2[0]
			contenido = contenido + " enviado el " + time.strftime('%d %b %Y %H:%M:%S')
	#abre el archivo para envio de mensajes de aviso
	with open('directorio.csv') as csvarchivo:
		entrada = csv.reader(csvarchivo)
		for reg in entrada:
			telefono = reg[0]
			print(telefono)
			print(contenido)
			sms_send(contenido, telefono)
			enviarWhats(contenido, telefono)

def mensajeprueba():
	#verifica los horarios del archivo
	with open('horarioMensajePrueba.csv') as csvarchivo3:
		entrada3 = csv.reader(csvarchivo3)
		
		for reg3 in entrada3:
			hora1 = reg3[0]
			hora2 = reg3[1]
	horaInicio = int(hora1)
	horaFinal = int(hora2)	        
	print(horaInicio)
	print(horaFinal)

	comparador = time.strftime('%H')+time.strftime('%M')
	fNumerico = int(comparador)

	print(fNumerico)

	if (fNumerico > horaInicio) and (fNumerico<horaFinal):
		#obtine el contenido del archivo contenido.txt
		pruebaDirecta()

def reportes_para(destinatario):
	lista = destinatario.split()
	if len(lista)==2:
		correo = destinatario.split()[1].lower()
	else:
		correo= "Error"
	valido = 0
	print(correo)
	if '@' in correo and '.' in correo:
		valido = 1
		print ("correo valido")
	if ' ' in correo:
		valido = 0
	if valido == 0:
		correo = "ERROR"
	print(valido)
	print(correo)
	return correo

def get_ip():
	a = os.popen("curl -s http://icanhazip.com").read()
	textoip = a.decode('UTF-8')
	return textoip	

#obtine el remitente del from
def get_remitente(dato):
	a = dato.find('<')
	b = dato.find('>')
	c = dato[a+1:b]
	return c

#Envia correo con los reportes del sistema
def solicitud_reportes(direccionreportes, mensajereportes,archivo):
	fromaddr = "smsgubia@gmail.com"
	toaddr = direccionreportes
 
	msg = MIMEMultipart()
 
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = archivo
 
	body = mensajereportes
 
	msg.attach(MIMEText(body, 'plain'))
 
	filename = archivo
	agregado = '/home(pi/sms/' + archivo
	attachment = open(archivo, "rb")
 
	part = MIMEBase('application', 'octet-stream')
	part.set_payload((attachment).read())
	encoders.encode_base64(part)
	part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
 
	msg.attach(part)
 
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "gubiasms")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()

#Envia correo de eror si el dongle no funciona
def mensaje_dongle(direccion, texto, tema):
	fromaddr = "smsgubia@gmail.com"
	toaddr = direccion
	msg = MIMEMultipart()
	msg['From'] = fromaddr
	msg['To'] = toaddr
	msg['Subject'] = tema
	body = texto
	msg.attach(MIMEText(body, 'plain'))
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(fromaddr, "gubiasms")
	text = msg.as_string()
	server.sendmail(fromaddr, toaddr, text)
	server.quit()
	#Verifica que el sms funcione con la variable smssetup

def sms_setup():
	
	try:
		# Create state machine object
		sm = gammu.StateMachine()
		# Read configuration of gammu
		sm.ReadConfig()
		# Conect to phone
		sm.Init()
		#netinfo = sm.GetNetworkInfo()
		smssetup = 1
		#print(netinfo)
				
	except gammu.GSMError:	
		smssetup = 0
		return smssetup
	
	finally:
		#termina coneccion con el dongle
		sm.Terminate()

	return smssetup

#envia sms
def sms_send(texto, numero):
	
	try:# Create state machine object
		#sm = gammu.StateMachine()
		# Read configuration of gammu
		#sm.ReadConfig()
		# Conect to phone
		#sm.Init()
		#netinfo = sm.GetNetworkInfo()
		# cierra conexion
		#sm.Terminate()
		texto = force_to_unicode(texto).encode('utf-8')
		separa = SeparaTexto()
		textoCortado = separa.separa(texto)
		textouni= force_to_unicode(texto)	
		mensaje = 'gammu sendsms TEXT {} -text "{}"'.format(numero, textoCortado)
		#print(mensaje)
		dato = commands.getoutput(mensaje)
		#message = {
		#	'Text': textouni, 
		#	'SMSC': {'Location': 1},
		#	'Number': numero,
		#}	
		# Send Message
		# Send SMS if all is OK
		#dato = sm.SendSMS(message)
		print(dato)
		#si el dato funciona regresa un uno y se da un tiempo de espera
		if "OK" in dato:
			enviado = 1
			espera = randint(9,23)
			print("Numero: 	{}".format(numero))
			print(texto)
			print ("la espera sera de: {}".format(espera))
			time.sleep(espera)
		else:
			enviado = 0
	except gammu.GSMError:
		# Show error if message not sent
		print("error en envio de mensaje")
		enviado = 0
	return enviado	

#obtiene para obtener el tema del email
def get_subject(email):
	h = decode_header(email.get('subject'))
	return unicode(make_header(h)).encode('utf-8')

#obtine el remitente del email
def get_from(email):
	j = decode_header(email.get('from'))
	return unicode(make_header(j)).encode('utf-8')

#obtiene el mensaje
def get_body(message_body):
	msg = email.message_from_string(message_body)
	text = ""
	if msg.is_multipart():
		html = None
		for part in msg.get_payload():
			#print "%s, %s" % (part.get_content_type(), part.get_content_charset())
			if part.get_content_charset() is None:
				# We cannot know the character set, so return decoded "something"
				text = part.get_payload(decode=True)
				continue
			charset = part.get_content_charset()
			if part.get_content_type() == 'text/plain':
				text = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
			if part.get_content_type() == 'text/html':
				html = unicode(part.get_payload(decode=True), str(charset), "ignore").encode('utf8', 'replace')
		if text is not None:
			return text.strip()
		else:
			return html.strip()
	else:
		text = unicode(msg.get_payload(decode=True), msg.get_content_charset(), 'ignore').encode('utf8', 'replace')
		return text.strip()

def instancias():
	instancias = 0
	for process in psutil.process_iter():
		cadena = str(process.name)
		if (cadena.find("SMSGUBIA")) > -1:
			instancias = instancias +1
		if instancias>=2:
			print("Ya se esta ejecutando una Instancia")
			sys.exit()

def escribirarchivo(lugar, valor = 0):
	archivo = open(lugar,'w')
	archivo.write("{}".format(valor))
	archivo.close()

def escribirincrementar(lugar):
	archivo = open(lugar,'r+')
	incrementa = int(archivo.read()) +1
	archivo.seek(0)
	archivo.write(str(incrementa))
	archivo.close()
	return incrementa

def leerArchivo(lugar):
	archivo = open(lugar,'r')
	incrementa = archivo.read()
	print incrementa
	archivo.close()
	return incrementa	

#En caso de que se tenga una instancia de SMSGUBIA sale del programa
instancias()

#establece preuba de contactos
pruebaContactos()

#telefonos para notificar errores de internet o whatsapp
telefonosError = ['5554374058','7971109731']
correosError = ['escamilla.cristian@gmail.com', 'uriel@gubia.mx']
mensajesCiclo = 5
correoFuente = "smsgubia@gmail.com"
contrasenaFuente = "gubiasms"
intentosSms = 3

separador = "========================================================="

fechahora = time.strftime('%d %b %y %H:%M:%S')

# Variable con la configuracion de la conexion
config_mysql = {
	'user': 'root',
	'password': 'gubia',
	'host': 'localhost',
	'database': 'smsGubia',
}

mensajeprueba()


#CICLO INFINITO
while True:
	#valida que funcione el dongle 
	dongleok = sms_setup()
	#valida coneccion al correo (internet)
	try:
		m = imaplib.IMAP4_SSL("imap.gmail.com")
		m.login(correoFuente, contrasenaFuente)
		m.select("inbox")
		internet = 1
	except:
		internet = 0
	#solo funciona en caso de que el dongle y el correo esten correctos
	
		
	if (dongleok == 1 and internet == 1) :
		#Elimina los log de errores de dongle e intenert
		escribirarchivo('dongle.log')
		escribirarchivo('internet.log')
	
		try:	
			fecha = time.strftime('%d %b %y')
			horainicio = time.strftime('%H:%M:%S')
			print ("Hora de Inicio del ciclo %s" %horainicio)
			print ("Fecha del ciclo %s" %fecha)

			tema = ''
			#selecciona los emails no vistos

			result, mails_data = m.search(None, "(UNSEEN)")
			mails_ids = mails_data[0]
			mails_id_list = mails_ids.split() 
			#controla el numero total de mensajes
			cuenta = 0
			#controla el numero de sms por enviar
			mensajes = 0
			#controla los mensajes enviados
			enviados = 0
			for i in reversed(mails_id_list):
				cuenta = cuenta + 1
				#limita el numero de mensajes por Ciclo 
				if (cuenta == mensajesCiclo + 1):
					print("Total mensajes del ciclo {}".format(mensajesCiclo))
					break
				result, mail_data = m.fetch(i, "(RFC822)")
				raw_email = mail_data[0][1]
				this_email = email.message_from_string(raw_email)
				de = get_from(this_email)
				tema = get_subject(this_email)
				#elimina espacios del tema
				tema = tema.strip()
				#pone en mayusculas el Tema
				tema = tema.upper()
				print("El numero o comando es %s" %tema)

				print(tema)
				#Valida el dominio de los correos		
				

				#verifica que el correo recibido sea correcto 				

				correoCorrecto = verificaCorreo(de)

				if (correoCorrecto):
					print("CORREO ORIGEN {}".format(de))
					#Valida que el subject este compuesto de digitos
					if tema.isdigit():
						mensajes = mensajes + 1
						body = get_body(raw_email)
						#si el mensaje se envia la variable resultado =1 sino 0
						resultado = sms_send(body, tema)
						#envia whats
						whats = enviarWhats(body, telefono)
						#print(whats)
											  	
						#obtiene hora de envpio de mensaje
						horamensaje = time.strftime('%H:%M:%S')	
						#en caso de que el mensaje se envio agrega 1 al contador de enviados
						if resultado == 1:
							enviados = enviados +1
							#m.store(i, '-FLAGS', r'(\Seen)')
							print (de)
						else:
							m.sotre(i, '-FLAGS', r'(\Seen)')
						#escribe al final el archivo detalleMensajes (reportes)
						#detalle = open('detalleMensajes.csv','a')
						remitente = get_remitente(de)
						#detalle.write(fecha + ',' + remitente + ',' + tema + ',' + body + ',' + horamensaje + ',' + str(resultado) +  "\n")			
						#detalle.close()
						#escribe en la base de datos
						fechaconsulta = "{}-{}-{}".format(time.strftime('%Y'),time.strftime('%m'),time.strftime('%d'))
						query="INSERT INTO `detalleMensajes`(`fecha`, `remitente`, `numero`, `mensaje`, `horaIntento`, `enviado`) VALUES ('{}','{}','{}','{}','{}','{}')".format(fechaconsulta,remitente,tema,body,horamensaje,str(resultado))
						#print(query)
						ejecutarbd(query)


					elif tema == "REPORTES":
						direccionReportes = get_remitente(de)
						reportes(direccionReportes)

					elif tema =="REPORTES_SQL":
						direccionCorreo = get_remitente(de)
						#obtiene el contenido del correo
						body = get_body(raw_email)
						resultado = reportes(direccionCorreo,body)
						if resultado == "Error":
							mensaje = "Error SQL la tabla se llama 'detalleMensajes' y los campos 'id','fecha','remitente','numero','mensaje','horaIntento','enviado' "
							mensaje_dongle(direccionCorreo, mensaje ,'ERROR')

					elif '@REPORTES_SQL' in tema:
						#obtiene el destinatario de los mensajes
						remitente = reportes_para(tema)
						#obtiene quien esta solicitando reportes
						direccionip = get_remitente(de)						

						if remitente == "ERROR":
							print ("ERRROR DE CORREO")						
							mensaje_dongle(direccionip, 'CORREO INVALIDO','ERROR')
						else:
							print ("CORREO VALIDO")
							body = get_body(raw_email)
							print(body)
							resultado = reportes(remitente,body)
							if resultado == "Error":
								mensaje = "Error SQL la tabla se llama 'detalleMensajes' y los campos 'id','fecha','remitente','numero','mensaje','horaIntento','enviado' "
								mensaje_dongle(direccionip, mensaje ,'ERROR')

					elif '@REPORTES' in tema:
						#obtiene el destinatario de los mensajes
						remitente = reportes_para(tema)
						#obtiene quien esta solicitando reportes
						direccionip = get_remitente(de).lower()					

						if remitente == "ERROR":
							print ("ERRROR DE CORREO")						
							mensaje_dongle(direccionip, 'CORREO INVALIDO','ERROR')
						else:
							print ("CORREO VALIDO")
							reportes(remitente)

					elif tema == "IP":
						direccionip = get_remitente(de)
						ippublica = get_ip()							
						print (ippublica)
						mensaje_dongle(direccionip, ippublica,'IP PUBLICA') 
					
					elif tema == "REINCIAR":
						direccionip = get_remitente(de)
						print (ippublica)
						mensaje_dongle(direccionip, 'REINICIANDO','REINICIANDO')
						os.system('sudo shutdown -r now')

					elif tema == "APAGAR":
						direccionip = get_remitente(de)
						print (ippublica)
						mensaje_dongle(direccionip, 'APAGAR','APAGAR')
						os.system('sudo shutdown now')
					
					elif tema == "PRUEBA": 
						pruebaDirecta()


					elif tema == "ONLINE":
						direccionip = get_remitente(de)
						mensaje_dongle(direccionip, 'ONLINE desde : '+ fechahora ,'ONLINE')
						print ("ONLINE")

					elif tema == "MUESTRA":
						print("MENSAJES DE MUESTRA")
						print(separador)
						telefono = get_body(raw_email)
						muestra(telefono)

					else:			
						direccionip = get_remitente(de)
						mensaje = "Los comandos válidos son: \n REPORTES envía reportes al correo \n REPORTES_SQL envía reportes al correo \n @REPORTES correo@dominio.com.  envía reportes al correo solicitado  \n IP  envía ip pública \n @REPORTES_SQL correo@dominio.com.  envía reportes al correo solicitado \n ONLINE envía señal de online \n PRUEBA envía mensaje de prueba"
						mensaje_dongle(direccionip, mensaje,'ERROR DE COMANDO') 			

			#ejecuta mensajes desde base
			listaMensajes = mensajesDesdeBase() 
			mensajesBase = listaMensajes[0]
			enviados = enviados + listaMensajes[1]
			print(separador)
			#recibe mensajes y los envia a la bd
			manejadorMensajes = RecibirMensajes()
			menRecibidos = manejadorMensajes.recibir()
			print(separador)
			#contadorResagadosWhats = resagadosWhats()
			#contadorResagadosSms = resagadosSms()

			#obtiene el momento del final de proceso	
			horafinal = time.strftime('%H:%M:%S')

			
			print ("Archivos procesados %s" %cuenta)
			print ("Mensajes procesador %s" %mensajes)
			print ("Hora de termino %s" %horafinal)
			print ("Mensaje Enviados correo %s" %enviados)
			print ("Mensaje Enviados Base de datos %s" %mensajesBase)
			print("Mensajes Recibidos %s" %menRecibidos)
			print("Mensajes resagados Whatsapp %s" %contadorResagadosWhats)
			print("Mensajes resagados SMS %s" %contadorResagadosSms)
			print (separador)
			mensajes+=mensajesBase
			#escribe al final del archivo registroTotal solo cuando hay mensajes posibles
			if (mensajes) != 0:
				#resumen = open('registroTotal.csv','a')
				#resumen.write(fecha+',' + horainicio + "," + str(cuenta) + ',' + str(mensajes)  +',' + str(enviados)+ ',' + horafinal + "\n")
				#resumen.close()
				m.logout()
				fechaconsulta = "{}-{}-{}".format(time.strftime('%Y'),time.strftime('%m'),time.strftime('%d'))
				query="INSERT INTO `registroTotal`(`fecha`, `horaInicio`, `totalCorreos`, `baseDatos`, `mensajesXEnviar`, `mensajesEnviados`, `horaFinal`) VALUES ('{}','{}','{}','{}','{}','{}','{}')".format(fechaconsulta,horainicio,str(cuenta),str(mensajesBase),str(mensajes),str(enviados),horafinal)
				#print(query)
				ejecutarbd(query)
				print (separador)
	
		except:
			error = traceback.format_exc()
			print ("ERROR OS")
			print(error)
			#os.system('sudo shutdown -r now')			
			#internet no funciona dongle si
	elif (internet == 0 and dongleok == 1):
		#reinicia log de dongle
		escribirarchivo('dongle.log')
		#revisa log de internet y suma uno
		contadorinternet = escribirincrementar('internet.log')
	
		if contadorinternet >35:
			for error in telefonosError:
				sms_send('ERROR DE INTERNET CHECAR POR FAVOR',error)
				print ("internet no funciona mensaje enviado")
			#reiniciar el log
			escribirarchivo('internet.log')
		else:
			print ("Internet no funciona {}".format(contadorinternet))
	#internet funciona dongle no
	elif (internet == 1 and dongleok == 0):
		#reinicia log de internet 
		escribirarchivo('internet.log')
		#revisa log de dongle  y suma uno
		contadordongle = escribirincrementar('dongle.log')
		
			#Al primer ciclo solo manda mensaje en pantalla al sengundo 
		if contadordongle > 35:
			#envia mensaje de error a dongle de error
			for error in correosError:
				mensaje_dongle(error, 'DONGLE 3G NO FUNCIONA FAVOR DE REVISAR', 'ERROR DONGLE 3G')
				print ("Dongle no funciona mensaje enviado")
			#reinicia log dongle
			escribirarchivo('dongle.log')
			#reincia sistema 
			os.system('sudo shutdown -r now')
		else:
			print ("Dongle no funciona {}".format(contadordongle)) 
	print ("Dongle %s" %dongleok)
	print ("internet %s" %internet)

	
