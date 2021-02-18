# s0nar
Anomaly detection service 🔎👻

## Deployment notes
First of all, download the .env vars for production deployment at following link:

* s3://s0nar/env/master/.env 

Create s0nar API and workers images
```sh
docker-compose build --no-cache .   # In project's root folder
```
Then start all containers using docker-compose, except **LSTM-GPU worker**:
```sh
docker-compose up -d api mongodb rabbitmq flower arima-worker lstm-cpu-worker
```

We don't start the gpu worker because docker-compose has no support for nvidia-docker flags, then:
```sh
docker run --name lstm-gpu-worker --gpus all s0nar_lstm-gpu-worker:latest
```
Embedded postman collection:
[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/952e9b0d1413f01f77c3#?env%5Bs0nar%5D=W3sia2V5IjoiaG9zdCIsInZhbHVlIjoibG9jYWxob3N0IiwiZW5hYmxlZCI6dHJ1ZX0seyJrZXkiOiJwb3J0IiwidmFsdWUiOiI1MDA0IiwiZW5hYmxlZCI6dHJ1ZX0seyJrZXkiOiJhcGlfdmVyc2lvbiIsInZhbHVlIjoidjEiLCJlbmFibGVkIjp0cnVlfSx7ImtleSI6ImRhdGFzZXRfaWQiLCJ2YWx1ZSI6ImZjZjk1N2FjLTVjNmUtNGZhMi1iNzkxLWRiYTYyNzI5OGUxMSIsImVuYWJsZWQiOnRydWV9LHsia2V5IjoibW9kZWxfaWQiLCJ2YWx1ZSI6ImZlYjk0Y2E3LWQ3ZDMtNGJmOS04YWI2LWY3Y2UyODU5OTQ2MyIsImVuYWJsZWQiOnRydWV9LHsia2V5IjoicmVwb3J0X2lkIiwidmFsdWUiOiI5NjZmNjgyNi0yM2RjLTQxZmYtYTk3ZC02ZGRmMWVjMDVmYWEiLCJlbmFibGVkIjp0cnVlfSx7ImtleSI6IngtYXBpLWtleSIsInZhbHVlIjoiYjVlYThlMTNmMTBkNDZjOWFlMzNiMzkyYmI2ZDc0ZGU5YzI0ZTNhOTFmZTQ0YmIiLCJlbmFibGVkIjp0cnVlfSx7ImtleSI6ImRhdGFzZXQiLCJ2YWx1ZSI6ImF3cy9idWNrZXRzL2JyYWluLWlvdC9kYXRhc2V0cy9pbnRlcm5hbC9FTUFMQ1NBX3dhdGVyX2RhbS8xLlZlcnNpb25fd2l0aF9jbGltYXRlL3RlbHZhX2RhdGFzZXQuY3N2IiwiZW5hYmxlZCI6dHJ1ZX1d)

First, establish the env vars and deploy mongodb and rabbitmq (and flower if you want to track the celery task)
```sh
cp .env.sample .env # maybe you need to update these variables
docker-compose up -d mongodb rabbitmq flower
``` 
Then start **s0nar service**
```sh
python app.py
```
Finally, start the workers:

* **auto-arima** worker
```sh
celery --app=project.ml_task.celery_app worker -l INFO -n worker.arima -Q arima -c 1
```

* **LSTM-CPU** worker
```sh
celery --app=project.ml_task.celery_app worker -l INFO -n worker.lstm-cpu -Q lstm-cpu -c 1
```

* **LSTM-CPU** worker
```sh
celery --app=project.ml_task.celery_app worker -l INFO -n worker.lstm-gpu -Q lstm-gpu -c 1
```

Once both services are running you can test it using postman or cURL.

## Development requirements
* python >=3.5 (using conda, virtenv, etc, it doesn't matter )
* pip3
* docker
* docker-compose
* cURL or Postman
