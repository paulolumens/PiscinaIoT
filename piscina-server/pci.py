# -*- coding: latin-1 -*-

#Para galileo
#from configuraPCI import *
#from upm import pyupm_jhd1313m1 as LCD
#lcd = LCD.Jhd1313m1(0, 0x3E, 0x62)
#from sensores import *

#PARA USAR EM Raspberry
from configuraPCIrasp import *
from sensoresrasp import *


from time import gmtime, strftime, time
import sqlite3
from db_sqlite import *
from datetime import datetime

class Display_LCD(threading.Thread):
	def __init__(self,nome,valor):
		threading.Thread.__init__(self)
		self.executando = False
		self.nome = nome
		self.valor = valor
		celsius = sensor_temperatura()
		self.celsius = celsius
		self.old_celsius = old_celsius
		self.abrir_txt = abrir_txt
		self.horarios_txt = horarios_txt
		self.old_horarios_txt = old_horarios_txt.split(',')
		self.ano = ano
		self.mes = mes
		self.dia = dia
		self.semana = semana
		self.hora = hora
		self.minuto = minuto
		self.segundo = segundo
		self.flag_print = flag_print

	def run(self):
		self.executando = True
		while self.executando:


			if (self.segundo == 30) & (self.flag_print == 0):
				flag_print=1
				self.flag_print=flag_print
				celsius = sensor_temperatura()
				self.celsius = celsius
				celsius=( '{:.1f}'.format(self.celsius))
				horario=('Horas {}:{}:{}'.format(self.hora, self.minuto, self.segundo))
				escreve_lcd(horario, celsius)
				horaIni = self.old_horarios_txt[7].split(':')
				horaFin = self.old_horarios_txt[8].split(':')
				str_inicial = horaIni[0]+horaIni[1];
				str_final = horaFin[0]+horaFin[1];
				str_atual =('{:2d}{:2d}').format(hora,minuto);
				if self.old_celsius != celsius:
					old_celsius= celsius
					self.old_celsius = old_celsius
					adiciona_dado_temperatura(celsius)
					print'gravado novo dado temperatura'
				print celsius
				print horario
				print'str_inicial',str_inicial
				print'str_final',str_final
				print'str_atual',str_atual
				print '======================='
#================liga_rele1 se temperatura maoir que 27 graus============
				if self.celsius > 27:
					liga_rele1()
					print'rele1 ligado'
					print'temperatura= ', self.celsius
				else:
					desliga_rele1()
					print'rele1 desligado'
					print'temperatura= ', self.celsius
				semana_int = int(self.semana)
#=================liga_rele2 se horarios conferem =======================
				if (self.old_horarios_txt[semana_int]) == '1':
					if (str_atual >= str_inicial):
						if (str_atual < str_final):
							liga_rele2()
						else:
							desliga_rele2()
				else:
					desliga_rele2()
#=====================fim funcoes reles =================================
#==================== reseta fag ========================================
			if self.segundo == 0:
				flag_print=0
				self.flag_print=flag_print
#========================================================================
			if self.nome == "Temperatura":
				celsius = sensor_temperatura()
				self.celsius = celsius

			elif self.nome == "Horas":
					hoje_1 = strftime("%w,%d,%m,%Y,%H,%M,%S", gmtime())
					hoje_2 = hoje_1.split(',')
					date_now = datetime.today()
					ano = hoje_2[3]
					mes = hoje_2[2] = date_now.month
					dia = hoje_2[1] = date_now.day
					semana = hoje_2[0]
					hora = hoje_2[4] = date_now.hour
					minuto = hoje_2[5] = date_now.minute
					segundo = hoje_2[6] = date_now.second
					self.ano = ano
					self.mes = mes
					self.dia = dia
					self.semana = semana
					self.hora = hora
					self.minuto = minuto
					self.segundo = segundo
			elif self.nome == "abrir_arq":
				if self.abrir_txt == 0:
					with open('horarios.txt', 'r') as arq_horarios:
						le_horarios = arq_horarios.readlines()
					self.horarios_txt = le_horarios[0];
					self.old_horarios_txt = self.horarios_txt.split(',')
					self.abrir_txt = 1
					old_horarios_txt = self.old_horarios_txt
					print 'old ',self.old_horarios_txt
			else:
					print('\n Erro Display')
					lcd.clear()
					lcd.setCursor(0,0)
					lcd.write('Erro Diplay')
					time.sleep(500)


	def stop(self):
		self.executando = False


#===============================================================
def sensor_temperatura():
	celsius=leitura_temperatura()
	return celsius
#==============================================================
def pause():
	programPause = raw_input("Tecle <ENTER> para encerrar...")


def meu_main():
	celsius = sensor_temperatura()
	ver_temp = Display_LCD('Temperatura',celsius)
	ver_hora = Display_LCD('Horas',date_now)
	ver_txt = Display_LCD('abrir_arq', abrir_txt)
	ver_txt.start()
	ver_hora.start()
	ver_temp.start()


hoje_1 = strftime("%w,%d,%m,%Y,%H,%M,%S", gmtime())
hoje_2 = hoje_1.split(',')
date_now = datetime.today()
ano = hoje_2[3]
mes = hoje_2[2]
dia = hoje_2[1]
semana = hoje_2[0]
hora = hoje_2[4]
minuto = hoje_2[5]
segundo = hoje_2[6]
flag_print = 0
with open('horarios.txt', 'r') as arq_horarios:
	le_horarios = arq_horarios.readlines()
horarios_txt = le_horarios[0];
old_horarios_txt = horarios_txt
celsius = sensor_temperatura()
old_celsius = 0
print'inicio celsius', celsius
print 'datetime.today ', date_now
print'datetime.day ', date_now.day
print'datetime.hour ', date_now.hour
print'datetime.minute ', date_now.minute
print'datetime.second ', date_now.second
print'gmtime ', hoje_1
abrir_txt = 0

if __name__ == '__main__':
	meu_main()
