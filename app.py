from flask import Flask, render_template, request, redirect, url_for, g
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@apple2021'
app.config['MYSQL_DB'] = 'hospital_management'

mysql = MySQL(app)

@app.route('/')
def index():
    g.page = 'homepage'
    return render_template('index.html')

@app.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        admission_date = request.form['admission_date']
        checkup_details = request.form['checkup_details']
        prescriptions = request.form['prescriptions']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO patients1 (name, age, gender, address, admission_date, checkup_details, prescriptions) VALUES (%s, %s, %s, %s, %s, %s, %s)', 
                       (name, age, gender, address, admission_date, checkup_details, prescriptions))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('view_patients'))
    return render_template('add_patient.html')

@app.route('/view_patients', methods=['GET', 'POST'])
def view_patients():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = 'SELECT * FROM patients1 WHERE 1=1'
    filters = []

    if request.method == 'POST':
        search_term = request.form.get('search_term')
        filter_gender = request.form.get('filter_gender')
        filter_admission_date = request.form.get('filter_admission_date')

        if search_term:
            try:
                # Check if search_term is an integer (patient ID)
                search_term_int = int(search_term)
                query += ' AND id = %s'
                filters.append(search_term_int)
            except ValueError:
                # If not an integer, treat it as a string (name)
                query += ' AND name LIKE %s'
                filters.append(f'%{search_term}%')

        if filter_admission_date:
            query += ' AND admission_date = %s'
            filters.append(filter_admission_date)

        if filter_gender:
            query += ' AND gender = %s'
            filters.append(filter_gender)

    cursor.execute(query, filters)
    patients = cursor.fetchall()
    
    for patient in patients:
        cursor.execute('SELECT * FROM lab_data WHERE patient_id = %s', (patient['id'],))
        patient['lab_data'] = cursor.fetchall()
        
        cursor.execute('SELECT * FROM billing WHERE patient_id = %s', (patient['id'],))
        patient['billing'] = cursor.fetchall()
    
    cursor.close()
    return render_template('view_patients.html', patients=patients)



@app.route('/update_patient/<int:id>', methods=['GET', 'POST'])
def update_patient(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        admission_date = request.form['admission_date']
        checkup_details = request.form['checkup_details']
        prescriptions = request.form['prescriptions']
        
        cursor.execute('UPDATE patients1 SET name=%s, age=%s, gender=%s, address=%s, admission_date=%s, checkup_details=%s, prescriptions=%s WHERE id=%s', 
                       (name, age, gender, address, admission_date, checkup_details, prescriptions, id))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('view_patients'))
    else:
        cursor.execute('SELECT * FROM patients1 WHERE id=%s', (id,))
        patient = cursor.fetchone()
        cursor.close()
        return render_template('update_patient.html', patient=patient)

@app.route('/delete_patient/<int:id>', methods=['POST'])
def delete_patient(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('DELETE FROM patients1 WHERE id=%s', (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('view_patients'))

@app.route('/add_lab_data', methods=['GET', 'POST'])
def add_lab_data():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        test_name = request.form['test_name']
        result = request.form['result']
        date = request.form['date']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO lab_data (patient_id, test_name, result, date) VALUES (%s, %s, %s, %s)', (patient_id, test_name, result, date))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('view_patients'))
    return render_template('add_lab_data.html')

@app.route('/billing', methods=['GET', 'POST'])
def billing():
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        amount = request.form['amount']
        date = request.form['date']
        
        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO billing (patient_id, amount, date) VALUES (%s, %s, %s)', (patient_id, amount, date))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('view_patients'))
    return render_template('billing.html')

@app.route('/update_lab_data/<int:id>', methods=['GET', 'POST'])
def update_lab_data(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        test_name = request.form['test_name']
        result = request.form['result']
        date = request.form['date']
        
        cursor.execute('UPDATE lab_data SET test_name=%s, result=%s, date=%s WHERE id=%s', (test_name, result, date, id))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('view_patients'))
    else:
        cursor.execute('SELECT * FROM lab_data WHERE id=%s', (id,))
        lab_data = cursor.fetchone()
        cursor.close()
        return render_template('update_lab_data.html', lab_data=lab_data)

@app.route('/update_billing/<int:id>', methods=['GET', 'POST'])
def update_billing(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        amount = request.form['amount']
        date = request.form['date']
        
        cursor.execute('UPDATE billing SET amount=%s, date=%s WHERE id=%s', (amount, date, id))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('view_patients'))
    else:
        cursor.execute('SELECT * FROM billing WHERE id=%s', (id,))
        billing = cursor.fetchone()
        cursor.close()
        return render_template('update_billing.html', billing=billing)

@app.route('/delete_lab_data/<int:id>', methods=['POST'])
def delete_lab_data(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM lab_data WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('view_patients'))

@app.route('/delete_billing/<int:id>', methods=['POST'])
def delete_billing(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM billing WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    return redirect(url_for('view_patients'))


if __name__ == '__main__':
    app.run(debug=True)
