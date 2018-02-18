# -*- coding: latin-1 -*-
from __future__ import division
from flask import Flask, render_template, jsonify
from datetime import datetime
from time import time
import urllib2, json

#configuração da comm serial no rasp
import serial
rs232 = serial.Serial(
    port='/dev/ttyS0',
    baudrate = 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=3.0)

import threading

#configuração dos pinos para Raspberry
import wiringpi as GPIO
pinos = GPIO
pinos.wiringPiSetup() # configura como pinos do Wiringpi

from openweather import openweather
with open('config.txt') as json_data:
    config = json.load(json_data)
piracicaba = openweather(config['api_key'], '3453643')
#configuração do LCD  e servo- para Galileo
'''
from upm import pyupm_jhd1313m1 as LCD
lcd = LCD.Jhd1313m1(0, 0x3E, 0x62)
from upm import pyupm_servo as servo
from upm import pyupm_temperature as upm
'''
pino_sensor_temperatura = 0
pino_rele1 =7
pino_servo = 5
pino_rele2 = 0
#pino_pot = 15
#pino_pot2 = 16
#pino_pot3 = 17

pinos.pinMode(pino_rele1, 1)
#pinos.pinMode(pino_pot, pinos.ANALOG_INPUT)
#pinos.pinMode(pino_pot2, pinos.ANALOG_INPUT)
#pinos.pinMode(pino_pot3, pinos.ANALOG_INPUT)
pinos.pinMode(pino_servo, 2)
pinos.pinMode(pino_rele2, 1)
#temperatura = upm.Temperature(pino_sensor_temperatura)
#sg_servo = servo.ES08A(pino_servo)
#pot = pinos.digitalRead(pino_pot)
#pot2 = pinos.digitalRead(pino_pot2)
#pot3 = pinos.digitalRead(pino_pot3)
