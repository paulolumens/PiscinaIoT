# -*- coding: latin-1 -*-
import db_sqlite
import site_db
from flask import Flask, render_template, request, url_for, flash, redirect, session,jsonify
from functools import wraps
from passlib.hash import sha256_crypt
import sqlite3
import datetime
import time
import sys
import os
import platform
processador= platform.machine()
print 'Tipo do Processador:',processador
identificacao = os.uname()
print ('Identificacao'),identificacao
reload(sys)
sys.setdefaultencoding('utf-8')
modelo = identificacao[1]
print 'Plataforma= ', modelo


if modelo == 'galileo':
	#PARA USAR EM GALILEO GEN1
	from configuraPCI import *
	from sensores import *
	from automatico import main_automatico
	#from pcisensores import meu_main2
	lcd.setCursor(0, 0)
	lcd.write("Galileo---IoT---")
	lcd.setCursor(1, 0)
	lcd.write("AutomacaoPiscina")
	texto1=""
	texto2=""
	print ('Rodando na Galileo GEN1')
elif modelo == 'galileogen2':
	#PARA USAR EM GALILEO GEN1
	from configuraPCI import *
	from sensores import *
	from automatico import main_automatico
	#from pcisensores import meu_main2
	lcd.setCursor(0, 0)
	lcd.write("Galileo---IoT---")
	lcd.setCursor(1, 0)
	lcd.write("AutomacaoPiscina")
	texto1=""
	texto2=""
	print ('Rodando na Galileo GEN2')		
elif modelo == 'raspberrypi':
	#PARA USAR EM Raspberry
	from configuraPCIrasp import *
	from sensoresrasp import *
	from automaticorasp import main_automatico
	print ('Rodando na Raspberry Pi3')

	

try:
	lcd.setCursor(0, 0)
	lcd.write("Galileo---IoT---")
	lcd.setCursor(1, 0)
	lcd.write("AutomacaoPiscina")
except:
	print('Sem Display LCD')
texto1=""
texto2=""
dados_sensores = [ "", "", "", ""]
horarios_var=[]



app = Flask(__name__)
#=============================Autenticacao==================================
app.secret_key = 'piscinaiotkey'
def admin_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if session['level'] == 2:
			return test(*args, **kwargs)
		else:
			flash('You need to be admin to enter here !')
			return redirect(url_for('loggin'))
	return wrap

def loggin_required(test):
	@wraps(test)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return test(*args, **kwargs)
		else:
			flash('You need to loggin first !')
			return redirect(url_for('loggin'))
	return wrap

@app.route('/loggin', methods=['GET','POST'])
def loggin():
	if 'logged_in' in session:
		return redirect(url_for('logout'))

	if request.method == 'POST':
		print ('entrou com metodo POST')

		try:
			email = request.form['email']
			senha = request.form['senha']
			nome =  email[:email.index('@')]
			print ('pegou email e senha')
			chave, senha_hash, level = site_db.checa_usuario(email)
			print ('checou usuario')
			if sha256_crypt.verify(senha,senha_hash):
				site_db.atualiza_acesso_usuario(chave)
				site_db.incrementa_contador_usuario(chave)
				print ('verificou crypto')
				if int(level) == 2:
					session['name'] = nome
					session['logged_in'] = True
					session['level'] = 2
					flash('loggin ok - Admin: ' + nome)
					print ('logou user admin')
					return redirect(url_for('home'))
				elif int(level) == 1:
					session['logged_in'] = True
					session['name'] = nome
					session['level'] = 1
					flash('loggin ok - User:' + nome)
					print ('logou user comum')
					return redirect(url_for('home'))
				else:
					flash('error in loggin !')
					return redirect(url_for('loggin'))
			else:
				flash('Senha ou usuario incorreto !')
				return redirect(url_for('loggin'))
		except:
			flash('error in loggin !')
			return redirect(url_for('loggin'))    # adicionado o return -- testar
	return render_template('loggin.html')


@app.route('/logout')
@loggin_required
def logout():
	session.pop('logged_in',None)
	session.pop('name',None)
	session.pop('level',None)
	flash('you are logged out !')
	return redirect(url_for('home'))


