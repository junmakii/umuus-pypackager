

FROM python:3.7-alpine

MAINTAINER Jun Makii <junmakii@gmail.com>

RUN apk update
RUN apk add --no-cache ca-certificates
RUN python3 -m ensurepip
RUN pip3 install --upgrade --no-cache-dir pip setuptools
ADD . /app
WORKDIR /app
RUN pip install -U .

CMD ["python", "-m", "umuus-pypackager"]

