FROM ubuntu:latest
LABEL authors="mlubn"

ENTRYPOINT ["top", "-b"]