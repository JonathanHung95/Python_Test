FROM ubuntu:18.04

RUN apt update
RUN apt-get install -y python3.8 python3-pip 
RUN pip install -r requirements.txt

CMD ["./run.sh"]