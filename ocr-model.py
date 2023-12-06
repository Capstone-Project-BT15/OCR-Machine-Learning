import easyocr
from PIL import Image,ImageDraw
import cv2
import matplotlib.pyplot as plt
import re

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
def CariAlamat(X):
    c=0
    for i in X:
        if c==1:
            return i
        if re.match(r'nam[a-z]',i.lower()):
            c=1

def CariTTL(X):
  for i in X:
    match = re.search(r'[a-zA-Z, ]+(\d{2}[- ]{1}\d{2}[- ]{1}\d{4})', i)
    if match:
        extracted_format = match.group(1)
        return extracted_format
  return ""

reader = easyocr.Reader(['id'])

image = '5.png'
results = reader.readtext(image)
List= []
for result in results:
    List.append(result[1])

List

CariNama(List),CariTTL(List),CariAlamat(List)

display(image)
print('NIK :',CariNIK(List))
print('Nama:',CariNama(List))
print('TTL :',CariTTL(List))
