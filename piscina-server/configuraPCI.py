# -*- coding: latin-1 -*-
from __future__ import division
from flask import Flask, render_template, jsonify
from datetime import datetime
from time import time
import urllib2, json
from wiringx86 import GPIOGalileo as GPIO
pinos = GPIO(debug=False)
from openweather import openweather
with open('config.txt') as json_data:
	config = json.load(json_data)
piracicaba = openweather(config['api_key'], '3453643')
from upm import pyupm_jhd1313m1 as LCD
lcd = LCD.Jhd1313m1(0, 0x3E, 0x62)
from upm import pyupm_servo as servo
from upm import pyupm_temperature as upm
import threading

pino_sensor_temperatura = 0
pino_rele1 = 4
pino_servo = 5
pino_rele2 = 8
pino_pot = 15
pino_pot2 = 16
pino_pot3 = 17

pinos.pinMode(pino_rele1, pinos.OUTPUT)
pinos.pinMode(pino_rele2, pinos.OUTPUT)
pinos.pinMode(pino_pot, pinos.ANALOG_INPUT)
pinos.pinMode(pino_pot2, pinos.ANALOG_INPUT)
pinos.pinMode(pino_pot3, pinos.ANALOG_INPUT)
pinos.pinMode(pino_servo, pinos.PWM)
sg_servo = servo.ES08A(pino_servo)
pinos.digitalWrite(pino_rele1,pinos.LOW)
pinos.digitalWrite(pino_rele2,pinos.LOW)