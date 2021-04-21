FROM fnndsc/ubuntu-python3
LABEL maintainer="Luis Lorenzo <luislm@improvingmetrics.com>"

ENV LANG C.UTF-8

# Upgrade python packages
RUN pip install pip --upgrade

# Install dependencies
ENV HOME /home/im/s0nar
WORKDIR ${HOME}
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

# Copy s0nar's code
COPY . ${HOME}
