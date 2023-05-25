from python:3.11.3-slim-bullseye

RUN apt update && apt add curl unzip -y
WORKDIR /tmp
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip && ./aws/install
RUN rm -rf /tmp/*

RUN addgroup app --gid 10000 \
    && useradd app -d /opt -g app -s /bin/bash \
    && chown app:app /opt

USER app
WORKDIR /opt
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["./run.sh"]