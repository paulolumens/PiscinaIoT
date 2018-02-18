# -*- coding: latin-1 -*-
from configuraPCI import *
def leitura_temperatura():
	temperatura = upm.Temperature(pino_sensor_temperatura)
	celsius = temperatura.value()
	#return temperatura.value()
	return celsius

def leitura_pot():	#sensor_phmetro
	sensor_phmetro = pinos.analogRead(pino_pot)
	ph = sensor_phmetro*14.0/1023.0
	return ph

def leitura_pot2():	#sensor_pressao1
	sensor_pressao1= pinos.analogRead(pino_pot2)
	psi1 = sensor_pressao1*40.0/1023.0
	return psi1	

def leitura_pot3():	#sensor_pressao2
	sensor_pressao2= pinos.analogRead(pino_pot3)
	psi2 = sensor_pressao2*40.0/1023.0
	return psi2	

def liga_rele1():
	pinos.digitalWrite(pino_rele1,pinos.HIGH)

def desliga_rele1():
	pinos.digitalWrite(pino_rele1,pinos.LOW)

def liga_rele2():
	pinos.digitalWrite(pino_rele2, pinos.HIGH)

def desliga_rele2():
	pinos.digitalWrite(pino_rele2, pinos.LOW)

def move_servo(posicao):
	angulo =(posicao)
	sg_servo.setAngle(angulo)	
	
def escreve_lcd(texto_linha1, texto_linha2):
	lcd.clear()
	lcd.setCursor(0, 0)
	lcd.write(texto_linha1)
	lcd.setCursor(1, 0)
	lcd.write(texto_linha2)

def horarios_txt(texto):
	arq = open('horarios.txt', 'w')
	arq.write(str(texto))
	#print 'horarios.txt= ', texto
	#lcd.write("-----Gravado----")
	arq.close()
	
def carrega_horarios():
	with open('horarios.txt', 'r') as arq_horarios:
		le_horarios = arq_horarios.readlines()
	dados_h = le_horarios[0];
	return jsonify(dados_h)