# FROM ubuntu:20.04
FROM python:3

WORKDIR /app
COPY ./ ./

COPY startup.sh .
RUN chmod +x startup.sh

CMD ["./startup.sh"]

