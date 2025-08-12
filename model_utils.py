import os, json
import numpy as np
from PIL import Image
import tensorflow as tf

MODEL = None
INPUT_SHAPE = (150, 150)

MODEL_PATH = os.path.join('model', 'fire_model.tflite')
CLASS_NAMES_PATH = os.path.join('model', 'class_names.json')

# Google Drive links (update if needed)
MODEL_URL = "https://drive.google.com/uc?id=1BBQt3ERqucWUjhV8fjij-QWmRXR9eKVY"
CLASS_NAMES_URL = None  # Set link if stored on Drive, else leave as None


def load_model():
    global MODEL, INPUT_SHAPE, CLASS_NAMES

    # --- Check & download model ---
    if not os.path.exists(MODEL_PATH):
        print("⚠ Model file missing, downloading...")
        import gdown
        os.makedirs("model", exist_ok=True)
        gdown.download(MODEL_URL, MODEL_PATH, quiet=False)
        if os.path.exists(MODEL_PATH):
            print("✅ Model file exists and size:", os.path.getsize(MODEL_PATH), "bytes")
        else:
            raise FileNotFoundError(f"Model still missing after download: {MODEL_PATH}")

    # --- Load the model ---
    MODEL = tf.keras.models.load_model(MODEL_PATH)

    # Update input shape
    try:
        inp = MODEL.input_shape
        if inp is not None and len(inp) >= 3:
            INPUT_SHAPE = (int(inp[1]), int(inp[2]))
    except Exception:
        pass

    # --- Load or create class names ---
    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, 'r') as f:
            CLASS_NAMES = json.load(f)
    else:
        if CLASS_NAMES_URL:
            print("⚠ class_names.json missing, downloading...")
            import gdown
            gdown.download(CLASS_NAMES_URL, CLASS_NAMES_PATH, quiet=False)
            if os.path.exists(CLASS_NAMES_PATH):
                with open(CLASS_NAMES_PATH, 'r') as f:
                    CLASS_NAMES = json.load(f)
            else:
                print("❌ class_names.json not found after download, using defaults.")
                CLASS_NAMES = ['nofire', 'fire']
        else:
            CLASS_NAMES = ['nofire', 'fire']


def preprocess_image_bytes(image_file):
    img = Image.open(image_file).convert('RGB')
    img = img.resize(INPUT_SHAPE)
    arr = np.array(img).astype('float32') / 255.0
    return np.expand_dims(arr, axis=0)


def predict_from_image_bytes(image_file):
    global MODEL, CLASS_NAMES
    if MODEL is None:
        load_model()
    x = preprocess_image_bytes(image_file)
    preds = MODEL.predict(x)

    try:
        prob = float(preds[0][0])
        idx = 1 if prob > 0.5 else 0
        label = CLASS_NAMES[idx]
        return {'label': label, 'probability': prob}
    except Exception:
        p = np.asarray(preds)[0]
        idx = int(np.argmax(p))
        prob = float(p[idx])
        label = CLASS_NAMES[idx]
        return {'label': label, 'probability': prob}

