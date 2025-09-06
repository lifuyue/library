FROM postgres:16-alpine
ENV POSTGRES_DB=cslibrary
ENV POSTGRES_USER=csuser
ENV POSTGRES_PASSWORD=change_me
COPY init.sql /docker-entrypoint-initdb.d/
