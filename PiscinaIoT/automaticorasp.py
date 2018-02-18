# -*- coding: latin-1 -*-
from db_sqlite import *
from datetime import datetime
import threading
from time import gmtime, strftime, sleep
from sensoresrasp import *

'''
from upm import pyupm_jhd1313m1 as LCD
lcd = LCD.Jhd1313m1(0, 0x3E, 0x62)
'''
hoje_1 = strftime("%w,%d,%m,%Y,%H,%M,%S", gmtime())
celsius = leitura_temperatura()
old_celsius = 0
old_valorpsi1 = 0
old_horarios_txt = 0
horarios_txt = 0
valorpsi2 = 0
texto2 = celsius
valorph = 0
old_valorph = 0


#================= funcao ler horarios ==================================================
def ver_horario():
	#hoje_1 = strftime("%w,%d,%m,%Y,%H,%M,%S", gmtime())
	hoje_2 = hoje_1.split(',')
	date_now = datetime.today()
	semana = hoje_2[0]
	ano = date_now.year
	mes = date_now.month
	dia = date_now.day
	hora = date_now.hour
	minuto = date_now.minute
	segundo = date_now.second
	lista_time=[semana,ano, mes, dia, hora, minuto, segundo]
	return lista_time

#===================== Thread PH ===============================================
class ph_sensor(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.executando = False
		self.valorph = valorph
		self.old_valorph = old_valorph

	def run(self):
		self.executando = True
		while self.executando:
			global valorph
			try:
				valorph = leitura_pot()
			except:
				valorph = 7.0
				print('Sensor Ph nao responde')
				print('valorph = 7.0 recebe valor padrao')
			self.valorph=('{:.1f}'.format(valorph))
			global texto2
			texto2 = ('{} PH'.format(self.valorph))
			valorph = ('{:.1f}'.format(valorph))
			if self.old_valorph != valorph:
				self.old_valorph = valorph
				adiciona_dado_ph(self.old_valorph)
			sleep(360)

	def stop(self):
		self.executando = False
#===================== Thread temperatura ===============================================
class temperatura_sensor(threading.Thread):

	def __init__(self):
		threading.Thread.__init__(self)
		self.executando = False
		self.old_celsius = old_celsius
		self.old_valorpsi1 = old_valorpsi1

	def run(self):
		self.executando = True
		while self.executando:
			try:
				celsius=leitura_temperatura()
			except:
				celsius=25.0
				print('Sensor Temperatura nao responde')
				print('celsius=25.0 recebe valor padrao')				
			with open('servicos.txt', 'r') as arq_servicos:
				le_servicos = arq_servicos.readlines();
			dados_servicos2 = le_servicos[0].split(',');
			motor1_int = int(dados_servicos2[1]);
			temperatura_int = int(dados_servicos2[3]);
			global texto2
			texto2 = ('{:.1f} graus'.format(celsius))
			celsius= ('{:.0f}'.format(celsius))
			celsius = int(celsius);
			#print 'celsius ',celsius;
			#print 'temperatura_int ',temperatura_int ;
			#print'soma ',(temperatura_int + celsius);
			if(motor1_int == 0):
				if (celsius > temperatura_int):
					liga_rele1()
					if self.old_celsius != celsius:
						self.old_celsius = celsius
						adiciona_dado_temperatura(celsius)
					try:	
						valorpsi1 = '{:.1f}'.format (leitura_pot2())
					except:
						valorpsi1=20.0
						print('Sensor Psi1 nao responde')
						print('valorpsi1=20.0 recebe valor padrao')						
					if self.old_valorpsi1 != valorpsi1:
						self.old_valorpsi1 = valorpsi1
						adiciona_dado_motor1(valorpsi1)
				else:
					desliga_rele1()
			else:
				liga_rele1()

			sleep(60)

	def stop(self):
		self.executando = False

#============================= Thread horarios ==========================================
class horarioAuto(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self.executando = False
		self.horarios_txt = horarios_txt
		self.old_horarios_txt = old_horarios_txt
		self.valorpsi2 = valorpsi2

	def run(self):
		self.executando = True
		while self.executando:
#====================  abrir arquivo txt =================================
			with open('horarios.txt', 'r') as arq_horarios:
				le_horarios = arq_horarios.readlines()
				self.horarios_txt = le_horarios[0];
				self.old_horarios_txt = self.horarios_txt.split(',')
				horaIni = self.old_horarios_txt[7].split(':')
				horaFin = self.old_horarios_txt[8].split(':')
				str_inicial = horaIni[0]+horaIni[1];
				str_final = horaFin[0]+horaFin[1];
#========================= funcao horario ==============================
			semana,ano, mes, dia, hora, minuto, segundo = ver_horario()
			if (dia < 10):
				dia = '0{}'.format(dia)
			if (mes < 10):
				mes = '0{}'.format(mes)
			if (hora < 10):
				hora = '0{}'.format(hora)
			if (minuto < 10):
				minuto = '0{}'.format(minuto)
			texto1 ='{}/{}/{}/{}:{}'.format( dia, mes, ano, hora, minuto)
			str_atual ='{}{}'.format(hora,minuto)

#======================trata servicos========================================
			with open('servicos.txt', 'r') as arq_servicos:
				le_servicos = arq_servicos.readlines();
			dados_servicos = le_servicos[0].split(',');
			retrolavagem_int = int(dados_servicos[0]);
			motor1_int = int(dados_servicos[1]);
			motor2_int = int(dados_servicos[2]);
			temperatura_int = int(dados_servicos[3]);
			#print 'retrolavagem_int ',retrolavagem_int;
			#print 'motor1_int ',motor1_int;
			#print 'motor2_int ',motor2_int;
			#print 'temperatura_int ',temperatura_int;

			if(retrolavagem_int == 0):
#=================liga_rele2 se horarios conferem =======================
				semana_int = int(semana)
				if (self.old_horarios_txt[semana_int]) == '1':
					if (str_atual >= str_inicial):
						if (str_atual < str_final):
							liga_rele2()
							try:
								valorpsi2 = ('{:.1f}'.format (leitura_pot3()))
							except:
								valorpsi2=20.0
								print('Sensor Psi2 nao responde')
								print('valorpsi2=20.0 recebe valor padrao')									
							if self.valorpsi2 != valorpsi2:
								self.valorpsi2 = valorpsi2
								adiciona_dado_motor2(self.valorpsi2)
						else:
							desliga_rele2()
				else:
					desliga_rele2()
#=====================fim funcoes reles =================================
			else:
				if(motor2_int == 1):
					liga_rele2()
				else:
					desliga_rele2()

			sleep(60)
			#escreve_lcd(texto1, texto2)

	def stop(self):
		self.executando = False

#============ inicia o programa =========================================================
def main_automatico():
	Ph_sensor = ph_sensor()
	Ph_sensor.start()
	Temperatura_sensor = temperatura_sensor()
	Temperatura_sensor.start()
	HorarioAuto = horarioAuto()
	HorarioAuto.start()
