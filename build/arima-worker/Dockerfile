FROM fnndsc/ubuntu-python3
LABEL maintainer="Luis Lorenzo <luislm@improvingmetrics.com>"

ENV LANG C.UTF-8

# Upgrade python packages
RUN pip install pip --upgrade

# Install dependencies
ENV HOME /home/im/s0nar_arima_worker
WORKDIR ${HOME}

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY build/ml_requirements.txt build/
RUN python3 -m pip install -r build/ml_requirements.txt

COPY build/arima-worker/custom_requirements.txt build/arima-worker/
RUN python3 -m pip install -r build/arima-worker/custom_requirements.txt

# Copy s0nar's code
COPY . ${HOME}
