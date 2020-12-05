import json
import os
import shutil
from json import dumps

import receipt_api as api
import receipt_printer as printer
import uvicorn
from fastapi import FastAPI, Depends, UploadFile, File, Security, HTTPException
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from receipt_parser_core.config import read_config
from receipt_parser_core.enhancer import process_receipt
from starlette.responses import RedirectResponse
from starlette.status import HTTP_403_FORBIDDEN
from werkzeug.utils import secure_filename

import util as util

COOKIE_DOMAIN = "localtest.me"
ALLOWED_PORT = 8721
ALLOWED_HOST = "0.0.0.0"

UPLOAD_FOLDER = 'data/img'
CERT_LOCATION = "cert/server.crt"
KEY_LOCATION = "cert/server.key"
DATA_PREFIX = "data/img/"


API_KEY = "44meJNNOAfuzT" # not final
API_KEY_NAME = "access_token"

api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

async def get_api_key(
        api_query: str = Security(api_key_query),
        api_header: str = Security(api_key_header),
        api_cookie: str = Security(api_key_cookie),
):
    if api_query == API_KEY:
        return api_query
    elif api_header == API_KEY:
        return api_header
    elif api_cookie == API_KEY:
        return api_cookie
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )

# Set header and cookies
api_key_query = APIKeyQuery(name=api.API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=api.API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=api.API_KEY_NAME, auto_error=False)
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Current image api
@app.post("/api/upload", tags=["api"])
async def get_open_api_endpoint(file: UploadFile = File(...), api_key: APIKey = Depends(api.get_api_key)):
    if file.filename == "":
        printer.error("No filename exist")
        raise HTTPException(
            status_code=500, detail="Invalid image send"
        )

    if file and util.allowed_file(file.filename):
        filename = secure_filename(file.filename)
        output = os.path.join(util.get_work_dir() + UPLOAD_FOLDER, filename)
        printer.info("Store file at: " + output)

        with open(output, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        printer.info("Parsing image")
        config = read_config(util.get_work_dir() + "/config.yml")
        receipt = process_receipt(config, filename)

        printer.print_receipt(receipt)
        receipt_data = {"storeName": receipt.market,
                        "receiptTotal": receipt.sum,
                        "receiptDate": dumps(receipt.date, default=util.json_serial),
                        "receiptCategory": "grocery"}

        return json.dumps(receipt_data)
    else:
        raise HTTPException(
            status_code=500, detail="Invalid image send"
        )

@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(api.API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response


if __name__ == "__main__":
    uvicorn.run("receipt_server:app", host="192.168.0.103", port=8721, log_level="debug",
                ssl_certfile=util.get_work_dir() + CERT_LOCATION, ssl_keyfile = util.get_work_dir() + KEY_LOCATION)
