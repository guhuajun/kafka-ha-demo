FROM python:3-alpine

WORKDIR /app/

RUN pip install kafka-python \
        --index-url http://mirrors.aliyun.com/pypi/simple/ \
        --trusted-host mirrors.aliyun.com

COPY producer.py .

CMD ["python", "producer.py"]