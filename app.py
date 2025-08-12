import os
import base64
from io import BytesIO
from flask import Flask, render_template, request
from model_utils import predict_from_image_bytes

app = Flask(__name__)

# Folder to store uploaded/captured images
UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


# ---- File Upload Prediction ----
@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return "No file uploaded", 400

    file = request.files["file"]
    if file.filename == "":
        return "No selected file", 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    with open(file_path, "rb") as f:
        result = predict_from_image_bytes(f)

    prob_percent = round(result["probability"] * 100, 2)

    return render_template(
        "result.html",
        label=result["label"],
        probability=prob_percent,
        image_url=file.filename
    )


# ---- Webcam Capture Prediction ----
@app.route("/predict_webcam", methods=["POST"])
def predict_webcam():
    img_data = request.form.get("webcam_image")
    if not img_data:
        return "No image captured", 400

    # Remove prefix and decode Base64
    img_data = img_data.split(",")[1]
    image_bytes = base64.b64decode(img_data)

    # Save image
    file_path = os.path.join(UPLOAD_FOLDER, "webcam.jpg")
    with open(file_path, "wb") as f:
        f.write(image_bytes)

    # Predict from bytes
    result = predict_from_image_bytes(BytesIO(image_bytes))
    prob_percent = round(result["probability"] * 100, 2)

    return render_template(
        "result.html",
        label=result["label"],
        probability=prob_percent,
        image_url="webcam.jpg"
    )


if __name__ == "__main__":
    app.run(debug=True)
