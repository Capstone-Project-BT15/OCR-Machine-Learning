# KTP Detection & Flask OCR (Text recognition from identity card)
___
KTP Detection is a TensorFlow model using CNN to identify KTP from user's identity card. The objective of this component is to recognize user's identity card whether it is KTP or not. If the identitiy card recognized as a KTP, the algorithm will call Flask OCR.
Flask OCR is a Python web application that employs Optical Character Recognition (OCR) to identify and extract information from identity cards. The objective of this component is to streamline the text extraction process for identity cards, thus enhancing the application's usability.

# Steps
___
1. Upload image of an identity card.
2. Detecting identity card whether it is KTP or not.
3. If it is a KTP then calling the Flask OCR.
4. Extract textual information from the image.
5. Display important information needed.
6. Insert the extracted data to database.
7. Return response json (Sucess, Failure).
8. If it isn't KTP then it will return error message.

# Prerequisites
___
1. Python 3.9 or higher
2. TensorFlow
3. Flask web framework
4. OCR library
5. Python libraries (specified in requirements.txt)

# Disclaimer
___
This part of the program is far from perfect. The accuracy and reliability of KTP Detection model and OCR may vary depending on various factors, including the quality of the input image.
