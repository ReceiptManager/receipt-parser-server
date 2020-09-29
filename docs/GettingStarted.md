# Getting started

## Generate certificates
Run `make generate_cert` to generate new certificates.

## Start the server
Before you start the server. Generate new certificated, even they are self signed.

The server uses a flask development server. This is a very simple python server.
To start the server run `make serve`. The output should be something like this
```
 Start in workdir ...
 Start flusk server with TLS support
 Cert file: ...
 Key file: ...
 * Running on https://<IP>:<PORT>/ (Press CTRL+C to quit)
```
 You can debug the server using `telnet`.
 ```
telnet <IP> <PORT>
Trying <IP>...
Connected to <IP>
...
```

### Requests
If you now send a `POST` request. You should see following output at the server console
```
<IP> - - [<DATE>] "POST /api/upload/ HTTP/1.1" <RET> -
```
If the `POST` request was valid. The return code should be `200`. You could consider
the `server.py` for more details. 

The server now store the image at `data/img`. Now, the server enhance the image using
various of technics. After the server uses `TESSERACT` to parse the text.

The parsed text is send back to the device.

## Clean directory
To clean the directory use `make clean`.

## Parse text without application
The application is not required. If you place the images in `data/img` and run `make convert`
the images get enhanced and parsed by `TESSERACT`. 