FROM python:3.7

RUN apt-get update -y && apt-get upgrade -y 
RUN apt-get install -y tesseract-ocr-all libgl1-mesa-glx libmagickwand-dev
RUN apt-get install -y qrencode

WORKDIR /app
COPY . .
COPY /tessdata/* /usr/share/tesseract-ocr/4.00/tessdata

RUN mkdir -p /app/data/img
RUN mkdir -p /app/data/tmp
RUN mkdir -p /app/data/training
RUN mkdir -p /app/data/txt

RUN pip install -r requirements.txt
CMD ["make", "serve"]
