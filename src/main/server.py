# -------------------------------------------------------------------------------------------------
# IMPORTS
import json
import os
import socket
from datetime import datetime, date
from json import dumps

import cv2
import numpy as np
from flask import Flask, flash, request, redirect
from receiptparser.config import read_config
from receiptparser.parser import process_receipt
# -------------------------------------------------------------------------------------------------
# SERVER SETTINGS
from werkzeug.utils import secure_filename

ALLOWED_PORT = 8721
ALLOWED_HOST = socket.gethostbyname(socket.gethostname())
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
UPLOAD_FOLDER = 'data/img'
CERT_LOCATION = "cert/server.crt"
KEY_LOCATION = "cert/server.key"
DATA_PREFIX = "data/img/"
app = Flask(__name__)
app.secret_key = "test"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024  # 16 MB


# -------------------------------------------------------------------------------------------------
# HELPER METHODS
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# PRINT INFO
def info(skk): print("\033[95m{}\033[00m".format(skk))


# PRINT ERROR
def error(skk): print("\033[91m{}\033[00m".format(skk))


# GET WORK DIR
def get_work_dir():
    dir = os.getcwd()

    if "main" in dir:
        dir = dir.replace("src/main/", "")

    if not dir.endswith("/"):
        dir = dir + "/"

    return dir


def save_ret(component):
    if not component:
        return ""

    return component


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    raise TypeError("Type %s not serializable" % type(obj))


# -------------------------------------------------------------------------------------------------
# UPLOAD API
@app.route("/api/upload/", methods=["POST"])
def upload_image():
    if "image" not in request.files:
        error("No image exist")
        flash("No file part")
        return redirect(request.url)

    file = request.files["image"]
    if file.filename == "":
        error("No filename exist")
        flash("Image has no filename")
        return redirect(request.url)

    if file and allowed_file(file.filename):
        info('Uploaded file: ' + file.filename)

        filename = secure_filename(file.filename)
        output = os.path.join(get_work_dir() + app.config["UPLOAD_FOLDER"], filename)
        info("Store file at: " + output)
        file.save(output)

        info("Image successfully uploaded and displayed")

        print("\t[TASK]: Rescale image")
        img = cv2.imread(get_work_dir() + DATA_PREFIX + filename)

        print("\t[TASK]: Grayscale image")
        img = cv2.resize(img, None, fx=1.2, fy=1.2, interpolation=cv2.INTER_CUBIC)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        print("\t[TASK]: Removing image noise")
        kernel = np.ones((1, 1), np.uint8)
        img = cv2.dilate(img, kernel, iterations=1)
        img = cv2.erode(img, kernel, iterations=1)

        print("\t[TASK]: Applying blur to the image")
        img = cv2.threshold(cv2.GaussianBlur(img, (5, 5), 0), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img = cv2.threshold(cv2.bilateralFilter(img, 5, 75, 75), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img = cv2.threshold(cv2.medianBlur(img, 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img = cv2.adaptiveThreshold(cv2.GaussianBlur(img, (5, 5), 0), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY,
                                    31, 2)
        img = cv2.adaptiveThreshold(cv2.bilateralFilter(img, 9, 75, 75), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY, 31, 2)
        img = cv2.adaptiveThreshold(cv2.medianBlur(img, 3), 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31,
                                    2)

        status = cv2.imwrite(get_work_dir() + DATA_PREFIX + filename, img)

        if status is True:
            info("Image written to file-system")

        info("Parsing image")
        config = read_config(get_work_dir() + "/config.yml")
        receipt = process_receipt(config, get_work_dir() + DATA_PREFIX + filename, out_dir=get_work_dir() + "data/txt/",
                                  verbosity=10)

        print("Filename:   ", save_ret(receipt.filename))
        print("Company:    ", save_ret(receipt.company))
        print("Postal code:", save_ret(receipt.postal))
        print("Date:       ", save_ret(receipt.date))
        print("Amount:     ", save_ret(receipt.sum))



        date = {"storeName": receipt.company,
                "receiptTotal": receipt.sum,
                "receiptDate": dumps(receipt.date, default=json_serial),
                "receiptCategory": "grocery"}

        response = app.response_class(
            response=json.dumps(date),
            mimetype='application/json'
        )

        return response

    else:
        error("Invalid image or filetype")
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


# -------------------------------------------------------------------------------------------------
# MAIN
if __name__ == "__main__":
    info("Start in workdir + " + get_work_dir())
    info("Start flusk server with TLS support")
    info("Cert file: " + get_work_dir() + CERT_LOCATION)
    info("Key file: " + get_work_dir() + KEY_LOCATION)

    app.run(ALLOWED_HOST, ALLOWED_PORT, ssl_context=(get_work_dir() + CERT_LOCATION, get_work_dir() + KEY_LOCATION))
