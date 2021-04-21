FROM tensorflow/tensorflow:2.1.0-py3
LABEL maintainer="Luis Lorenzo <luislm@improvingmetrics.com>"

# Upgrade pip
RUN pip install pip --upgrade

# Install python dependencies
ENV HOME /home/im/s0nar
WORKDIR ${HOME}

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY build/ml_requirements.txt build/
RUN python3 -m pip install -r build/ml_requirements.txt

# Copy s0nar's code
COPY . ${HOME}

# Run celery worker
CMD celery --app=src.celery.lstm_task worker -l INFO -n worker.lstm-cpu -Q lstm-cpu -c 1