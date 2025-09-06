import os
import numpy as np
from io import BytesIO
import base64
from flask import Flask, render_template, request, redirect, url_for
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from flask import send_from_directory

import h5py  # Add this line to handle .h5 model files



app = Flask(__name__)

# Load the pre-trained models (ensure the model files are in the same directory)
glaucoma_model = tf.keras.models.load_model("glaucoma_detection_model.keras", compile=False)

cd_model = tf.keras.models.load_model("cd_ratio_model.h5", compile=False)
custom_glaucoma_model = tf.keras.models.load_model("cnn_glaucoma_model_lag.keras")


# Global configuration for image size (for CD ratio prediction)
IMAGE_SIZE = (224, 224)

##############################
# Home Route
##############################
@app.route("/")
def home():
    return render_template("home.html")

##############################
# Clinical Glaucoma Detection Route
##############################
@app.route("/clinical", methods=["GET", "POST"])
def clinical():
    prediction_text = None
    alert_class = None
    form_data = {}
    if request.method == "POST":
        try:
            # Get input values from the form for clinical glaucoma detection
            age = float(request.form["age"])
            iop = float(request.form["iop"])
            cct = float(request.form["cct"])
            oct_rnfl = float(request.form["oct_rnfl"])
            oct_rnfl1 = float(request.form["oct_rnfl1"])
            oct_rnfl2 = float(request.form["oct_rnfl2"])
            oct_rnfl3 = float(request.form["oct_rnfl3"])
            oct_rnfl4 = float(request.form["oct_rnfl4"])
            vf_mean = float(request.form["vf_mean"])
            interval_years = float(request.form["interval_years"])
            
            # Create the input array in the order the glaucoma model expects
            input_data = np.array([[age, iop, cct, oct_rnfl, oct_rnfl1, oct_rnfl2, oct_rnfl3, oct_rnfl4, vf_mean, interval_years]])
            
            # Get the raw predicted probability from the glaucoma model
            raw_prob = glaucoma_model.predict(input_data)[0][0]
            
            # Amplify the probability by 10 and then transform as (1 - (raw_prob * 10)) x 100
            transformed_percentage = (1 - (raw_prob * 10)) * 100
            
            # Determine diagnosis based on an 85% threshold
            diagnosis = "Normal" if transformed_percentage > 85 else "Glaucoma"
            
            # Set alert class: red for glaucoma, green for normal
            alert_class = "alert-danger" if diagnosis == "Glaucoma" else "alert-success"
            
            prediction_text = (f"Confidence Percentage: {transformed_percentage:.2f}%<br>"
                               f"Diagnosis: {diagnosis}")
            
            # Save form data to repopulate form fields if needed
            form_data = request.form
        except Exception as e:
            prediction_text = f"Error in prediction: {e}"
            alert_class = "alert-warning"
            form_data = request.form

    return render_template("clinical.html", prediction=prediction_text, alert_class=alert_class, form_data=form_data)

##############################
# CD Ratio Prediction Route
##############################
@app.route("/cd_ratio", methods=["GET", "POST"])
def cd_ratio():
    prediction_text = None
    alert_class = None
    uploaded_image = None
    if request.method == "POST":
        try:
            # Check if the file part exists in the request
            if "inputImage" not in request.files:
                raise Exception("No file part in the request")
            file = request.files["inputImage"]
            if file.filename == "":
                raise Exception("No file selected for uploading")
            
            # Read file bytes into memory and process image
            img_bytes = file.read()
            img = load_img(BytesIO(img_bytes), target_size=IMAGE_SIZE)
            img_array = img_to_array(img)
            img_array = img_array / 255.0  # Normalize pixel values
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            
            # Get the predicted CD ratio from the cd_model
            cd_ratio_pred = cd_model.predict(img_array)[0][0]
            
            prediction_text = f"Predicted CD Ratio: {cd_ratio_pred:.3f}"
            alert_class = "alert-info"
            
            # Convert the uploaded image to a base64 string for display
            uploaded_image = base64.b64encode(img_bytes).decode('utf-8')
        except Exception as e:
            prediction_text = f"Error in CD Ratio prediction: {e}"
            alert_class = "alert-warning"

    return render_template("cd_ratio.html", prediction=prediction_text, alert_class=alert_class, uploaded_image=uploaded_image)

##############################
# Custom Glaucoma Detection Route
##############################
@app.route("/custom_glaucoma", methods=["GET", "POST"])
def custom_glaucoma():
    prediction_text = None
    alert_class = None
    uploaded_image = None
    if request.method == "POST":
        try:
            # Check if the file part exists in the request
            if "inputImage" not in request.files:
                raise Exception("No file part in the request")
            file = request.files["inputImage"]
            if file.filename == "":
                raise Exception("No file selected for uploading")
            
            # Read file bytes into memory and process the image
            img_bytes = file.read()
            img = load_img(BytesIO(img_bytes), target_size=IMAGE_SIZE)
            img_array = img_to_array(img)
            img_array = img_array / 255.0  # Normalize pixel values
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            
            # Use the custom glaucoma model to predict
            raw_pred = custom_glaucoma_model.predict(img_array)[0][0]
            diagnosis = "Glaucoma" if raw_pred < 0.5 else "Normal"
            prediction_text = f"Prediction: {diagnosis} (score: {raw_pred:.3f})"
            alert_class = "alert-danger" if diagnosis == "Glaucoma" else "alert-success"
            
            # Convert the uploaded image to a base64 string for display
            uploaded_image = base64.b64encode(img_bytes).decode('utf-8')
        except Exception as e:
            prediction_text = f"Error in prediction: {e}"
            alert_class = "alert-warning"
    
    return render_template("custom_glaucoma.html", prediction=prediction_text, alert_class=alert_class, uploaded_image=uploaded_image)

@app.route('/templates/<path:filename>')
def serve_template_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'templates'), filename)

if __name__ == "__main__":
    app.run(debug=True)
