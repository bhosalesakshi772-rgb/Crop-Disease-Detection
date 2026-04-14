from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
import os
import tensorflow as tf
from tensorflow import keras
import numpy as np
from PIL import Image
import pickle
import mysql.connector
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load model and class names
MODEL_PATH = 'model/best_crop_disease_model.h5'
CLASS_NAMES_PATH = 'model/class_names.pkl'
try:
    print("Checking model path:", MODEL_PATH)
    print("Model exists:", os.path.exists(MODEL_PATH))

    print("Checking class file:", CLASS_NAMES_PATH)
    print("Class file exists:", os.path.exists(CLASS_NAMES_PATH))

    model = keras.models.load_model(MODEL_PATH)

    # ✅ manual class names (FIX)
    class_names = [
        'Apple___Apple_scab',
        'Apple___Black_rot',
        'Apple___Cedar_apple_rust',
        'Apple___healthy',
        'Blueberry___healthy',
        'Cherry_(including_sour)___Powdery_mildew',
        'Cherry_(including_sour)___healthy',
        'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot',
        'Corn_(maize)___Common_rust_',
        'Corn_(maize)___healthy'
    ]

    print("✅ Model loaded successfully")

except Exception as e:
    model = None
    class_names = []
    print("❌ Error loading model:", e)
# Database config
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'crop_disease_db'
}
def get_db_connection():
    return mysql.connector.connect(**db_config)

def preprocess_image(image):
    img = image.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def save_prediction(image_filename, disease, confidence):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO predictions (image_filename, disease, confidence) VALUES (%s, %s, %s)",
            (image_filename, disease, float(confidence))
        )
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Database error: {e}")

# Disease treatment suggestions
TREATMENT_SUGGESTIONS = {
    'healthy': 'Your plant is healthy! Continue good farming practices.',
    'leaf_spot': 'Apply copper-based fungicides. Remove affected leaves. Improve air circulation.',
    'rust': 'Use sulfur-based fungicides. Remove infected plant material. Avoid overhead watering.',
    'blight': 'Apply fungicides containing chlorothalonil. Rotate crops. Remove debris.',
    'powdery_mildew': 'Use sulfur or potassium bicarbonate. Increase air flow. Avoid high humidity.'
}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Predict
            if model is not None:
                image = Image.open(filepath)
                processed_image = preprocess_image(image)
                
                predictions = model.predict(processed_image)
                predicted_class = class_names[np.argmax(predictions[0])]
                confidence = float(np.max(predictions[0]) * 100)
                
                # Save to database
                save_prediction(filename, predicted_class, confidence)
                
                treatment = TREATMENT_SUGGESTIONS.get(predicted_class.lower(), 'Consult agricultural expert.')
                
                return render_template('result.html', 
                                     filename=filename,
                                     disease=predicted_class,
                                     confidence=confidence,
                                     treatment=treatment)
            else:
                flash('Model not loaded. Please train the model first.')
                return redirect(url_for('home'))
    
    return render_template('upload.html')
@app.route('/history')
def history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM predictions ORDER BY date DESC LIMIT 10"
        cursor.execute(query)

        predictions = cursor.fetchall()

        print("DATA:", predictions)  # 🔥 debug

        cursor.close()
        conn.close()

        return render_template('history.html', predictions=predictions)

    except Exception as e:
        print("❌ DB ERROR:", e)   # 🔥 actual error disel
        flash('Database not configured properly')
        return render_template('history.html', predictions=[])
    
import os
print("Current folder:", os.getcwd())
print("Model exists:", os.path.exists("model/best_crop_disease_model.h5"))

if __name__ == '__main__':
    app.run(debug=True)

