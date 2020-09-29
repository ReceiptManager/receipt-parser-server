# -------------------------------------------------------------------------------------------------
# IMPORTS
import os
import socket
from flask import Flask, flash, request, redirect
from werkzeug.utils import secure_filename

# -------------------------------------------------------------------------------------------------
# SERVER SETTINGS
ALLOWED_PORT = 5000
ALLOWED_HOST = socket.gethostbyname(socket.gethostname())
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
UPLOAD_FOLDER = 'data/img'
CERT_LOCATION = "cert.pem"
KEY_LOCATION = "key.pem"
app = Flask(__name__)
app.secret_key = "test"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 * 1024  # 16 MB


# -------------------------------------------------------------------------------------------------
# HELPER METHODS
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# PRINT INFO
def info(skk): print("\033[95m {}\033[00m".format(skk))


# PRINT ERROR
def error(skk): print("\033[91m {}\033[00m".format(skk))


# GET WORK DIR
def getWorkDir():
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
    if "file" not in request.files:
        error("No image exist")
        flash("No file part")
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        error("No filename exist")
        flash("Image has no filename")
        return redirect(request.url)

    if file and allowed_file(file.filename):
        info('Uploaded file: ' + file.filename)

        filename = secure_filename(file.filename)
        output = os.path.join(getWorkDir() + app.config["UPLOAD_FOLDER"], filename)
        info("Store file at: " + output)

        file.save(output)
        info("Image successfully uploaded and displayed")

        return "Success"

    else:
        error("Invalid image or filetype")
        flash("Allowed image types are -> png, jpg, jpeg, gif")
        return redirect(request.url)


# -------------------------------------------------------------------------------------------------
# MAIN
if __name__ == "__main__":
    info("Start in workdir + " + getWorkDir())
    info("Start flusk server with TLS support")
    info("Cert file: " + getWorkDir() + CERT_LOCATION)
    info("Key file: " + getWorkDir() + KEY_LOCATION)

    app.run(ALLOWED_HOST, ALLOWED_PORT, ssl_context=(getWorkDir() + CERT_LOCATION, getWorkDir() + KEY_LOCATION))