@app.route('/admin', methods=['GET','POST'])
@loggin_required
@admin_required
def admin():
	if request.method == 'POST':
		if request.form['submit'] == 'novousuario':
			#senha_hash = sha256_crypt.encrypt(request.form['senha'])
			senha_hash = sha256_crypt.encrypt(request.form['senha'])
			if 'admin' in request.form:
				a = site_db.adiciona_usuario(request.form['usuario'],senha_hash,2)
				if a == 1:
					flash('Admin Adicionado')
				elif a == 0:
					flash('Erro ao adicionar ao banco de dados')
				else:
					flash('Usuario já existe')
			else:
				a = site_db.adiciona_usuario(request.form['usuario'], senha_hash,1)
				if a == 1:
					flash('Admin Adicionado')
				elif a == 0:
					flash('Erro ao adicionar ao banco de dados')
				else:
					flash('Usuario já existe')
			return redirect(url_for('admin'))
		elif int(request.form['submit']) > 0:
			try:
				if(site_db.deleta_usuario(int(request.form['submit']))):
					flash('Usuario removido')
				else:
					flash('Erro ao remover usuario')
			except:
				flash('Erro ao remover usuario')
				pass
			return redirect(url_for('admin'))
		flash('Erro ao remover/adicionar usuario')
		return redirect(url_for('admin'))
	else:
		print 'admin', request.path
		users = site_db.lista_usuarios()
		return render_template('admin.html',users=users)

@app.route('/usuario',methods=['GET','POST'])
@loggin_required
def usuario():
	return render_template('usuario.html')
#==============================================================================
@app.route("/")
def index():
	return render_template("home.html")

@app.route("/home")
def home():
	return render_template("home.html")

@app.route("/botoes")
def botoes():
	return render_template("botoes.html")

@app.route("/sensores")
def sensores():   
	celsius=("{:.1f}".format(leitura_temperatura()))
	leitura_pot()
	ph = ("{:.1f}".format(leitura_pot()))
	leitura_pot2()
	psi1 = ("{:.1f}".format(leitura_pot2()))
	leitura_pot3()
	psi2 = ("{:.1f}".format(leitura_pot3()))
	valores1 = [celsius,ph,psi1,psi2]
	lista1 = ["Temperatura", "PH", "psi", "psi"]
	#texto1 = ("Temp: {}      ".format(celsius))
	#texto2=("pH: {}      ".format(ph))
	#escreve_lcd(texto1, texto2)
	return render_template("sensores.html", valores1=valores1, lista1=lista1)

@app.route("/sensores2")
def sensores2():   
	celsius=("{:.1f}".format(leitura_temperatura()))
	leitura_pot()
	ph = ("{:.1f}".format(leitura_pot()))
	leitura_pot2()
	psi1 = ("{:.1f}".format(leitura_pot2()))
	leitura_pot3()
	psi2 = ("{:.1f}".format(leitura_pot3()))
	valores1 = [celsius,ph,psi1,psi2]
	lista1 = ["Temperatura", "PH", "psi", "psi"]
	#texto1 = ("Temp: {}      ".format(celsius))
	#texto2=("pH: {}      ".format(ph))
	#escreve_lcd(texto1, texto2)
	return render_template("sensores2.html", valores1=valores1, lista1=lista1)	

@app.route("/web")
def web():
	try:
		temperatura_opw = piracicaba.temperatura()
		pressao_opw = piracicaba.pressao()
		humidade_opw = piracicaba.humidade()
		vento_opw = piracicaba.vento_speed()
		valores2 = [temperatura_opw, pressao_opw, humidade_opw, vento_opw]
		lista2 = ["Temperatura", "Pressao", "Humidade", "Ventos"]
		return render_template("web.html", valores2=valores2, lista2=lista2)
	except:
		print'Erro coneccao com a internet'
		temperatura_opw = 0
		pressao_opw = 0
		humidade_opw = 0
		vento_opw = 0
		valores2 = [temperatura_opw, pressao_opw, humidade_opw, vento_opw]
		lista2 = ["Temperatura", "Pressao", "Humidade", "Ventos"]
		return render_template("web.html", valores2=valores2, lista2=lista2)		

@app.route('/horarios')
@loggin_required
def horarios():
	with open('horarios.txt', 'r') as arq_horarios:
		le_horarios = arq_horarios.readlines()
	le_horarios = le_horarios[0].split(',')

	return render_template("horarios.html", val_horarios=le_horarios)

