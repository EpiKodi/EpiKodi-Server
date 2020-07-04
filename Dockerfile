FROM python:3.6.9

WORKDIR /home/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .