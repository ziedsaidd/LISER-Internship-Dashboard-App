FROM python:3.7.9-buster
WORKDIR /Theapp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ../Theapp .
CMD ["python", "app.py"]
