celery --app=src.celery.auto_arima_task worker -l INFO -n worker.arima -Q arima -c 1

# celery multi start worker arima lstm-worker -c 2 # TODO: research
# flower --broker=amqp://admin:t00r@localhost:5672/training