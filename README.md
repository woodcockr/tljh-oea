# tljh-oea plugin

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

$ python3 /srv/src/the-littlest-jupyterhub/bootstrap/bootstrap.py --admin admin --plugin git+https://github.com/woodcockr/tljh-oea
```

# Install script for Cloud:
```
#!/bin/bash
curl -L https://tljh.jupyter.org/bootstrap.py \
  | sudo python3 - \
    --admin admin:foobar223 --plugin git+https://github.com/woodcockr/tljh-oea
postgres_password='superPassword'
odc_db_admin_password='insecurePassword'
odc_db_user_password='worrysomePassword'
bbox='146.8,-36.3,147.3,-35.8'
time_range='2021-06-01/2021-07-01'

# Start postgresql
systemctl enable postgresql
service postgresql restart

# Some guards in case running the install script repeatedly in same container. This will remove the database
su - postgres -c "psql -c 'DROP DATABASE IF EXISTS datacube;'"
su - postgres -c "psql -c 'DROP EXTENSION IF EXISTS postgis;'"
su - postgres -c "psql -c 'DROP ROLE IF EXISTS odc_db_admin;'"
su - postgres -c "psql -c 'DROP ROLE IF EXISTS odc_db_user;'"

# Configure postgres and create datacube database
su - postgres -c "psql -c 'CREATE EXTENSION postgis;'"
su - postgres -c "psql -c 'CREATE DATABASE datacube;'"
# The datacube system commands will require a postgres super user password
# and also the specification to use localhost for the database hostname
su - postgres -c "psql -c \"ALTER USER postgres PASSWORD '${postgres_password}';\""
su - postgres -c "source /opt/tljh/user/bin/activate && DB_HOSTNAME=localhost DB_USERNAME=postgres DB_PASSWORD=${postgres_password} DB_DATABASE=datacube datacube -v system init"
su - postgres -c "psql -c \"CREATE ROLE odc_db_admin WITH LOGIN IN ROLE agdc_admin, agdc_user ENCRYPTED PASSWORD '${odc_db_admin_password}';\""
su - postgres -c "psql -c \"CREATE ROLE odc_db_user WITH LOGIN IN ROLE agdc_user ENCRYPTED PASSWORD '${odc_db_user_password}';\""
su - postgres -c "psql -c 'ALTER DATABASE datacube OWNER TO odc_db_admin;'"

# initialise datacube database  default products
source /opt/tljh/user/bin/activate
export DB_HOSTNAME=localhost
export DB_USERNAME=odc_db_admin
export DB_PASSWORD=${odc_db_admin_password}
export DB_DATABASE=datacube
dc-sync-products https://raw.githubusercontent.com/woodcockr/tljh-oea/main/products.csv

# index default products
stac-to-dc --bbox=${bbox} --catalog-href='https://earth-search.aws.element84.com/v0/' --collections='sentinel-s2-l2a-cogs' --datetime=${time_range}
stac-to-dc --catalog-href='https://planetarycomputer.microsoft.com/api/stac/v1/' --collections='io-lulc'
stac-to-dc --bbox=${bbox} --catalog-href='https://planetarycomputer.microsoft.com/api/stac/v1/' --collections='nasadem'
```

As root user:
```
$ su postgres

postgres$ psql
postgres=# CREATE EXTENSION postgis;
postgres=# CREATE DATABASE datacube;


postgres=# quit


postgres$ source /opt/tljh/user/bin/activate
(base) postgres$ export DB_DATABASE=datacube
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

Login to Jupyter and create the ~/.datacube.conf file

.datacube.conf:
```
[datacube]
db_database: datacube

# A blank host will use a local socket. Specify a hostname (such as localhost) to use TCP.
# TCP will be necessary for most configurations as the default peer authentication will not work on a local socket without creating UNIX users
db_hostname: localhost

# Credentials are optional: you might have other Postgres authentication configured.
# The default username otherwise is the current user id.
db_username: odc_db_user
db_password: worrysomePassword

[datacube-admin]
db_database: datacube

# A blank host will use a local socket. Specify a hostname (such as localhost) to use TCP.
# TCP will be necessary for most configurations as the default peer authentication will not work on a local socket without creating UNIX users
db_hostname: localhost

# Credentials are optional: you might have other Postgres authentication configured.
# The default username otherwise is the current user id.
db_username: odc_db_admin
db_password: insecurePassword

```

## Add product definitions to database

```
dc-sync-products /srv/src/tljh-oea/products.csv
```
## Index data via terminal
```
stac-to-dc \
  --bbox='146.8,-36.3, 147.3, -35.8' \
  --catalog-href='https://earth-search.aws.element84.com/v0/' \
  --collections='sentinel-s2-l2a-cogs' \
  --datetime='2021-06-01/2021-07-01'

stac-to-dc \
  --catalog-href=https://planetarycomputer.microsoft.com/api/stac/v1/ \
  --collections='io-lulc'

stac-to-dc \
  --catalog-href='https://planetarycomputer.microsoft.com/api/stac/v1/' \
  --collections='nasadem' \
  --bbox='146.8,-36.3, 147.3, -35.8'
```

# NOTES:

hub python environment is at /opt/tljh/opt - this is where the tljh-oea plugin package is installed

