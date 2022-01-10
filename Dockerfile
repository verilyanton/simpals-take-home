FROM python:3.7

EXPOSE 8888

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

ENTRYPOINT ["python3", "app.py"]
