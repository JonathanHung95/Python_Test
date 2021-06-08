FROM ubuntu:18.04

COPY ["requirements.txt", "exercise_1.py", "exercise_2.py", "get_data.sh", "input.yml", "run.sh", "Station Inventory EN.csv", "./"]
 
RUN apt update && apt-get install -y wget python3.8 python3-pip && pip3 install -r requirements.txt

ENTRYPOINT ["bash", "./run.sh"]
