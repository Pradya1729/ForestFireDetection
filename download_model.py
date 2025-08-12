import gdown
import os

# Your full Google Drive link
url = "https://drive.google.com/file/d/1BBQt3ERqucWUjhV8fjij-QWmRXR9eKVY/view?usp=drive_link"

output = os.path.join("model", "fire_model.h5")
os.makedirs("model", exist_ok=True)

print("📥 Downloading model from Google Drive...")
gdown.download(url, output, quiet=False)

if os.path.exists(output):
    print(f"✅ Model downloaded successfully to {output}")
else:
    print("❌ Download failed! Check if the file is shared as 'Anyone with the link'.")

