FROM python:3.7.9-buster
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./ .
#CMD [ "python", "app.py" ]
CMD ["gunicorn", "-b", "0.0.0.0", "app:server"]
#CMD ["gunicorn", "app:server"]
