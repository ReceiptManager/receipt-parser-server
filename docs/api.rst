Upload API
====================
The upload API is used to upload a given receipt to the receipt parser server.
The server return the parsed image (if successful) or an ERROR code.


Entrypoint
"""""""""""""""

The entrypoint of the upload api is ``api/upload``.


Parameter
"""""""""""""""

+-----------------+------+---------------+-------------------------+
| Parameter       | Type | Default value | Description             |
+-----------------+------+---------------+-------------------------+
| legacy_parser   | bool | false         | Use the legacy parser   |
+-----------------+------+---------------+-------------------------+
| grayscale_image | bool | false         | Grayscale the image     |
+-----------------+------+---------------+-------------------------+
| gaussian_blur   | bool | false         | Apply the gaussian blur |
+-----------------+------+---------------+-------------------------+
| rotate_image    | bool | false         | Rotate image            |
+-----------------+------+---------------+-------------------------+

Please note: The parameter `file` and `access_token` is always required.
Take a look at the cURL example.

Return Code
"""""""""""""""

+-------------+---------------------+
| Return code | Event               |
+-------------+---------------------+
| 200         | request is valid    |
+-------------+---------------------+
| 403         | APITOKEN is invalid |
+-------------+---------------------+
| 415         | image is invalid    |
+-------------+---------------------+

Curl example
"""""""""""""""

.. code-block:: bash

    curl -X POST "https://$IP:$PORT/api/upload?access_token=$API_TOKEN -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=$IMAGE;type=image/jpeg"

with the given parameters:

+--------------+-------------------------+
| Parameter    | Description             |
+--------------+-------------------------+
| IP           | The server ip           |
+--------------+-------------------------+
| PORT         | The server port         |
+--------------+-------------------------+
| ACCESS_TOKEN | The server access token |
+--------------+-------------------------+
| IMAGE        | The receipt image       |
+--------------+-------------------------+

Training API
====================
The training API is used to upload a given receipt to the receipt parser server.
The server return the parsed image (if successful) or an ERROR code.

Entrypoint
"""""""""""""""

The entrypoint of the upload api is ``api/training``.

Return Code
"""""""""""""""

+-------------+---------------------+
| Return code | Event               |
+-------------+---------------------+
| 200         | request is valid    |
+-------------+---------------------+
| 403         | APITOKEN is invalid |
+-------------+---------------------+
| 415         | image is invalid    |
+-------------+---------------------+

Parameter
""""""""""""

The parameter receipt and access_token is always required. Take a look at the cURL example.

Curl example
"""""""""""""""

.. code-block:: bash

   curl -X POST "https://$IP:$PORT/api/training?access_token=$ACCESS_TOKEN" -H  "accept: application/json" --data '{"company":"$COMPANY_NAME","date":"$DATE","total":"$RECEIPT_TOTAL"}'   -k

with the given parameters:

+--------------+-------------------------+
| Parameter    | Description             |
+--------------+-------------------------+
| IP           | The server ip           |
+--------------+-------------------------+
| PORT         | The server port         |
+--------------+-------------------------+
| ACCESS_TOKEN | The server access token |
+--------------+-------------------------+
| RECEIPT      | Receipt object as json  |
+--------------+-------------------------+

the receipt object is submitted via the ``--data`` flag.