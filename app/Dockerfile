FROM python:3.6.12-alpine as builder

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "UpdateTableRank.py"]
