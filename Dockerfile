FROM python:3.13-slim


COPY ./src ./src
COPY ./pyproject.toml ./

RUN pip3 install .
RUN pip3 install gunicorn

EXPOSE 443

ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:443", "trinkgo.webapp.router:app"]
