# Welcome to the EstateIn project :house_with_garden:
## EstateIn is RestAPI of a real estate agency for Buenos Aires using FastAPI and MongoDB.

In this project I scrapped a platform of an agency, cleaned the data and uploaded it to a Cloud based NoSQL database. Then an API provides the data, the app is ready to go using Docker.

> :warning: *This project uses a .env file so you won't be able to connect to the DB*

# Steps to run the project using Docker
1. Clone the repo
2. Create a Docker image using:
    ```
    docker build -t estatein-api .
    ```
3. Run a Docker container:
    ```
    docker run -d --name estatein -p 5000:80 estatein-api
    ```
4. Go to 127.0.0.1:5000/ to read the API docs

# Steps to run the project without Docker

1. Clone the repo
2. Install the dependencies using:
```
pip install -r requirements.txt
```
3. In the terminal do the following:
```
uvicorn app:app --host 0.0.0.0 --port 5000
```
4. Go to 127.0.0.1:5000/ to read the API docs
