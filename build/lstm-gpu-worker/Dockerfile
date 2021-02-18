FROM tensorflow/tensorflow:2.1.0-gpu-py3
LABEL maintainer="Luis Lorenzo <luislm@improvingmetrics.com>"

# Upgrade pip
RUN pip install pip --upgrade

# Copy s0nar's code
ENV HOME /home/im/s0nar
COPY . ${HOME}
WORKDIR ${HOME}

# Install python dependencies
RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install -r build/ml_requirements.txt

# Run celery worker
CMD celery --app=src.celery.lstm_task worker -l INFO -n worker.lstm-gpu -Q lstm-gpu -c 1