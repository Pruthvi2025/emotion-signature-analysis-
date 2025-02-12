import os
import random
from flask import Flask, render_template, request, redirect, url_for, flash

from werkzeug.utils import secure_filename

# Flask setup
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key_here")  # Use environment variable for security

# Configurations for the upload folder
UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Allow only certain file types
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # Limit upload size to 16 MB

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Mock emotion prediction function
def predict_emotion():
    emotions = ["Happy", "Sad", "Angry", "Normal"]
    return random.choice(emotions)

# Check if the file is allowed (only images)
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        flash("No file part", "error")
        return redirect(url_for("index"))

    file = request.files["file"]

    # If no file is selected
    if file.filename == "":
        flash("No selected file", "error")
        return redirect(url_for("index"))

    if file and allowed_file(file.filename):
        # Generate a secure filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        
        # Save the file
        file.save(file_path)

        # Predict the emotion
        predicted_emotion = predict_emotion()

        # Emotion descriptions
        descriptions = {
            "Happy": "You have an optimistic and cheerful personality. Your signature reflects confidence and positivity.",
            "Sad": "Your signature indicates emotional depth and introspection. You may be experiencing moments of stress or melancholy.",
            "Angry": "Your signature suggests a strong-willed and passionate personality. You may be feeling frustration or determination.",
            "Normal": "Your signature reflects balance and neutrality. You are calm and composed in various situations."
        }

        # Generate the URL for the uploaded image
        file_url = url_for("static", filename="uploads/" + filename)

        return render_template("result.html", 
                               predicted_emotion=predicted_emotion, 
                               file_url=file_url, 
                               description=descriptions[predicted_emotion])

    else:
        flash("Invalid file format. Please upload an image.", "error")
        return redirect(url_for("index"))

# Route for About page
@app.route("/about")
def about():
    return render_template("about.html")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
