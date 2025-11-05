FROM python:3.13-slim

RUN apt update
RUN apt install -y jq
RUN pip3 install gunicorn
RUN pip3 install toml-cli

COPY ./pyproject.toml ./
RUN pip3 install $(toml get --toml-path pyproject.toml project.dependencies | sed -e "s/[']/\"/g" | jq -r '.[]')

COPY ./src/trinkgo ./trinkgo

EXPOSE 443

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:443", "trinkgo.webapp.router:app"]
