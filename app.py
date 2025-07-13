from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret_key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/home')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    conn = get_db_connection()
    cars = conn.execute('SELECT * FROM cars').fetchall()
    conn.close()
    return render_template('home.html', cars=cars)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add', methods=['GET', 'POST'])
def add_car():
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        conn = get_db_connection()
        conn.execute('INSERT INTO cars (brand, model) VALUES (?, ?)', (brand, model))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    return render_template('add_car.html')

@app.route('/edit/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    conn = get_db_connection()
    car = conn.execute('SELECT * FROM cars WHERE id = ?', (car_id,)).fetchone()
    if request.method == 'POST':
        brand = request.form['brand']
        model = request.form['model']
        conn.execute('UPDATE cars SET brand = ?, model = ? WHERE id = ?', (brand, model, car_id))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))
    conn.close()
    return render_template('edit_car.html', car=car)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)

