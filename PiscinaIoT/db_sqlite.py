# -*- coding: latin-1 -*-
import sqlite3
import datetime
import time
#import scipy

#funcoes para leitura e atualizacao do banco piscinaiot.db

def retorna_dados_temperatura(quantidade=None):
	conect = sqlite3.connect('piscinaiot.db')
	cursor = conect.cursor()
	if not quantidade:
		cursor.execute('''SELECT * FROM temperatura ORDER BY datetime(data) AND datetime(hora) ASC ''')
		#cursor.execute('''SELECT * FROM temperatura ORDER BY data AND hora ASC''')
	else:
		cursor.execute('''SELECT * FROM temperatura ORDER BY datetime(data) DESC LIMIT ?''',
			(quantidade,))
	return cursor.fetchall()

def retorna_dados_ph(quantidade=None):
	conect = sqlite3.connect('piscinaiot.db')
	cursor = conect.cursor()
	if not quantidade:
		cursor.execute('''SELECT * FROM ph ORDER BY datetime(data) AND datetime(hora) ASC''')
		#cursor.execute('''SELECT * FROM ph ORDER BY data AND hora ASC''')
	else:
		cursor.execute('''SELECT * FROM ph ORDER BY datetime(data) DESC LIMIT ?''',
			(quantidade,))
	return cursor.fetchall()

def retorna_dados_motor1(quantidade=None):
	conect = sqlite3.connect('piscinaiot.db')
	cursor = conect.cursor()
	if not quantidade:
		cursor.execute('''SELECT * FROM motor1 ORDER BY datetime(data) AND datetime(hora) ASC''')
		#cursor.execute('''SELECT * FROM motor1 ORDER BY data AND hora ASC''')
	else:
		cursor.execute('''SELECT * FROM motor1 ORDER BY datetime(data) DESC LIMIT ?''',
			(quantidade,))
	return cursor.fetchall()

def retorna_dados_motor2(quantidade=None):
	conect = sqlite3.connect('piscinaiot.db')
	cursor = conect.cursor()
	if not quantidade:
		cursor.execute('''SELECT * FROM motor2 ORDER BY datetime(data) AND datetime(hora) ASC''')
		#cursor.execute('''SELECT * FROM motor2 ORDER BY datetime(hora) AND data ASC''')
	else:
		cursor.execute('''SELECT * FROM motor2 ORDER BY datetime(data) DESC LIMIT ?''',
			(quantidade,))
	return cursor.fetchall()

def adiciona_dado_temperatura(valorTemp):
	try:
		conect     = sqlite3.connect('piscinaiot.db')
		cursor = conect.cursor()
		x = datetime.date.today()
		print x
		y = x.timetuple()
		print y
		z = list(y)
		print z
		data = datetime.date(z[0],z[1]-1,z[2])
		print data
		obj = datetime.datetime.now()
		hora = datetime.datetime.strftime(obj, "%H:%M:%S")
		cursor.execute('''INSERT INTO temperatura (valorTemp, data, hora)
							VALUES(?,?,?)''',(valorTemp, data, hora))
		conect.commit()
		conect.close()
		if cursor.rowcount > 0:
			return True
		else:
			return False
	except Exception as e:
		print ('excessao', e)
		return False

def adiciona_dado_ph(valorPh):
	try:
		conect     = sqlite3.connect('piscinaiot.db')
		cursor = conect.cursor()
		#data  = datetime.date.today()
		x = datetime.date.today()
		print x
		y = x.timetuple()
		print y
		z = list(y)
		print z
		data = datetime.date(z[0],z[1]-1,z[2])
		print data
		obj = datetime.datetime.now()
		hora = datetime.datetime.strftime(obj, "%H:%M:%S")
		cursor.execute('''INSERT INTO ph (valorPh, data, hora)
							VALUES(?,?,?)''',(valorPh, data, hora))
		conect.commit()
		conect.close()
		if cursor.rowcount > 0:
			return True
		else:
			return False
	except Exception as e:
		print e
		return False

def adiciona_dado_motor1(valorMotor1):
	try:
		conect     = sqlite3.connect('piscinaiot.db')
		cursor = conect.cursor()
		#data  = datetime.date.today()
		x = datetime.date.today()
		print x
		y = x.timetuple()
		print y
		z = list(y)
		print z
		data = datetime.date(z[0],z[1]-1,z[2])
		print data
		obj = datetime.datetime.now()
		hora = datetime.datetime.strftime(obj, "%H:%M:%S")
		cursor.execute('''INSERT INTO motor1 (valorMotor1, data, hora)
							VALUES(?,?,?)''',(valorMotor1, data, hora))
		conect.commit()
		conect.close()
		if cursor.rowcount > 0:
			return True
		else:
			return False
	except Exception as e:
		print e
		return False

def adiciona_dado_motor2(valorMotor2):
	try:
		conect     = sqlite3.connect('piscinaiot.db')
		cursor = conect.cursor()
		#data  = datetime.date.today()
		x = datetime.date.today()
		print x
		y = x.timetuple()
		print y
		z = list(y)
		print z
		data = datetime.date(z[0],z[1]-1,z[2])
		print data
		obj = datetime.datetime.now()
		hora = datetime.datetime.strftime(obj, "%H:%M:%S")
		cursor.execute('''INSERT INTO motor2 (valorMotor2, data, hora)
							VALUES(?,?,?)''',(valorMotor2, data, hora))
		conect.commit()
		conect.close()
		if cursor.rowcount > 0:
			return True
		else:
			return False
	except Exception as e:
		print e
		return False
