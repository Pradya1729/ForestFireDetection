import os, json
import numpy as np
from PIL import Image
import tensorflow as tf

MODEL = None
INPUT_SHAPE = (150, 150)
MODEL_PATH = os.path.join('model', 'fire_model.h5')  # change to your file name
CLASS_NAMES_PATH = os.path.join('model', 'class_names.json')

def load_model():
    global MODEL, INPUT_SHAPE, CLASS_NAMES
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found: {MODEL_PATH}")
    MODEL = tf.keras.models.load_model(MODEL_PATH)

    try:
        inp = MODEL.input_shape
        if inp is not None and len(inp) >= 3:
            INPUT_SHAPE = (int(inp[1]), int(inp[2]))
    except Exception:
        pass

    if os.path.exists(CLASS_NAMES_PATH):
        with open(CLASS_NAMES_PATH, 'r') as f:
            CLASS_NAMES = json.load(f)
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
