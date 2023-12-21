import json
import re
from flask
import Flask, request
from flask_cors
import CORS
from keras.models import load_model
from PIL import Image, ImageDraw
import cv2
import easyocr
import numpy as np
import os
import requests
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

app = Flask(__name__)
CORS(app)

# Load the KTP detection model
ktp_model = load_model('ktp_detection_model.h5')

reader = easyocr.Reader(['id'])

def CariNIK(X):
    for i in X:
        if re.match(r'\d{10,}', i):
            return i

    return ""

def CariNama(X):
    c = 0
    for i in X:
        if c == 1:
            return i
        if re.match(r'nam[a-z]', i.lower()):
            c = 1

    return ""

def CariTTL(X):
    for i in X:
        match = re.search(r'[a-zA-Z, ]+(\d{2}[- ]{1}\d{2}[- ]{1}\d{4})', i)
        if match:
            extracted_format = match.group(1)
            return extracted_format
    return ""

def ktp_detection(params):
    img = Image.open(params)
    img_array = np.array(img)
    img_array = cv2.resize(img_array, (150, 150))  # Adjust target size as needed
    img_array = np.expand_dims(img_array, axis=0)
    print("Input Image Shape:", img_array.shape)
    predictions = ktp_model.predict(img_array)
    return predictions

reader = easyocr.Reader(['id'])

def getOCRData(file):
    predictions = ktp_detection(file)

    if predictions[0, 0] == 0:
        image = Image.open(file)
        gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        gaussian = cv2.GaussianBlur(src=gray, ksize=(3, 3), sigmaX=0, sigmaY=0)
        clahe = cv2.createCLAHE(clipLimit=2.00, tileGridSize=(12, 12))
        image = clahe.apply(gaussian)
        _, final_image = cv2.threshold(image, thresh=165, maxval=255, type=cv2.THRESH_TRUNC + cv2.THRESH_OTSU)
        border_image = cv2.copyMakeBorder(
            src=final_image,
            top=20,
            bottom=20,
            left=20,
            right=20,
            borderType=cv2.BORDER_CONSTANT,
            value=(255, 255, 255))
        results = reader.readtext(np.array(border_image))
        List = []
        for result in results:
            List.append(result[1])
        nik = CariNIK(List)
        nama = CariNama(List).title()
        ttl = CariTTL(List)
        if (nama is not None and nik is not None and ttl is not None and isinstance(nama, str) and isinstance(nik, str) and isinstance(ttl, str) and nama.strip() != '' and nik.strip() != '' and ttl.strip() != ''):
            return json.dumps({
                'error': 'false',
                'message': 'Data berhasil diterima!',
                'NIK': nik,
                'Nama': nama,
                'Tgl Lahir': ttl,
                'Link Photo': 'uploaded_image.jpg'
            })
        else:
            return json.dumps({
                'error': 'true',
                'message': 'Foto KTP tidak jelas atau data tiddak valid',
            })

    else:
        return json.dumps({
            'error': 'true',
            'message': 'KTP not detected in the image.'
        })

@app.route('/masuk/image', methods=['POST'])
def upload_image():
    if 'images' not in request.files:
        return json.dumps({'error': 'true', 'message': 'No file part'})

    uploaded_file = request.files['images']

    if uploaded_file.filename == '':
        return json.dumps({'error': 'true', 'message': 'No selected file'})

    uploaded_file.save('uploaded_image.jpg')  # Save the uploaded image to a file
    test_result = getOCRData(uploaded_file)  # Process the uploaded image

    # Logic to upload to the specified API link
    api_endpoint = 'https://jasane-vy5bsv56bq-et.a.run.app/api/ktp/verification'
    files = {'ktp': open('uploaded_image.jpg', 'rb')}
    response = requests.post(api_endpoint, files=files)

    return response.text  # Returning the response from the API

@app.route('/masuk', methods=['POST'])
def upload_image_old():
    if 'file' not in request.files:
        return json.dumps({'error': 'true', 'message': 'No file part'})

    uploaded_file = request.files['file']

    if uploaded_file.filename == '':
        return json.dumps({'error': 'true', 'message': 'No selected file'})

    uploaded_file.save('uploaded_image.jpg')  # Save the uploaded image to a file
    test_result = getOCRData('uploaded_image.jpg')  # Process the uploaded image

    # Logic to upload to the specified API link
    api_endpoint = 'https://jasane-vy5bsv56bq-et.a.run.app/api/ktp/verification'
    files = {'ktp': open('uploaded_image.jpg', 'rb')}
    response = requests.post(api_endpoint, files=files)

    return response.text  # Returning the response from the API


@app.route('/')
def home():
    return "Welcome to the home page"

if __name__ == '__main__':
    app.run(debug=True)
