FROM python:3.6.14-stretch

WORKDIR /app
COPY . .

RUN pip install --upgrade pip setuptools==45.2.0 && \
    pip install -r requirements.pip 

EXPOSE 5000

CMD ["todo.py"]
ENTRYPOINT ["python3"]

