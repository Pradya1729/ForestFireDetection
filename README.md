# Forest Fire Detection — Flask Webapp (VS Code, Windows)

This is a starter full-stack Flask webapp that loads your Keras model and serves a simple frontend
for uploading images or using a webcam to get predictions (fire / no fire).

## What you need (before running)
1. Python 3.8 - 3.12 installed on Windows.
2. VS Code with Python extension (recommended).
3. Your trained Keras model file from your notebook saved as `FFD.keras` (you already have `model.save('FFD.keras')` in your notebook). Copy `FFD.keras` into the `models/` folder.
4. (Optional but recommended) a `models/class_names.json` file containing the class names in index order, e.g. `["nofire","fire"]`.
   You can create it from your notebook like this:

```python
# after creating train_generator in your notebook
class_mapping = train_generator.class_indices   # e.g. {'nofire': 0, 'fire': 1}
inv = {v:k for k,v in class_mapping.items()}
class_names = [inv[i] for i in range(len(inv))]
import json, os
os.makedirs('models', exist_ok=True)
with open('models/class_names.json','w') as f:
    json.dump(class_names, f)
# and save the model
model.save('models/FFD.keras')
```

## Files in this project
- `app.py` — Flask backend that loads model and exposes `/predict` endpoint.
- `model_utils.py` — Loads model and preprocesses images.
- `templates/index.html` — Frontend page to upload or capture images.
- `static/js/main.js` and `static/css/styles.css` — Frontend scripts and styles.
- `requirements.txt` — Python packages to install.
- `.gitignore` — common ignores.

## Setup (Windows, VS Code)
1. Open the folder in VS Code (`File → Open Folder` → select this project).
2. Open Terminal in VS Code (Ctrl+`).
3. Create & activate a venv:
   ```
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Copy your trained model file (`FFD.keras`) into `models/` (create the `models/` folder if needed).
6. Run the app:
   ```
   python app.py
   ```
   Open `http://127.0.0.1:5000/` in your browser.

## If something fails
- If `ImportError` for tensorflow: check Python version and install a compatible TF wheel for Windows.
- Model input mismatch: ensure your model expects images resized to 150x150 (this notebook used 150x150). If different, edit `model_utils.INPUT_SHAPE`.
- If class labels appear swapped: re-create `models/class_names.json` from your notebook as shown above.

## Notes
- This skeleton does not include the trained model (too large). Place your `models/FFD.keras` file in the `models/` directory before running.
- If you'd like, reply “include my model” and upload `FFD.keras` and I will bundle it for you.
