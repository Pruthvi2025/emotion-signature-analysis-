import os
import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from PIL import Image
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

# Set up the Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.secret_key = 'your_secret_key'

# Corrected path for your background image
BACKGROUND_IMAGE_PATH = r"C:\Users\pruth\Downloads\DALL·E 2025-01-29 09.49.53 - A futuristic digital background representing signature analysis and emotion prediction. The image should feature abstract neural networks, glowing han.webp"

# Feature extraction function (mockup)
def extract_features(image_path):
    return np.random.rand(1, 258)

# Pre-trained model and scaler (mockup)
def load_pretrained_model():
    model = SVC(probability=True)
    scaler = StandardScaler()
    return model, scaler

# Mock training function
def train_mock_model():
    model, scaler = load_pretrained_model()
    X_train = np.random.rand(100, 258)
    y_train = np.random.choice([1, 2, 3, 4], size=100)
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    model.fit(X_train, y_train)
    return model, scaler

# Predict emotion function
def predict_emotion(model, scaler, image_path):
    features = extract_features(image_path)
    if features is None:
        return "Invalid image or unable to extract features."
    
    features = scaler.transform(features)
    emotion_label = model.predict(features)[0]
    emotion_map = {1: "Happy", 2: "Sad", 3: "Angry", 4: "Normal"}
    
    return emotion_map.get(emotion_label, "Unknown")

# Train model
model, scaler = train_mock_model()

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for uploading and predicting emotion
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        
        # If user does not select a file, the browser submits an empty part without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Predict emotion based on the uploaded signature image
            predicted_emotion = predict_emotion(model, scaler, filepath)
            emoji_map = {
                "Happy": "😊",
                "Sad": "😢",
                "Angry": "😡",
                "Normal": "😐"
            }
            emoji = emoji_map.get(predicted_emotion, "❓")
            
            return render_template('result.html', emotion=predicted_emotion, emoji=emoji, image_url=filepath)

    return render_template('upload.html')

# Run the application
if __name__ == "__main__":
    app.run(debug=True)
