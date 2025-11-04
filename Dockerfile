FROM python:3.13-slim


COPY ./src/trinkgo ./trinkgo
COPY ./pyproject.toml ./

RUN apt update
RUN apt install -y jq
RUN pip3 install toml-cli
RUN pip3 install $(toml get --toml-path pyproject.toml project.dependencies | sed -e "s/[']/\"/g" | jq -r '.[]')
RUN pip3 install gunicorn

EXPOSE 443

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:443", "trinkgo.webapp.router:app"]
