# -*- coding: latin-1 -*-
import sqlite3
import datetime
import time
#import scipy

def cria_tabela_usuarios():
	db = sqlite3.connect('site.db')
	cursor = db.cursor()
	cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios
	(id INTEGER PRIMARY KEY,mail TEXT,senha TEXT,tipo INTEGER,ultimo_acesso TIMESTAMP DEFAULT (DATETIME('now')), acessos INTEGER DEFAULT 0)''')
	db.commit()
	db.close()

def incrementa_contador_usuario(chave_primaria):
	db = sqlite3.connect('site.db')
	cursor = db.cursor()
	cursor.execute('''UPDATE usuarios SET acessos = acessos + 1 WHERE id = ?''',(chave_primaria,))
	db.commit()
	db.close()
	if cursor.rowcount > 0:
		return True
	else:
		return False

def atualiza_acesso_usuario(chave_primaria):
	tempo  = datetime.datetime.now()
	db = sqlite3.connect('site.db')
	cursor = db.cursor()
	cursor.execute('''UPDATE usuarios SET ultimo_acesso = ? WHERE id = ?''',(tempo,chave_primaria,))
	db.commit()
	db.close()
	if cursor.rowcount > 0:
		return True
	else:
		return False

def adiciona_usuario(mail,senha,tipo):
	try:
		a, b, c = checa_usuario(mail)
		if (a < 1):
			db = sqlite3.connect('site.db')
			cursor = db.cursor()
			t_abs = datetime.datetime.now()
			cursor.execute('''INSERT INTO usuarios (mail,senha,tipo)
								VALUES(?,?,?)''',(mail,senha,tipo))
			db.commit()
			db.close()
			if cursor.rowcount > 0:
				return 1
			else:
				return 0
		else:
			return -1
	except:
		return 0

def checa_usuario(mail):
	try:
		db = sqlite3.connect('site.db')
		cursor = db.cursor()
		cursor.execute('''SELECT * FROM usuarios WHERE mail = ?''',(mail,))
		row = cursor.fetchone()
		db.close()
		if row:
			return row[0], row[2], row[3]
		else:
			return None, None, None
	except:
		return None, None, None

def lista_usuarios():
	try:
		db = sqlite3.connect('site.db')
		cursor = db.cursor()
		cursor.execute('''SELECT * FROM usuarios ''')
		rows = cursor.fetchall()
		db.close()
		return rows
	except:
		return None

def deleta_usuario(chave_primaria):
	try:
		db = sqlite3.connect('site.db')
		cursor = db.cursor()
		cursor.execute('''DELETE FROM usuarios WHERE id = ? ''', (chave_primaria,))
		db.commit()
		db.close()
		if cursor.rowcount > 0:
			return True
		else:
			return False
	except:
		return None
