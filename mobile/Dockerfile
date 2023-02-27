FROM ubuntu:20.04

RUN apt-get update && apt-get install -y default-jdk
WORKDIR /app
COPY ./Main.py ./

COPY startup.sh .
RUN chmod +x startup.sh

CMD ["./startup.sh"]

