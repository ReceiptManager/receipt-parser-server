import json
import os
from datetime import datetime, date
from json import dumps

from flask import Flask, flash, request, redirect
from receipt_parser.config import read_config
from receipt_parser.enhancer import process_receipt
from werkzeug.utils import secure_filename

ALLOWED_PORT = 8721
ALLOWED_HOST = "0.0.0.0"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
UPLOAD_FOLDER = 'data/img'
CERT_LOCATION = "cert/server.crt"
KEY_LOCATION = "cert/server.key"
DATA_PREFIX = "data/img/"
app = Flask(__name__)
app.debug = True
app.secret_key = "ignore_me"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 16 MB
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def info(skk): print("\033[95m{}\033[00m".format(skk))


def error(skk): print("\033[91m{}\033[00m".format(skk))


def get_work_dir():
    dir = os.getcwd()

    if "main" in dir: dir = dir.replace("src/main/", "")
    if not dir.endswith("/"): dir = dir + "/"

    return dir


def save_ret(component):
    if not component: return ""
    return component


def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    raise TypeError("Type %s not serializable" % type(obj))


def print_receipt(receipt):
    print("Company:    ", save_ret(receipt.market))
    print("Date:       ", save_ret(receipt.date))
    print("Amount:     ", save_ret(receipt.sum))


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

        info("Parsing image")
        config = read_config(get_work_dir() + "/config.yml")
        receipt = process_receipt(config, filename)

        print_receipt(receipt)

        receipt_data = {"storeName": receipt.market,
                        "receiptTotal": receipt.sum,
                        "receiptDate": dumps(receipt.date, default=json_serial),
                        "receiptCategory": "grocery"}

        response = app.response_class(
            response=json.dumps(receipt_data),
            mimetype='application/json'
        )

        return response

    else:
        error("Invalid image or filetype")
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


def start():
    info("Start in workdir + " + get_work_dir())
    info("Start flusk server with TLS support")
    info("Cert file: " + get_work_dir() + CERT_LOCATION)
    info("Key file: " + get_work_dir() + KEY_LOCATION)

    app.run(ALLOWED_HOST, ALLOWED_PORT, ssl_context=(get_work_dir() + CERT_LOCATION, get_work_dir() + KEY_LOCATION))


if __name__ == '__main__':
    start()
