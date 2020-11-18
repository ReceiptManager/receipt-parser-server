<p align="center">
<img src="https://miro.medium.com/max/700/1*VfeXSnc08x6BTCbPNPCfIg.jpeg">
</p>

# ReceiptManger server
The server parses the receipt via tesseract which is a very hard task.
The main problem is the image quality of the smartphone camera. 
To tackle this issue, I enhance the image using a variety of techniques. 
First, I resize the image.

<p align="center">
<img src="https://miro.medium.com/max/700/1*bC0DxIy-W0l-mtuesaCe3g.png"></p

Where FX and FY describes the scaling factor of the image.
In this case, INTER_CUBIC generally performs better than other alternatives, though it’s also slower than others. 
Since we care about quality I do not use the INTER_LINEAR.

What got the ball rolling was the gaussian blurring which uses the Gaussian kernel instead of a normalized box filter, for convolution.
In our case, the dimensions of the kernel and the standard deviations in both directions can be determined independently. 
It is very useful to remove noise from the image thus it does not preserve the edges in the input.

To remove the salt and peppter noise in the image. I applied a median blurring. 
The central element in the kernel area is replaced with the median of all the pixels under the kernel.

After, I use convert to increase the contrast. 
This is very important since it massively increase the outcome but this is covered in the receipt parser library.

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

If you have not pip installed. Use `apt-get install python python-pip`.
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
The docker image is currently tested. There might be some bugs present at the moment. However, the installation is much simpler.
First, check if docker is running
```
systemctl status docker
```

<p align="center">
<img src="https://i.imgur.com/OSqiDh8.png"></p>

Now clone the server repository.
```
git clone https://github.com/ReceiptManager/Server
```

Navigate in the `server` directory and generate an new file called `.private_key` and
type your favorite password (please replace favorite_password with something stronger).
```
cd Server
echo "favorite_password" > .private_key
```

Create an docker `image`
```
make docker-build
```

If it is successfull. You can run the docker image
```
docker run -p 8721:8721 monolidth/receipt-parser-server
```

<p align="center">
  <img src="https://i.imgur.com/xcwvmYa.png">
</p>


If you do all steps correctly. The server is running at `https://[YOUR-IP]:8721`.
There might be an image on docker hub in the future, thus at the moment it is required to build the image manual.

### Questions
If there any questions, bug or enhancements, please raise an issue or read my medium article about this. You can
find the article [here](https://medium.com/swlh/fuzzy-receipt-parser-and-manager-cb614e4eaa6a)
