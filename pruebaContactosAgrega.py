#!/usr/bin/python2
# -*- coding: utf-8 -*-
from contactos import Contactos
import time


telefonos = ['5554374058', '7971109731', '7971065201', '2223178965', '4422044583', '2223241151']
#telefonos = ['7971111441']
nombre = 'Uriel'
#texto = "Gubia le informa que los resultados de su paciente \n \n  *SEBASTIAN GONZALEZ HERRERA*  \n\n ya se encuentran en su portal en _*http://www.GUBIA.MX*_ o en \n\n  _http://www.goo.gl/zQGWrQ_"
#texto = "Hola *ANDRES* ya puede pasar por sus resultados a Gubia o descargalos aqui \n  \n http://www.goo.gl/AJZuQd \n  \n *Aproveche en Septiembre Chequeo Premium $599* \n  \n_--Mensaje generado de manera automática favor de no contestar_ \n _--Si no puede acceder a sus resultados agregue este numero a sus contactos_"
#texto = "Conoce nuestras nuevas instalaciones, Frente al Hospital General de Zacatlán *Gubia Diagnostico Especializado* -En Agosto Limpieza Dental $150"


contactos = Contactos()



resultado = contactos.agregarContacto("5554374058", "Cristian")

	

#time.sleep(10)

#print("El resultado de mandar whats es {}".format(resultado2))


print("Termina Prueba")

