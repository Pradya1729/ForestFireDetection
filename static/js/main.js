// static/js/main.js
const imageInput = document.getElementById('imageInput');
const uploadBtn = document.getElementById('uploadBtn');
const preview = document.getElementById('preview');
const resultDiv = document.getElementById('result');

uploadBtn.addEventListener('click', async () => {
  const file = imageInput.files[0];
  if (!file) { alert('Please choose an image first'); return; }

  preview.innerHTML = '';
  const imgEl = document.createElement('img');
  imgEl.src = URL.createObjectURL(file);
  preview.appendChild(imgEl);

  const form = new FormData();
  form.append('image', file);

  resultDiv.textContent = 'Predicting...';
  const res = await fetch('/predict', { method: 'POST', body: form });
  const data = await res.json();
  if (res.ok) {
    resultDiv.textContent = `Label: ${data.label} — Confidence: ${data.probability ? (data.probability*100).toFixed(2) + '%' : 'N/A'}`;
  } else {
    resultDiv.textContent = 'Error: ' + (data.error || 'Unknown');
  }
});

// Webcam capture
const video = document.getElementById('video');
const snap = document.getElementById('snap');
const canvas = document.getElementById('canvas');

if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
  navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    video.srcObject = stream;
    video.play();
  }).catch(err => {
    console.warn('Camera access denied or not available:', err);
  });
}

snap.addEventListener('click', async () => {
  const context = canvas.getContext('2d');
  context.drawImage(video, 0, 0, canvas.width, canvas.height);
  const dataURL = canvas.toDataURL('image/jpeg');

  resultDiv.textContent = 'Predicting...';
  const form = new FormData();
  form.append('data', dataURL);

  const res = await fetch('/predict', { method: 'POST', body: form });
  const data = await res.json();
  if (res.ok) {
    resultDiv.textContent = `Label: ${data.label} — Confidence: ${data.probability ? (data.probability*100).toFixed(2) + '%' : 'N/A'}`;
  } else {
    resultDiv.textContent = 'Error: ' + (data.error || 'Unknown');
  }
});
