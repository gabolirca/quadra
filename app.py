from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Configuración de la aplicación y base de datos
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quadra.db'  # Base de datos SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Necesario para usar flash()
db = SQLAlchemy(app)

# Modelo de datos para los puestos de comida
class Puesto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(500), nullable=True)
    ubicacion = db.Column(db.String(200), nullable=False)

# Crear las tablas en la base de datos (si no existen)
with app.app_context():
    db.create_all()

# Ruta principal que muestra los puestos de comida
@app.route('/')
def home():
    puestos = Puesto.query.all()  # Obtiene todos los puestos de la base de datos
    return render_template('index.html', puestos=puestos)

# Ruta para agregar un nuevo puesto
@app.route('/agregar', methods=['GET', 'POST'])
def agregar_puesto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        ubicacion = request.form['ubicacion']
        
        if nombre and ubicacion:
            nuevo_puesto = Puesto(nombre=nombre, descripcion=descripcion, ubicacion=ubicacion)
            db.session.add(nuevo_puesto)
            db.session.commit()
            flash('Puesto agregado correctamente!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Por favor, complete todos los campos obligatorios.', 'danger')
    
    return render_template('agregar_puesto.html')

if __name__ == '__main__':
    app.run(debug=True)
