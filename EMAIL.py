import imaplib
import email
from email.header import decode_header
from email.header import make_header

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
 

#se conecta al correo
m = imaplib.IMAP4_SSL("imap.gmail.com")
m.login("smsgubia@gmail.com", "gubiasms")
m.select("inbox")

tema = ''

#selecciona los emails no vistos
result, mails_data = m.search(None, "(UNSEEN)")
mails_ids = mails_data[0]
mails_id_list = mails_ids.split() 

#controla el numero total de mensajes
cuenta = 0

#controla el numero de sms por enviar
mensajes = 0

for i in reversed(mails_id_list):
	cuenta = cuenta + 1
	result, mail_data = m.fetch(i, "(RFC822)")
	raw_email = mail_data[0][1]
	this_email = email.message_from_string(raw_email)
	de = get_from(this_email)
	tema = get_subject(this_email)

	#Valida el dominio de los correos		
	if 'escamilla.cristian@gmail.com' in de:
		
		#Valida que el subject este compuesto de digitos
		if tema.isdigit():
			mensajes = mensajes + 1
			body = get_body(raw_email)
 	
			print de
			print tema
			print body	
	

print cuenta
print mensajes

m.logout()
