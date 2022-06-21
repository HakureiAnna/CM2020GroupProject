FROM mysql:5.7
ENV MYSQL_DATABASE=caldowndb
ENV MYSQL_ROOT_PASSWORD=p@ssw0rd!
COPY ./dbserver/scripts /docker-entrypoint-initdb.d