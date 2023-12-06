import easyocr
from PIL import Image,ImageDraw
import cv2
import matplotlib.pyplot as plt
import re
import os

from flask import Flask, request
from google.cloud import storage
from io import BytesIO
from flask_cors import CORS
from urllib.parse import unquote

def CariNIK(X):
    for i in X:
        if re.match(r'\d{10,}',i):
            return i

    return ""

def CariNama(X):
    c=0
    for i in X:
        if c==1:
            return i
        if re.match(r'nam[a-z]',i.lower()):
            c=1

    return ""

def CariTTL(X):
  for i in X:
    match = re.search(r'[a-zA-Z, ]+(\d{2}[- ]{1}\d{2}[- ]{1}\d{4})', i)
    if match:
        extracted_format = match.group(1)
        return extracted_format
  return ""

app = Flask(__name__)
CORS(app)

reader = easyocr.Reader(['id'])

#Get OCR Data (still a guess, haven't tried it yet)
def getOCRData(params):
    response = requests.get(params)
    image = Image.open(BytesIO(response.content))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gaussian = cv2.GaussianBlur(src=gray,ksize=(3, 3),sigmaX=0,sigmaY=0)
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
    results = reader.readtext(image)
    List= []
    for result in results:
        List.append(result[1])
    return json.dumps({
      'error': 'false',
      'message': 'Data berhasil diterima!',
      'NIK':CariNIK(List),
      'Nama':CariNama(List),
      'Tgl Lahir':CariTTL(List),
      'Link Photo':params
      })

#Still a guess, haven't tried it yet
@app.route('/masuk',methods=['POST'])
def upload():
    gcpClient = secretmanager.SecretManagerServiceClient()
    keysName = f"projects/xxx/secrets/gcs-key/versions/latest"
    response = gcpClient.access_secret_version(request={"name": keysName})
    credentials = json.loads(response.payload.data.decode('UTF-8'))
    client = storage.Client.from_service_account_info(credentials)
    file= request.files['images']
    file.save(file.filename)
    bucket_name = "xxx"
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob('fotoktp/{}'.format(file.filename))
    blob.upload_from_filename(file.filename)
    linkFoto = blob.public_url
    os.remove(file.filename)
    test = getOCRData(linkFoto)
    return test

if __name__ == '__main__':
    app.run(debug=True)
