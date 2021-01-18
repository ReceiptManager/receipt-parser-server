FROM python:3
FROM tensorflow/tensorflow:nightly-py3

RUN apt-get update -y && apt-get upgrade -y 
RUN apt-get install -y tesseract-ocr-all libgl1-mesa-glx libmagickwand-dev

WORKDIR /app
COPY . .

RUN mkdir -p /app/data/img
RUN mkdir -p /app/data/tmp
RUN mkdir -p /app/data/training
RUN mkdir -p /app/data/txt

RUN echo $(tr -dc A-Za-z0-9 </dev/urandom | head -c 13 ; echo '') > /app/.api_token

RUN pip install -r requirements.txt --verbose
RUN make generate_cert
CMD ["make", "serve"]
