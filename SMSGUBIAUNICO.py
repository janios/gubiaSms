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
from random import randint
import psutil


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
	correo = destinatario[10:]
	valido = 0
	print correo
	if '@' in correo and '.' in correo:
		valido = 1
		print ("valido", valido)
	if ' ' in correo:
		valido = 0
	if valido == 0:
		correo = "ERROR"
	print valido
	print correo
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
		netinfo = sm.GetNetworkInfo()
		smssetup = 1
		
	except gammu.GSMError:	
		smssetup = 0
		return smssetup
	
	return smssetup

#envia sms
def sms_send(texto, numero):
	# Create state machine object
	sm = gammu.StateMachine()
	# Read configuration of gammu
	sm.ReadConfig()
	# Conect to phone
	sm.Init()
	netinfo = sm.GetNetworkInfo()
	# Message
	
	textouni= texto.decode('UTF-8')	

	message = {
		'Text': textouni, 
		'SMSC': {'Location': 1},
		'Number': numero,
	}	

	# Send Message

	try:
		# Send SMS if all is OK
		sm.SendSMS(message)
		enviado = 1

	except gammu.GSMError:
    		# Show error if message not sent
   		enviado = 0
	espera = randint(20,45)
	print ("la espera sera de: ")
	print(espera)
	time.sleep(espera)
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

#En caso de que se tenga una instancia de SMSGUBIA sale del programa

for process in psutil.process_iter():
	cadena = str(process.name)
	if (cadena.find("SMSGUBIA")) > -1:
		print(process)
		print("Ejecutando actualmente no se ejecutará de nuevo")
		sys.exit()

#CICLO INFINITO DIFERENCIA ENTRE SMSGUBIA Y INFISMSGUBIA

fechahora = time.strftime('%d %b %y %H:%M:%S')
mensajeprueba()

