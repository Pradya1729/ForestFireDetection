import gdown
import os

# Replace with your own Google Drive file ID
url = "https://drive.google.com/drive/folders/1Ldcq-ub_CEds3QADCHRHAj2p3ASm8J34"
output = os.path.join("model", "fire_model.h5")

os.makedirs("model", exist_ok=True)
print("📥 Downloading model from Google Drive...")
gdown.download(url, output, quiet=False)
print("✅ Model downloaded to", output)
