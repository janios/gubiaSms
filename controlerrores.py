archivo = open('dongle.log','r')
contenido = int(archivo.read())
archivo.close()
contenido = contenido +1

print contenido
archivo2 = open('dongle.log','w')
archivo2.write(str(contenido))
archivo2.close






