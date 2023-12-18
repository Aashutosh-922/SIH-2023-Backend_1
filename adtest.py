# import cv2
# from pyzbar.pyzbar import decode
# from pyaadhaar.utils import isSecureQr
# from pyaadhaar.decode import AadhaarSecureQr

# img = cv2.imread('/home/aashutosh9178/Downloads/Screenshot_2023-09-24-18-41-42-172_com.google.android.apps.docs.jpg')
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# code = decode(gray)
# qrData = code[0].data

# isSecureQR = (isSecureQr(qrData))

# if isSecureQR:
#     secure_qr = AadhaarSecureQr(int(qrData))
#     decoded_secure_qr_data = secure_qr.decodeddata()
#     print(decoded_secure_qr_data)
# app.py

from flask import Flask, render_template, request
import cv2
from pyzbar.pyzbar import decode
from pyaadhaar.utils import isSecureQr
from pyaadhaar.decode import AadhaarSecureQr
import os

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the uploaded file
        uploaded_file = request.files['file']

        if uploaded_file.filename != '':
            # Save the uploaded file
            uploaded_file.save(os.path.join('uploads', uploaded_file.filename))

            # Process the uploaded image
            image_path = os.path.join('uploads', uploaded_file.filename)
            decoded_data = process_image(image_path)
            return render_template('index.html', decoded_data=decoded_data)

    return render_template('index.html', decoded_data=None)


def process_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    code = decode(gray)
    qr_data = code[0].data if code else None

    if qr_data:
        is_secure_qr = isSecureQr(qr_data)

        if is_secure_qr:
            secure_qr = AadhaarSecureQr(int(qr_data))
            decoded_secure_qr_data = secure_qr.decodeddata()
            return decoded_secure_qr_data

        print("test comment ")
    return None


if __name__ == '__main__':
    app.run(port=4000, debug=True)