@app.route('/carrega_horarios')
def carrega_horarios():
	with open('horarios.txt', 'r') as arq_horarios:
		le_horarios = arq_horarios.readlines()
	dados_h = le_horarios[0];
	return jsonify(dados_h)
	
@app.route('/carrega_servicos')
def carrega_servisos():
	with open('servicos.txt', 'r') as arq_servicos:
		le_servicos = arq_servicos.readlines()
	dados_servicos = le_servicos[0];
	return jsonify(dados_servicos)	

@app.route("/servicos")
def servicos():
	return render_template("servicos.html")

@app.route('/servicos2')
@loggin_required
def servicos2():
	with open('servicos.txt', 'r') as arq_servicos:
		le_servicos = arq_servicos.readlines()
	le_servicos = le_servicos[0].split(',')
	return render_template("servicos2.html", val_servicos=le_servicos)	
	
@app.route("/servo/<val_servo>")
def servo(val_servo):
	temp = int(val_servo)
	#print 'posicao= ', temp
	move_servo(temp)
		
	if (temp == 180):
		texto1=('Modo  Servico ')
		texto2=("Valvula Aberta ")
		escreve_lcd(texto1, texto2)
	#return render_template("servo2.html", temp=temp)
	return ('OK', 200)

@app.route("/rele1/<val_rele1>")
def rele1(val_rele1):
	status = int(val_rele1)
	
	if status == 1:
		liga_rele1()
		#texto2="M1 Ligado      "
		#escreve_lcd(texto1, texto2)
	else:
		desliga_rele1()
		#texto2 = "M1 Desligado   "
		#escreve_lcd(texto1, texto2)
	return ('OK', 200)

@app.route("/rele2/<val_rele2>")
def rele2(val_rele2):
	status = int(val_rele2)
	
	if status == 1:
		liga_rele2()
		#texto2="M2 Ligado     "
		#escreve_lcd(texto1, texto2)
	else:
		desliga_rele2()
		#texto2="M2 Desligado  "
		#escreve_lcd(texto1, texto2)
	return ('OK', 200)

@app.route('/graficos')
def graficos():
    temperatura_db = db_sqlite.retorna_dados_temperatura()
    ph_db = db_sqlite.retorna_dados_ph()
    psi1_db = db_sqlite.retorna_dados_motor1()
    psi2_db = db_sqlite.retorna_dados_motor2()
    return render_template('graficos.html',temperatura_db=temperatura_db,ph_db=ph_db,psi1_db=psi1_db,psi2_db=psi2_db)

@app.route('/zoonable')
def zoonable():
    temperatura_db = db_sqlite.retorna_dados_temperatura()
    ph_db = db_sqlite.retorna_dados_ph()
    psi1_db = db_sqlite.retorna_dados_motor1()
    psi2_db = db_sqlite.retorna_dados_motor2()
    return render_template('zoonable.html',temperatura_db=temperatura_db,ph_db=ph_db,psi1_db=psi1_db,psi2_db=psi2_db)	


@app.route('/update_potenciometro')
def update_potenciometro():
		dados_sensores[0] = ("{:.1f}".format(leitura_temperatura())) #temperatura
		dados_sensores[1] = ("{:.1f}".format(leitura_pot()))			#ph
		dados_sensores[2] = ("{:.1f}".format(leitura_pot2()))		#motor1
		dados_sensores[3] = ("{:.1f}".format(leitura_pot3()))		#motor2
		#texto1=("pH: {}      ".format(dados_sensores[1]))
		#texto2=("M1:{} psi   ".format(dados_sensores[2]))
		#escreve_lcd(texto1, texto2)
		return jsonify(dados_sensores)

@app.route('/update_horarios/<val_hora>')
def update_horarios(val_hora):
		horas = val_hora
		arq = open('horarios.txt', 'w')
		arq.write(str(horas))
		arq.close()
		return ('OK', 200)	

@app.route('/update_servicos/<servicos_var>')
def update_servicos(servicos_var):
		servicos = servicos_var
		arq = open('servicos.txt', 'w')
		arq.write(str(servicos))
		arq.close()
		return ('OK', 200)

		
if __name__ == "__main__":
	main_automatico()
	app.run(debug=True,host='0.0.0.0')