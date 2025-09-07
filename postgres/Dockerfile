FROM postgres:16-alpine
ENV POSTGRES_DB=cslibrary
ENV POSTGRES_USER=csuser
ENV POSTGRES_PASSWORD=change_me
COPY init.sql /docker-entrypoint-initdb.d/
COPY entrypoint.sh /usr/local/bin/pg-verbose-entrypoint.sh
RUN chmod +x /usr/local/bin/pg-verbose-entrypoint.sh
ENTRYPOINT ["/usr/local/bin/pg-verbose-entrypoint.sh"]
