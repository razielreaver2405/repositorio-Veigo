
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'shadou240590'
app.config['MYSQL_DB'] = 'product'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos ORDER BY id DESC")
    productos = cur.fetchall()
    cur.close()
    return render_template('index.html', productos=productos)

@app.route('/agregar', methods=['POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        precio = request.form['precio']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO productos (nombre, precio) VALUES (%s, %s)", (nombre, precio))
        mysql.connection.commit()
        flash('Producto agregado exitosamente')
        return redirect(url_for('index'))

@app.route('/eliminar/<int:id>')
def eliminar(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE id = %s", (id,))
    mysql.connection.commit()
    flash('Producto eliminado')
    return redirect(url_for('index'))

@app.route('/editar/<int:id>', methods=['POST'])
def editar(id):
    nombre = request.form['nombre']
    precio = request.form['precio']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE productos SET nombre = %s, precio = %s WHERE id = %s", (nombre, precio, id))
    mysql.connection.commit()
    flash('Producto actualizado')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
