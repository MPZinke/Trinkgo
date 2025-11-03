FROM python:3.13-slim


COPY ./source /usr/local/bin/trinkgo
COPY ./requirements.txt /usr/local/bin/trinkgo/
WORKDIR /usr/local/bin/trinkgo/


RUN pip3 install -r requirements.txt


ENTRYPOINT ["python3", "/usr/local/bin/trinkgo"]
