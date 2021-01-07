import json
import os
import random
import shutil
import socket
from json.encoder import JSONEncoder
from collections import namedtuple
from json import dumps

import receipt_printer as printer
import uvicorn
from colors import bcolors
from fastapi import FastAPI, Depends, UploadFile, File, Security, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey
from receipt_parser_core.config import read_config
from receipt_parser_core.enhancer import process_receipt
from starlette.responses import RedirectResponse
from starlette.status import HTTP_403_FORBIDDEN
from werkzeug.utils import secure_filename
from fastapi.responses import JSONResponse
import util as util

#import sys
#sys.path.insert(0, 'receipt-parser-neuronal/invoicenet/api/')
#from predict_api import predict


COOKIE_DOMAIN = "localtest.me"
ALLOWED_PORT = 8721
ALLOWED_HOST = "0.0.0.0"

UPLOAD_FOLDER = 'data/img'
CERT_LOCATION = "cert/server.crt"
KEY_LOCATION = "cert/server.key"
DATA_PREFIX = "data/img/"
API_TOKEN_FILE = ".api_token"

# fallback key
API_KEY = "44meJNNOAfuzT"
PRINT_DEBUG_OUTPUT=False

class TupelEncoder(JSONEncoder):

    def _iterencode(self, obj, markers=None):
        if isinstance(obj, tuple) and hasattr(obj, '_asdict'):
            gen = self._iterencode_dict(obj._asdict(), markers)
        else:
            gen = JSONEncoder._iterencode(self, obj, markers)
        for chunk in gen:
            yield chunk

def generate_api_token():
    random_string = ''
    for _ in range(10):
        random_integer = random.randint(97, 97 + 26 - 1)
        flip_bit = random.randint(0, 1)
        random_integer = random_integer - 32 if flip_bit == 1 else random_integer
        random_string += (chr(random_integer))

    tokenFile = open(API_TOKEN_FILE, "w")
    tokenFile.write(random_string)
    tokenFile.close()

    return random_string



if not os.path.isfile(API_TOKEN_FILE):
    API_KEY = generate_api_token()

else:
    with open(API_TOKEN_FILE) as f:
        line = f.readline().strip()
        if not line:
            API_KEY = generate_api_token()
        else:
            API_KEY = line

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
api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

# Current image api
@app.post("/api/upload", tags=["api"])
async def get_open_api_endpoint(file: UploadFile = File(...), api_key: APIKey = Depends(get_api_key)):
    if file.filename == "":
        printer.error("No filename exist")
        raise HTTPException(
            status_code=500, detail="Invalid image send"
        )

    if file and util.allowed_file(file.filename):
        print(file.filename)

        filename = secure_filename(file.filename)
        output = os.path.join(util.get_work_dir() + UPLOAD_FOLDER, filename)
        printer.info("Store file at: " + output)

        with open(output, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        if PRINT_DEBUG_OUTPUT:
            items = []
            # example items
            item = namedtuple("item", ("article", "sum"))
            items.append(item("Brot","1.33"))
            items.append(item("Kaffee", "5.33"))

            receipt_data = {"storeName": "DebugStore",
                            "receiptTotal": "15.10",
                            "receiptDate": "09.25.2020",
                            "receiptItems" : items,
                            "receiptCategory": "grocery"}
            json_compatible_item_data = jsonable_encoder(receipt_data)
            return JSONResponse(content=json_compatible_item_data)

        printer.info("Parsing image")
        config = read_config(util.get_work_dir() + "/config.yml")
        receipt = process_receipt(config, filename)

        printer.print_receipt(receipt)

        receipt_data = {"storeName":receipt.market ,
                        "receiptTotal": receipt.sum,
                        "receiptDate": dumps(receipt.date, default=util.json_serial),
                        "receiptItems": receipt.items,
                        "receiptCategory": "grocery"}

        json_compatible_item_data = jsonable_encoder(receipt_data)
        return JSONResponse(content=json_compatible_item_data)

    else:
        raise HTTPException(
            status_code=500, detail="Invalid image send"
        )

@app.get("/logout")
async def route_logout_and_remove_cookie():
    response = RedirectResponse(url="/")
    response.delete_cookie(API_KEY_NAME, domain=COOKIE_DOMAIN)
    return response


if __name__ == "__main__":
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)

    print("Current API token: " + bcolors.OKGREEN + API_KEY)
    uvicorn.run("receipt_server:app", host="0.0.0.0", port=8721, log_level="debug",
                ssl_certfile=util.get_work_dir() + CERT_LOCATION, ssl_keyfile=util.get_work_dir() + KEY_LOCATION)
