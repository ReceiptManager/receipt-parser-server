import os
import json
import shutil
from datetime import datetime, date
from json import dumps

import uvicorn
from fastapi import FastAPI, Security, HTTPException, Depends, UploadFile, File
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from receipt_parser_core.config import read_config
from receipt_parser_core.enhancer import process_receipt
from starlette.responses import RedirectResponse
from starlette.status import HTTP_403_FORBIDDEN
from werkzeug.utils import secure_filename

# ========================================= < CONFIG > =========================================
API_KEY = "44meJNNOAfuzT"
API_KEY_NAME = "access_token"
COOKIE_DOMAIN = "localtest.me"
ALLOWED_PORT = 8721
ALLOWED_HOST = "0.0.0.0"

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
UPLOAD_FOLDER = 'data/img'
CERT_LOCATION = "cert/server.crt"
KEY_LOCATION = "cert/server.key"
DATA_PREFIX = "data/img/"
# ========================================= < CONFIG > =========================================

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)


async def get_api_key(
        api_key_query: str = Security(api_key_query),
        api_key_header: str = Security(api_key_header),
        api_key_cookie: str = Security(api_key_cookie),
):
    if api_key_query == API_KEY:
        return api_key_query
    elif api_key_header == API_KEY:
        return api_key_header
    elif api_key_cookie == API_KEY:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


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


def print_receipt_list(receipt):
    if not receipt.items:
        return None

    for _ in map(print, receipt.items):
        pass


def print_receipt(receipt):
    print("Company:    ", save_ret(receipt.market))
    print("Date:       ", save_ret(receipt.date))
    print("Amount:     ", save_ret(receipt.sum))
    print("Items:     ", print_receipt_list(receipt))


@app.post("/api/upload", tags=["test"])
async def get_open_api_endpoint(file: UploadFile = File(...), api_key: APIKey = Depends(get_api_key)):
    if file.filename == "":
        error("No filename exist")
        return "invalid_image"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        output = os.path.join(get_work_dir() + UPLOAD_FOLDER, filename)
        info("Store file at: " + output)

        with open(output, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        info("Parsing image")
        config = read_config(get_work_dir() + "/config.yml")
        receipt = process_receipt(config, filename)

        print_receipt(receipt)
        receipt_data = {"storeName": receipt.market,
                        "receiptTotal": receipt.sum,
                        "receiptDate": dumps(receipt.date, default=json_serial),
                        "receiptCategory": "grocery"}

        return json.dumps(receipt_data)


@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response


if __name__ == "__main__":
    uvicorn.run("receipt_server:app", host="127.0.0.1", port=ALLOWED_PORT, log_level="debug")
