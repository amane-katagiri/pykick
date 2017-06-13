FROM python:3-alpine
MAINTAINER Amane Katagiri
CMD [""]
ENTRYPOINT ["pykick"]
WORKDIR /app
COPY . /app
RUN pip install -e .
WORKDIR /app/pykick/example
