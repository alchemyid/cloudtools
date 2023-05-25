from python:3.11.3-slim-bullseye

RUN apt update && apt install curl unzip -y
WORKDIR /tmp
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip && ./aws/install
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
RUN chmod +x kubectl && mv kubectl /usr/local/bin/
RUN rm -rf /tmp/*

RUN addgroup app --gid 10000 \
    && useradd app -d /opt -g app -s /bin/bash \
    && chown app:app /opt

USER app
WORKDIR /opt
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["./run.sh"]