# -------------------------------------------------------------------------------------------------
# IMPORTS
import json
import os
import socket

from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename

# -------------------------------------------------------------------------------------------------
# SERVER SETTINGS
from src.main.parser.importer import prepare_folders, find_images, INPUT_FOLDER, sharpen_image, run_tesseract, \
    OUTPUT_FOLDER, TMP_FOLDER
from src.main.parser.parse import read_config, get_files_in_folder, ocr_receipts

ALLOWED_PORT = 8721
ALLOWED_HOST = socket.gethostbyname(socket.gethostname())
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
UPLOAD_FOLDER = 'data/img'
CERT_LOCATION = "client.crt"
KEY_LOCATION = "client.key"
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

    if "server" in dir:
        dir = dir.replace("src/main/server", "")

    if not dir.endswith("/"):
        dir = dir + "/"

    return dir


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
        prepare_folders()

        filename = secure_filename(file.filename)
        output = os.path.join(get_work_dir() + app.config["UPLOAD_FOLDER"], filename)
        info("Store file at: " + output)
        file.save(output)

        info("Image successfully uploaded and displayed")
        images = list(find_images(INPUT_FOLDER))
        for image in images:
            input_path = os.path.join(
                INPUT_FOLDER,
                image
            )
            tmp_path = os.path.join(
                TMP_FOLDER,
                image
            )
            out_path = os.path.join(
                OUTPUT_FOLDER,
                image + ".out"
            )

            sharpen_image(input_path, tmp_path)
            run_tesseract(tmp_path, out_path)

            config = read_config(get_work_dir() + "/config.yml")
            receipt_files = get_files_in_folder(get_work_dir() + "data/img")
            ocr_receipts(config, receipt_files)
s
            date = {"storeName": "",
                    "receiptTotal": "",
                    "receiptDate": "",
                    "receiptCategory": ""}

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
