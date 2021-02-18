FROM fnndsc/ubuntu-python3
LABEL maintainer="Luis Lorenzo <luislm@improvingmetrics.com>"

ENV LANG C.UTF-8

# Upgrade python packages
RUN pip install pip --upgrade

# Copy s0nar's code
ENV HOME /home/im/s0nar
COPY . ${HOME}
WORKDIR ${HOME}

# Install dependencies
RUN python3 -m pip install -r requirements.txt
