# -*- coding: latin-1 -*-

#configuraçãao para Galileo GEN1
#from configuraPCI import *
#configuração para Raspberry
from configuraPCIrasp import *

def leitura_temperatura():
		try:
			rs232.write('1')
			temperatura =int(rs232.read(4))
			celsius = temperatura/22.0
		except:
			celsius = 25.0
			print('Sensor Temperatura nao responde')
			print('celsius=25.0 recebe valor padrao')		
		#print (celsius)
		return celsius

def leitura_pot():	#sensor_phmetro
		try:
			rs232.write('2')
			adpot=int(rs232.read(4))
			#print ('Valor lido = {}\n'.format(sensor_phmetro))
			ph = adpot*14.0/1023.0
		except:
			ph =7.0
			print('Sensor Ph nao responde')
			print('valorph = 7.0 recebe valor padrao')		
		return ph

def leitura_pot2():	#sensor_pressao1
    #sensor_pressao1= pinos.analogRead(pino_pot2)
		try:
			rs232.write('3')
			sensor_pressao1=int(rs232.read(4))
			psi1 = sensor_pressao1*40.0/1023.0
		except:
			psi1=20.0
			print('Sensor Psi1 nao responde')
			print('valorpsi1=20.0 recebe valor padrao')	
		return psi1

def leitura_pot3():	#sensor_pressao2
    #sensor_pressao2= pinos.analogRead(pino_pot3)
		try:
			rs232.write('3')
			sensor_pressao2=int(rs232.read(4))
			psi2 = sensor_pressao2*40.0/1023.0
		except:
			psi2=20.0
			print('Sensor Psi2 nao responde')
			print('valorpsi2=20.0 recebe valor padrao')	
		return psi2

def liga_rele1():
    pinos.digitalWrite(pino_rele1, 1)

def desliga_rele1():
    pinos.digitalWrite(pino_rele1, 0)

def liga_rele2():
	pinos.digitalWrite(pino_rele2,1)

def desliga_rele2():
	pinos.digitalWrite(pino_rele2,0)

'''
def move_servo(posicao):
    sg_servo.setAngle(posicao)
    angulo = posicao
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.write("Servo: {}".format(angulo))

def escreve_lcd(texto_linha1, texto_linha2):
    lcd.clear()
    lcd.setCursor(0, 0)
    lcd.write(texto_linha1)
    lcd.setCursor(1, 0)
    lcd.write(texto_linha2)
'''

def horarios_txt(texto):
	#lcd.setCursor(1, 0)
	#lcd.write("gravando arquivo")
	arq = open('horarios.txt', 'w')
	arq.write(str(texto))
	print 'texto = ', texto
	#lcd.write("-----Gravado----")
	arq.close()

def carrega_horarios():
	with open('horarios.txt', 'r') as arq_horarios:
		le_horarios = arq_horarios.readlines()
	dados_h = le_horarios[0];
	return jsonify(dados_h)
