FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY . /app

RUN pip3 install -r requirements.txt

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]