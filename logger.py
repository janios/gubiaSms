
#!/usr/bin/python2
# -*- coding: utf-8 -*-

class Logger():

     #Elimina codigo unicode
    def force_text(self, text):
        if (isinstance(text, unicode)):
            return text.encode("utf-8")
        return str(text)

    