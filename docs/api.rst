Upload API
====================
The upload API is used to upload a given receipt to the receipt parser server.
The server return the parsed image (if successfull) or an ERROR code.


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

Return Code
"""""""""""""""

The server return ``200`` if success or ``500`` if the given image is invalid or the
API token is invalid.

Curl example
"""""""""""""""

.. code-block:: bash

    curl -X POST "https://$IP:$PORT/api/upload ?access_token=$API_TOKEN -H  "accept: application/json" -H  "Content-Type: multipart/form-data" -F "file=$IMAGE;type=image/jpeg"

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
