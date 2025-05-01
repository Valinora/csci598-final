#####################################################
#                 DJANGO BUILD STAGE                #
#####################################################
FROM python:3.13-alpine AS djangobuild

RUN set -eux;\
    apk update;\
    apk add nginx;

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY nginx.conf /etc/nginx/nginx.conf
COPY . /opt/srv/
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/


WORKDIR /opt/srv

EXPOSE 8000

CMD [ "sh", "start.sh" ]
