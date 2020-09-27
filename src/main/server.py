from flask import Flask, request, Response
import jsonpickle
import os

# -----------------------------------------------------------------------------
PORT=5000
HOST="0.0.0.0" 
# -----------------------------------------------------------------------------

app = Flask(__name__)
@app.route('/api/upload', methods=['POST'])

def handle_post_request(img):
    print("[REQ][POST] ", request)

    response = {'message': 'image received.'}
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")

app.run(host=HOST, port=PORT, ssl_context=('cert.pem', 'key.pem'))
