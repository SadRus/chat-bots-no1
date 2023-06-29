FROM python:3
LABEL maintainer='sadrus'

WORKDIR /docker-chat-bots-no1
COPY requirements.txt /docker-chat-bots-no1/
RUN pip install -r requirements.txt

COPY main.py /docker-chat-bots-no1/
RUN chmod a+x *.py

ENTRYPOINT ["python3"]
CMD ["./main.py"]
