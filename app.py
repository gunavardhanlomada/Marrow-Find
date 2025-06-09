import os
import numpy as np
import sqlite3
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.resnet50 import preprocess_input
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['OUTPUT_FOLDER'] = 'static/output'
app.config['DATABASE'] = 'database.db'

# Load the trained model
model = load_model('model/mymodel2.h5')

# Define class labels
class_labels = ['Benign', 'Pre', 'Pro', 'Early']

# Use LabelEncoder to ensure consistency in label encoding/decoding
label_encoder = LabelEncoder()
label_encoder.fit(class_labels)  # Fit encoder with the correct order of class names

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)
for category in class_labels:
    os.makedirs(os.path.join(app.config['OUTPUT_FOLDER'], category), exist_ok=True)

# Connect to the SQLite database
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        with connect_db() as db:
            cursor = db.cursor()
            try:
                cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
                db.commit()
                flash('Registration successful! Please login.', 'success')
                return redirect(url_for('index'))
            except sqlite3.IntegrityError:
                flash('Username already exists.', 'danger')
    return render_template('register.html')

# Login route
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute('SELECT id, password FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('index'))

# Dashboard route
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', username=session['username'])

# File upload and prediction route
@app.route('/upload', methods=['POST'])
def upload():
    if 'user_id' not in session:
        flash("Please log in first", "danger")
        return redirect(url_for('index'))

    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('dashboard'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('dashboard'))
    
    if file:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Load and preprocess the image
            img = load_img(filepath, target_size=(224, 224))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = preprocess_input(img_array)  # Ensure correct preprocessing

            # Make the prediction
            prediction = model.predict(img_array)
            predicted_class = np.argmax(prediction)

            # Decode the predicted label using LabelEncoder
            predicted_label = label_encoder.inverse_transform([predicted_class])[0]

            # DEBUG: Print prediction probabilities for analysis
            print(f"Prediction probabilities: {prediction}")
            print(f"Predicted label: {predicted_label}")
            
            # Save prediction history
            with connect_db() as db:
                cursor = db.cursor()
                cursor.execute('INSERT INTO history (user_id, filename, prediction, timestamp) VALUES (?, ?, ?, ?)',
                               (session['user_id'], filename, predicted_label, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                db.commit()

            flash(f'Prediction: {predicted_label}', 'success')
            return redirect(url_for('result', filename=filename, prediction=predicted_label))
        except Exception as e:
            flash(f"Error processing the image: {str(e)}", 'danger')
            return redirect(url_for('dashboard'))

# Result route
@app.route('/result')
def result():
    filename = request.args.get('filename')
    prediction = request.args.get('prediction')
    if not filename or not prediction:
        flash("Invalid result request.", 'danger')
        return redirect(url_for('dashboard'))
    
    return render_template('result.html', filename=filename, prediction=prediction)

# History route
@app.route('/history')
def history():
    if 'user_id' not in session:
        return redirect(url_for('index'))

    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT filename, prediction, timestamp FROM history WHERE user_id = ?", (session['user_id'],))
        history_records = cursor.fetchall()

    return render_template('history.html', history=history_records)

# About route
@app.route('/about')
def about():
    return render_template('about.html')

from flask import send_file

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

@app.route('/download_pdf')
def download_pdf():
    if 'user_id' not in session:
        flash("Please log in first", "danger")
        return redirect(url_for('index'))

    # Fetch the user's prediction history from the database
    with connect_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT filename, prediction, timestamp FROM history WHERE user_id = ?", (session['user_id'],))
        history_records = cursor.fetchall()

    # Path to save the generated PDF
    pdf_filename = f"history_report_{session['username']}.pdf"
    pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)

    # Create the PDF
    pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
    elements = []

    # Create table data for the PDF
    table_data = [['Filename', 'Prediction', 'Timestamp']]  # Header
    for record in history_records:
        table_data.append([record[0], record[1], record[2]])

    # Create a table for the PDF
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)

    # Build the PDF
    pdf.build(elements)

    # Send the file to the user for download
    return send_file(pdf_path, as_attachment=True, download_name=pdf_filename)


# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
