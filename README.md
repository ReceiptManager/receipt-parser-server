# ReceiptManger server
## How it works

<p align="center">
<img src="https://miro.medium.com/max/647/1*KVZia8odiR2W-b6TOySjsg.png">
</p>

#### Client

1. At first the user takes an photo of the receipt.
2. The photo is uploaded to your server via a POST request

Now, the photo is stored at the server.

#### Server

1. Server increase the contrast of the given image
2. Blur is applied to the image
3. The server uses pytesseract to parses the text

Now, the parsed text is send as a JSON response

#### Client

1. The application convert the JSON response to a receipt object
2. The application auto fill the text-fields

## Getting started
### Recomended way
First, clone the repository.

```
git clone https://github.com/ReceiptManager/Server
```

After go in the server directory and install the required dependencies
```
cd Server
pip install -r requirements.txt
```

If you have not pip installed. Use your favorite package manager to install `python` and `python-pip`.
Now, generate new ssl certficates. First generate an new file called `.private_key` and
type your favorite password.
```
echo "favorite_password" > .private_key
```

The password is used to generate the root certificate. Now, you should see new certificates located
in `cert` folder which is located in the root directory.

<p align="center">
<img src="https://i.imgur.com/fZsI0kY.png"></p>

If you want to execute the server. Run
```
make serve
```

If you do all steps correctly. The server is running at `https://[YOUR-IP]:8721`. Now, you can change the
server ip in the application, see [here](https://github.com/ReceiptManager/Application).

<p align="center">
  <img src="https://i.imgur.com/xcwvmYa.png">
</p>

### Build using docker
The docker image is now available at https://hub.docker.com/repository/docker/monolidth/receipt-parser. You can `pull`
the image using `docker pull`. After you can run the image.
```
docker pull monolidth/receipt-parser:latest
docker run -p 8721:8721 monolidth/receipt-parser
```

<p align="center">
  <img src="https://i.imgur.com/xcwvmYa.png">
</p>


If you do all steps correctly. The server is running at `https://[YOUR-IP]:8721`. 

### Questions
If there any questions, bug or enhancements, please raise an issue or read my medium article about this. You can
find the article [here](https://medium.com/swlh/fuzzy-receipt-parser-and-manager-cb614e4eaa6a)
