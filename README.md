# tljh-oea

To use this in dev clone the tljh (https://github.com/jupyterhub/the-littlest-jupyterhub alongside this tljh-oea repo into a directory `oea`

```console
$ cd ~/dev/oea/the-littlest-jupyterhub

$ docker build -t tljh-systemd . -f integration-tests/Dockerfile

$ cd ~/dev/oea

$ docker run \
  --privileged \
  --detach \
  --name=tljh-dev \
  --publish 12000:80 \
  --mount type=bind,source=$(pwd),target=/srv/src \
  tljh-systemd

$ docker exec -it tljh-dev /bin/bash

$ python3 /srv/src/the-littlest-jupyterhub/bootstrap/bootstrap.py --admin admin --plugin /srv/src/tljh-oea

$ service postgresql start
$ update-rc.d postgresql enable
```

As admin user:

```
$ su postgres

postgres$ psql

postgres=# CREATE DATABASE datacube;
postgres=# CREATE EXTENSION postgis;

postgres=# quit


postgres$ source /opt/tljh/user/bin/activate
### Either create a temporary .datacube.conf or and ENV vars for DB_DATABASE. Sample datacube.conf further down.
### comment out username and password whilst using the postgres superuser to initialise the database
(base) postgres$ vim .datacube.conf
(base) postgres$ datacube -v system init
Initialising database...
Created.
Checking indexes/views.
Done.
(base) postgres# psql

postgres=# CREATE ROLE odc_db_admin WITH LOGIN IN ROLE agdc_admin, agdc_user ENCRYPTED PASSWORD 'asecurepassword';
postgres=# CREATE ROLE odc_db_user WITH LOGIN IN ROLE agdc_user ENCRYPTED PASSWORD 'anothersecurepassword';
postgres=# ALTER DATABASE datacube OWNER TO odc_db_admin;
postgres=# quit
```

datacube.conf:
```
[datacube]
db_database: datacube

# A blank host will use a local socket. Specify a hostname (such as localhost) to use TCP.
# TCP will be necessary for most configurations as the default peer authentication will not work on a local socket without creating UNIX users
db_hostname: localhost

# Credentials are optional: you might have other Postgres authentication configured.
# The default username otherwise is the current user id.
# db_username: odc_db_user
# db_password: anothersecurepassword

[datacube-admin]
db_database: datacube

# A blank host will use a local socket. Specify a hostname (such as localhost) to use TCP.
# TCP will be necessary for most configurations as the default peer authentication will not work on a local socket without creating UNIX users
db_hostname: localhost

# Credentials are optional: you might have other Postgres authentication configured.
# The default username otherwise is the current user id.
# db_username: odc_db_admin
# db_password: asecurepassword

```

