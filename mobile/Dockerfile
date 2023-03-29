FROM openjdk:11

WORKDIR /app
COPY ./Main.java ./

# RUN javac Main.java
RUN javac Client.java

COPY startup.sh .
RUN chmod +x startup.sh

CMD ["./startup.sh"]

