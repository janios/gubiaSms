#!/usr/bin/python2
# -*- coding: utf-8 -*-

from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


class Contactos():

    #Elimina codigo unicode
    def force_text(self, text):
        if (isinstance(text, unicode)):
            return text.encode("utf-8")
        return str(text)

    def eliminarContacto(self, telefono):
        try:
            global service
            global listadoTelefonos
            
            if telefono in listadoTelefonos:
                id = listadoTelefonos[telefono]
                service.people().deleteContact(resourceName = id).execute()
                print("Contacto {} eliminado ".format(telefono))
            else:
                print("El Contacto {} no existe en los contactos".format(telefono))
        except:
            print("Error al eliminar contactos")

    def agregarContacto(self, telefono, nombre=None):
        try:
            global service
            global listadoTelefonos        
            if (nombre == None):
                nombre = telefono
            
            if not (telefono in listadoTelefonos):
                print("Se agregara Contacto {}".format(telefono))
                
                service.people().createContact(body={
                        "names": [
                            {
                                "givenName": nombre
                            }
                        ],
                        "phoneNumbers": [
                            {
                                'value': telefono
                            }
                        ]
                        
                    }).execute()
                print("Contacto Creado")
                return "Contacto Creado"
            print("Contacto Existente")   
            return "Contacto Existente"
        except Exception as inst:
            print("Error al agregar contactos",inst)


    def agregarContactos(self, listaContactos):
        for conta in listaContactos:
            self.agregarContacto(conta)


    def listarContactos(self):
        try:
            global service
            results = service.people().connections().list(
                resourceName='people/me',
                #pageSize=10,
                personFields='names,phoneNumbers').execute()
            connections = results.get('connections', [])

            listadoTelefonos ={}
            idContacto = ""

            for person in connections:
                #print(person)
                names = person.get('names', [])
                telefono = person.get('phoneNumbers', [])
                recurso = person.get('resourceName', [])
                idContacto = recurso
                if names:
                    name = names[0].get('displayName')
                    telefono = self.force_text(telefono[0].get('value'))
                    recurso = self.force_text(recurso)
                    listadoTelefonos[telefono] = recurso
            return listadoTelefonos
        except Exception as inswt:
            print("Error al listar contactos",inswt)

# If modifying these scopes, delete the file token.json.
try:
    SCOPES = 'https://www.googleapis.com/auth/contacts'

    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('people', 'v1', http=creds.authorize(Http()))
    contactos = Contactos()
    listadoTelefonos =  contactos.listarContactos()
#except: 
except Exception as inst:
    print("Error al crear la instancia",inst)
