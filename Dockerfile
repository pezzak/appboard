FROM python:2.7-alpine

EXPOSE 8000

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev

RUN mkdir -p /app/
WORKDIR /app/

COPY requirements*.txt /app/
RUN pip install -r requirements-docker.txt

COPY . /app
RUN chmod 755 /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["app:start"]
