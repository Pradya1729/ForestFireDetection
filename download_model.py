import gdown
import os

# Your full Google Drive link
url = "https://drive.google.com/file/d/1WyRsEwZ5APGkIB-ry_zFrimK26BOZbOk/view?usp=drive_link"

output = os.path.join("model", "fire_model.tflite")
os.makedirs("model", exist_ok=True)

print("📥 Downloading model from Google Drive...")
gdown.download(url, output, quiet=False)

if os.path.exists(output):
    print(f"✅ Model downloaded successfully to {output}")
else:
    print("❌ Download failed! Check if the file is shared as 'Anyone with the link'.")

