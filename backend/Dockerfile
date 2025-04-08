FROM python:3.10-alpine AS builder

RUN mkdir /opt/srv
WORKDIR /opt/srv

COPY . .
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

RUN uv sync

#####################################################
#                    FINAL STAGE                    #
#####################################################
FROM python:3.10-alpine AS final

COPY --from=builder /opt/srv /opt/srv/
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

EXPOSE 8000

WORKDIR /opt/srv
ENTRYPOINT [ "uv", "run", "manage.py", "runserver", "0.0.0.0:8000" ]
