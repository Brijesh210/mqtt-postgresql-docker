FROM python:3.8

ADD src/main/store_data.py .
ADD src/main/process_data.py .

ADD requirement.txt .

RUN pip install -r requirement.txt

ENTRYPOINT ["python", "./process_data.py"]

CMD ["Run docker image with argument as: docker run <image> <time_interval> <measurement>"]
