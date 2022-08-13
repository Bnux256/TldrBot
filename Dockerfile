FROM python:3.10-alpine
WORKDIR /usr/src/app
RUN pip install -U pip
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt
ADD . .
CMD ["python3", "main.py"]