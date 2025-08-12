import gdown
import os

# Extracted file ID from your link
file_id = "1BBQt3ERqucWUjhV8fjij-QWmRXR9eKVY"
url = f"https://drive.google.com/uc?id={file_id}"

output = os.path.join("model", "fire_model.h5")
os.makedirs("model", exist_ok=True)

print("📥 Downloading model from Google Drive...")
gdown.download(url, output, quiet=False)
print("✅ Model downloaded to", output)
