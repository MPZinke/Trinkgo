FROM golang:1.26-bookworm AS builder

RUN apt update
RUN apt install -y git
RUN git clone --depth 1 https://github.com/MPZinke/typescript-jinja.git /typescript-jinja
WORKDIR /typescript-jinja
RUN go build -o tsgo ./cmd/tsgo

WORKDIR /usr
COPY ./src src
COPY ./tsconfig.json tsconfig.json
RUN /typescript-jinja/tsgo


# ---------------------- #

FROM python:3.13-slim

RUN apt update
RUN apt install -y jq
RUN pip3 install gunicorn
RUN pip3 install toml-cli

COPY ./pyproject.toml ./
RUN pip3 install $(toml get --toml-path pyproject.toml project.dependencies | sed -e "s/[']/\"/g" | jq -r '.[]')

COPY --from=builder ./src/trinkgo ./trinkgo

EXPOSE 443

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:443", "trinkgo.webapp.router:app"]
