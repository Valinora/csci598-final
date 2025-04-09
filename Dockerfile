#####################################################
#                 DJANGO BUILD STAGE                #
#####################################################
FROM python:3.10-alpine AS djangobuild

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
RUN bun run build
 
#####################################################
#                    FINAL STAGE                    #
#####################################################
FROM python:3.10-alpine AS final

COPY --from=djangobuild /opt/srv /opt/srv/
COPY --from=bunbuild /opt/build/dist /opt/srv/reststop_rater/static/
COPY --from=ghcr.io/astral-sh/uv:0.6 /uv /uvx /bin/

EXPOSE 8000

WORKDIR /opt/srv
CMD [ "uv", "run", "manage.py", "runserver", "0.0.0.0:8000" ]
