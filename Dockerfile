FROM debian

WORKDIR /app

COPY main.py requirements.txt utils.py /data/

RUN apt-get update && apt-get install -y python3-pip

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]