# -*- coding: latin-1 -*-
from __future__ import division
import time
import threading
import sensores
import sqlite3
import datetime
from db_sqlite import *

#================ Criar objeto display =====================
class Display_LCD(threading.Thread):
    def __init__(self,nome,valor):
        threading.Thread.__init__(self)
        self.gravatemp = False
        self.executando = False
        self.habilitabomba1 = False
        self.habilitamotor2 = False
        self.temp1=0
        self.nome = nome
        self.valor = valor

    def run(self):
        self.executando = True
        while self.executando:
            if self.nome == "Temperatura":
                self.valor=sensores.leitura_temperatura()
                valortemp=('{:03.2f}'.format(self.valor))
                print 'valortemp',valortemp
                if self.gravatemp==False:
                    adiciona_dado_temperatura(valortemp)
                    self.gravatemp=True
                    valortemp1=valortemp
                    print 'valortemp salvo',valortemp
                if valortemp1!=valortemp:
                    adiciona_dado_temperatura(valortemp)
                    valortemp1=valortemp
                    print 'novo valortemp salvo ',valortemp
                else:
                    print 'mesmo valortemp'
                time.sleep(1)

            elif self.nome == "ph":
                self.valor=sensores.leitura_pot()
                valorph=('{:03.2f}'.format(self.valor))
                print 'valorph',valorph
                obj = datetime.datetime.now()
                hora = datetime.datetime.strftime(obj, "%H:%M:%S")
                if hora == "22:10:00" or hora=="22:25:00" or hora=="22:30:00":
                    adiciona_dado_ph(valorph)
                    print 'valorph salvo',valorph
                time.sleep(10)
            elif self.nome == "motor1":
                self.valor=sensores.leitura_pot2()
                valormotor1=('{:03.2f}'.format(self.valor))
                self.temp1=sensores.leitura_temperatura()
                #valortemperatura1=('{:03.2f}'.format(self.temp1))
                print 'valormotor1',valormotor1
                if self.temp1>27.00 and self.habilitabomba1==False:
                    sensores.liga_rele1()
                    print 'motor1 ligado'
                    if self.habilitabomba1==False:
                        adiciona_dado_motor1(valormotor1)
                        self.habilitabomba1=True
                    valormotoraquecedor=valormotor1
                    print 'valormotor1 salvo',valormotor1
                else:
                    print 'valormotor1 < 27'
                if self.habilitabomba1==True:
                    if valormotoraquecedor!=valormotor1:
                        adiciona_dado_motor1(valormotor1)
                        valormotoraquecedor=valormotor1
                        print 'novo valormotor1 salvo',valormotor1

                if self.temp1<25.00 and self.habilitabomba1==True:
                    sensores.desliga_rele1()
                    self.habilitabomba1=False
                    print 'motor1 desligado'
                time.sleep(5)
            elif self.nome =="motor2":
                atualmotor2 = sensores.liga_rele2()
                print 'atualmotor2',atualmotor2
                self.valor=sensores.leitura_pot3()
                valormotor2=('{:03.2f}'.format(self.valor))
                print 'valormotor2',valormotor2
                if atualmotor2==1 and self.habilitamotor2==False:
                    adiciona_dado_motor2(valormotor2)
                    valormotorfiltro=valormotor2
                    self.habilitamotor2=True
                    print 'valormotor2 salvo', valormotor2
                if self.habilitamotor2==True:
                    if valormotorfiltro!=valormotor2:
                        adiciona_dado_motor2(valormotor2)
                        print 'novo valormotor2 salvo',valormotor2
                if atualmotor2==0:
                    self.habilitamotor2=False
                time.sleep(5)
            else:
                break
                #print('\n Erro de leitura dos sensores')

    def stop(self):
        self.executando = False
        print 'fim'
                        #===========================================================

def meu_main2():
    ver_temp = Display_LCD('Temperatura',sensores.leitura_temperatura())
    ver_ph = Display_LCD('ph',sensores.leitura_pot)
    ver_motor1 = Display_LCD('motor1',sensores.leitura_pot2)
    #ver_motor2 = Display_LCD('motor2',sensores.leitura_pot3)
    #ver_stop = Display_LCD('stop', 0)
    ver_ph.start()
    ver_temp.start()
    ver_motor1.start()
    #ver_motor2.start()
    #ver_stop.start()
