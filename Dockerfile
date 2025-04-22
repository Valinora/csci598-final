#####################################################
#                 DJANGO BUILD STAGE                #
#####################################################
FROM python:3.13-alpine AS djangobuild

COPY . /opt/srv/
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

COPY start.sh /opt/srv/start.sh
RUN chmod +x /opt/srv/start.sh

WORKDIR /opt/srv
RUN uv sync

EXPOSE 8000

CMD [ "sh", "/opt/srv/start.sh" ]