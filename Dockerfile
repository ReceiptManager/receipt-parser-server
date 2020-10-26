FROM python:3
FROM tensorflow/tensorflow:nightly-py3
RUN apt-get update -y && apt-get upgrade -y 
RUN apt-get install -y tesseract-ocr-all

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt --verbose
RUN make generate_cert
CMD ["make", "serve"]
