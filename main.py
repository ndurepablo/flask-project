from ast import Not
from flask import Flask, flash, redirect, url_for, render_template, request
from datetime import datetime
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'super_secret_key'

# db connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'proyecto_flask'

mysql = MySQL(app)



# context processor
@app.context_processor
def date_now():
    return {'now': datetime.utcnow()}
    

@app.route('/')
def index():
    saludo = 'Estamos saludando'
    edad = 18
    personas = ['Juan', 'Pedro', 'Maria']
    return render_template('index.html', saludar = saludo, edad=edad, personas=personas)

@app.route('/info')
@app.route('/info/<string:nombre>')
@app.route('/info/<string:nombre>/<int:edad>')
def info(nombre = None, edad = None):
    texto = 'No hay nombre ni edad'
    if nombre != None and edad != None:
        texto = f"{nombre} tiene {edad} años"
    return render_template('info.html', text = texto)

@app.route('/contact')
@app.route('/contact/<redirection>')
def contact(redirection = None):
    if redirection is not None:
        return redirect(url_for('index'))
    
    return render_template('contact.html')

@app.route('/languages')
def languages():
    return render_template('languages.html', languages='Python')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/create-car', methods=['GET', 'POST'])
def create_car():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']
        
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO coches VALUES(NULL, %s, %s, %s, %s)", (marca, modelo, precio, ciudad))
        cursor.connection.commit()
        
        flash('Auto creado correctamente')

        return redirect(url_for('cars'))
    return render_template('create_car.html')

@app.route('/cars')
def cars():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM coches ORDER BY id DESC')
    coches = cursor.fetchall()
    cursor.close()
    return render_template('cars.html', coches=coches)

@app.route('/cars/<car_id>')
def car(car_id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM coches WHERE id = %s', (car_id))
    coche = cursor.fetchall()
    cursor.close()
    return render_template('car.html', coche=coche[0])

@app.route('/delete-car/<car_id>')
def delete_car(car_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM coches WHERE id = %s', (car_id))
    mysql.connection.commit()
    
    flash('Auto eliminado correctamente')

    return redirect(url_for('cars'))

@app.route('/edit-car/<car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        precio = request.form['precio']
        ciudad = request.form['ciudad']
        
        cursor = mysql.connection.cursor()
        cursor.execute("""
                        UPDATE coches
                        SET marca = %s, modelo = %s, precio = %s, ciudad = %s
                        WHERE id = %s
                       """, 
                        (marca, modelo, precio, ciudad, car_id))
        cursor.connection.commit()
        
        flash('Auto Editado correctamente')

        return redirect(url_for('cars'))
    
    
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM coches WHERE id = %s', (car_id))
    coche = cursor.fetchall()
    cursor.close()
    return render_template('create_car.html', coche=coche[0])

if __name__ == '__main__':
    app.run(debug=True)