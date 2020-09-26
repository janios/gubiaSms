import gammu

# Create state machine object
sm = gammu.StateMachine()

# Read configuration of gammu
sm.ReadConfig()

# Conect to phone
sm.Init()

# Reads network information 
netinfo = sm.GetNetworkInfo()

# Print information

#print 'Network name: %s' % netinfo['NetworkName']
#print 'Network code: %s' % netinfo['NetworkCode']
#print 'LAC: %s' % netinfo['LAC']
#print 'CID: %s' % netinfo['CID']


texto = 'GAMMU PRUEBA'
numero = '5554374058'


# Message
message = {
    'Text': texto, 
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



print 'ENVIADO: %s' % enviado 
