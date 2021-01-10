#
from flask import Flask, render_template, request, redirect, url_for, flash
#important pip install flask-mysqldb, IMPORT 'MySQL'
from flask_mysqldb import MySQL

app = Flask(__name__)
#MySQL connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] =	'jonathanperez'
app.config['MYSQL_PASSWORD'] = 'CARA DE PESCAR CARPAS'
app.config['MYSQL_DB'] = 'first_database'
mysql = MySQL(app)
#setting/configuración necesaria como seguridad
app.secret_key = 'mysecretkey'


@app.route('/')
def Home():
	cur = mysql.connection.cursor()
	cur.execute('SELECT * FROM contacts')
	data = cur.fetchall()
	return render_template('table.html', contacts = data )


@app.route('/add_contact', methods=['POST'])
def add_contact():	
	if request.method == 'POST':
		fullname = request.form['fullname']
		email = request.form['email']
		phone = request.form['phone']

		#ESTA PARTE ES IMPORTANTE PARA CONECTAR MySQL!!!!!!!!!
		cur = mysql.connection.cursor()
		cur.execute('INSERT INTO contacts (fullname, email, phone) VALUES(%s,%s,%s)',
		(fullname, phone, email))
		mysql.connection.commit()
		flash('Contact Added Successfully')
		
		""" PARA IMPRIMIR POR CONSOLA
		ejemplo:
		print(fullname)
		print(email)
		print(phone)"""
		return redirect(url_for('Home'))

	#HASTA ACÁ FUNCIONA PERFECTO	
#ESTE HAY QUE ENTENDERLO BIEN, ES EL MÁS DIFÍCIL 
#ESTUDIAR LAS SENTENCIAS SQL
@app.route('/edit/<id>')
def get_contact(id):
	cur = mysql.connection.cursor()
	#acá solucione el problema cambiando los parentesís del id por [] AVERIGUAR PQ!!
	cur.execute('SELECT * FROM contacts WHERE id = %s', [id])
	data = cur.fetchall()
	print(data[0])
	return render_template('edit-contact.html', contact= data[0])
#EDIT:Esta ruta se tiene que hacer para poder cambiar los datos que se necesitán modificar. 
@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
	if request.method == 'POST':
		fullname = request.form['fullname']
		email = request.form['email']
		phone = request.form['phone'] 
		cur = mysql.connection.cursor()
		cur.execute('''
			UPDATE contacts
			SET fullname=%s,
			 	email=%s,
			 	phone=%s
		 	WHERE id = %s''',(fullname, email, phone,id))
		mysql.connection.commit()
		flash('Contact Update Successfully')
		return redirect(url_for('Home'))


#DELETE IMPORTANT!
@app.route('/delete/<string:id>')
def delete_contact(id):	
	cur = mysql.connection.cursor()
	cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
	mysql.connection.commit()
	flash('Contact Removed Successfully')
	return  redirect(url_for('Home'))


if __name__ == '__main__':	
	app.run(port = 8000, debug = True)