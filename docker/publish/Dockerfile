FROM python:3.8

ADD src/main/publish_data.py .

ADD requirement.txt .

RUN pip install -r requirement.txt

CMD ["python", "./publish_data.py"]
