# -*- coding: latin-1 -*-
from configuraPCI import *
from sensores import *
import db_sqlite
#import pci
from automatico import main_automatico
#from pcisensores import meu_main2
lcd.setCursor(0, 0)
lcd.write("Galileo---IoT---")
lcd.setCursor(1, 0)
lcd.write("AutomacaoPiscina")
texto1=""
texto2=""
dados_sensores = [ "", "", "", ""]
horarios_var=[]
#print 'chama o programa= ',pci.__name__
#print'DIR= ', dir(automatico)
app = Flask(__name__)
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
	temperatura_opw = piracicaba.temperatura()
	pressao_opw = piracicaba.pressao()
	humidade_opw = piracicaba.humidade()
	vento_opw = piracicaba.vento_speed()
	valores2 = [temperatura_opw, pressao_opw, humidade_opw, vento_opw]
	lista2 = ["Temperatura", "Pressao", "Humidade", "Ventos"]
	return render_template("web.html", valores2=valores2, lista2=lista2)

@app.route('/horarios')
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

@app.route("/dash")
def dash():
    return render_template("dash.html")

@app.route("/navbar")
def navbar():
    return render_template("navbar.html")

@app.route("/cards")
def cards():
    return render_template("cards.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/forgot")
def forgot():
    return render_template("forgot-password.html")

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/google")
def google():
    return render_template("google.html")

	
if __name__ == "__main__":
	main_automatico()
	app.run(debug=True,host='0.0.0.0')