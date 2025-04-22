#####################################################
#                 DJANGO BUILD STAGE                #
#####################################################
FROM python:3.13-alpine AS djangobuild

COPY ./backend /opt/srv/
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

WORKDIR /opt/srv
RUN uv sync

#####################################################
#                  BUN BUILD STAGE                  #
#####################################################
FROM oven/bun:slim AS bunbuild

COPY ./frontend /opt/build/

WORKDIR /opt/build
RUN bun install
RUN bun run build
 
#####################################################
#                    FINAL STAGE                    #
#####################################################
FROM python:3.13-alpine AS final

COPY --from=djangobuild /opt/srv /opt/srv/
COPY --from=bunbuild /opt/build/dist/assets/ /opt/frontend/dist/assets/
COPY --from=bunbuild /opt/build/dist/index.html /opt/frontend/dist/
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

COPY ./backend/start.sh /opt/srv/start.sh
RUN chmod +x /opt/srv/start.sh

EXPOSE 8000

WORKDIR /opt/srv
CMD [ "sh", "/opt/srv/start.sh" ]