while True:
	#valida que funcione el dongle 
	dongleok = sms_setup()
	#valida coneccion al correo (internet)
	try:
		m = imaplib.IMAP4_SSL("imap.gmail.com")
		m.login("smsgubia@gmail.com", "gubiasms")
		m.select("inbox")
		internet = 1
	except:
		internet = 0
	#solo funciona en caso de que el dongle y el correo esten correctos
	
		
	if (dongleok == 1 and internet == 1) :
		#Elimina los log de errores de dongle e intenerte
		archivo = open('dongle.log','w')
		archivo.write('0')
		archivo.close()

		archivo2 = open('internet.log','w')
		archivo2.write('0')
		archivo.close()
	
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
				if ('escamilla.cristian@gmail.com' in de) or ('@gubia.mx' in de) or ('smsgubia@gmail.com' in de) :
	
					#Valida que el subject este compuesto de digitos
					if tema.isdigit():
						mensajes = mensajes + 1
						body = get_body(raw_email)
						#si el mensaje se envia la variable resultado =1 sino 0
						resultado = sms_send(body, tema) 	
						#obtiene hora de envpio de mensaje
						horamensaje = time.strftime('%H:%M:%S')	
						#en caso de que el mensaje se envio agrega 1 al contador de enviados
						if resultado == 1:
							enviados = enviados +1
							#m.store(i, '-FLAGS', r'(\Seen)')
							print (de)
							print (tema)
							print (body)
						else:
							m.sotre(i, '-FLAGS', r'(\Seen)')
						#escribe al final el archivo detalleMensajes
						detalle = open('detalleMensajes.csv','a')
						remitente = get_remitente(de)
						detalle.write(fecha + ',' + remitente + ',' + tema + ',' + body + ',' + horamensaje + ',' + str(resultado) +  "\n")			
						detalle.close()		
					elif tema == "REPORTES":
						direccionreportes = get_remitente(de)
						mensajereportes = "Envio de reportes " + time.strftime('%H:%M:%S')
						archivo = "registroTotal.csv"
						solicitud_reportes(direccionreportes, mensajereportes, archivo)
						archivo = "detalleMensajes.csv"
						solicitud_reportes(direccionreportes, mensajereportes, archivo)
						print("Reportes Enviados")	
					
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


					elif '@REPORTES' in tema:
						remitente = reportes_para(tema)
						direccionip = get_remitente(de)

						if remitente == "ERROR":
							print ("ERRROR DE CORREO")						
	                                                mensaje_dongle(direccionip, 'CORREO INVALIDO','ERROR')
						else:

							print ("CORREO VALIDO")
							mensajereportes = "Envio de reportes " + time.strftime('%H:%M:%S')
							archivo = "registroTotal.csv"
                                       			solicitud_reportes(remitente, mensajereportes, archivo)
                                               		archivo = "detalleMensajes.csv"
	                                               	solicitud_reportes(remitente, mensajereportes, archivo)
							mensaje_dongle(direccionip, 'REPORTES ENVIADOS A ' + remitente,'REPORTES')
						print("Reportes enviados")							

					elif tema == "ONLINE":
						direccionip = get_remitente(de)
                                	        mensaje_dongle(direccionip, 'ONLINE desde : '+ fechahora ,'ONLINE')
						print ("ONLINE")	
					else:			
						direccionip = get_remitente(de)
						mensaje = "Los comandos válidos son: \n REPORTES envía reportes al correo \n IP  envía ip pública \n REPORTES correo@dominio.com.  envía reportes al correo solicitado \n ONLINE envía señal de online \n PRUEBA envía mensaje de prueba"
						mensaje_dongle(direccionip, mensaje,'ERROR DE COMANDO') 			

			#obtiene el momento del final de proceso	
			horafinal = time.strftime('%H:%M:%S')

			
			print ("Archivos procesados %s" %cuenta)
			print ("Mensajes procesador %s" %mensajes)
			print ("Hora de termino %s" %horafinal)
			print ("Mensaje Enviados %s" %enviados)
			print ("___________________________________")

			#escribe al final del archivo registroTotal solo cuando hay mensajes posibles
			if mensajes != 0:
				resumen = open('registroTotal.csv','a')
				resumen.write(fecha+',' + horainicio + "," + str(cuenta) + ',' + str(mensajes)  +',' + str(enviados)+ ',' + horafinal + "\n")
				resumen.close()
				m.logout()
	
		except:
			print ("ERROR OS", sys.exc_info()[0])
			#os.system('sudo shutdown -r now')			
			#internet no funciona dongle si
	elif (internet == 0 and dongleok == 1):
		#reinicia log de dongle
		archivo3 = open('dongle.log','w')
		archivo3.write('0')
		archivo3.close()
		
		#revisa log de internet y suma uno
		archivo4 = open('internet.log','r')
		contadorinternet = int(archivo4.read()) +1
		archivo4.close()

		archivo5 = open('internet.log','w')
		archivo5.write(str(contadorinternet))
		archivo5.close()
		#Al primer ciclo solo manda mensaje en pantalla al sengundo envia mensaje sms
		if contadorinternet >35:

			sms_send('ERROR DE INTERNET CHECAR POR FAVOR','5554374058')
			print ("internet no funciona mensaje enviado")
			archivo10 = open ('internet.log','r')
			archivo10.write('0')
			archivo10.close()
		else:

			print ("Internet no funciona primer ciclo")
	
	#internet funciona dongle no
	elif (internet == 1 and dongleok == 0):
		#reinicia log de internet 

		archivo6 = open('internet.log','w')
	        archivo6.write('0')
	        archivo6.close()
		
		#revisa log de dongle  y suma uno
	        archivo7 = open('dongle.log','r')
	        contadordongle = int(archivo7.read()) +1
	        archivo7.close()
	
	        archivo8 = open('dongle.log','w')
	        archivo8.write(str(contadordongle))
	        archivo8.close()
	        #Al primer ciclo solo manda mensaje en pantalla al sengundo 
		if contadordongle > 35:
			mensaje_dongle('escamilla.cristian@gmail.com', 'DONGLE 3G NO FUNCIONA FAVOR DE REVISAR', 'ERROR DONGLE 3G')
			print ("Dongle no funciona mensaje enviado")
			archivo9 = open('dongle.log','w')
			archivo9.write('0')
			archivo9.close()
			os.system('sudo shutdown -r now')
		else:
			print ("Dongle no funciona primera vez") 
	print ("Dongle %s" %dongleok)
	print ("internet %s" %internet)

	
