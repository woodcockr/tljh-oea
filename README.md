# tljh-oea
cd ~/dev/oea

docker run \
  --privileged \
  --detach \
  --name=tljh-dev \
  --publish 12000:80 \
  --mount type=bind,source=$(pwd),target=/srv/src \
  tljh-systemd

docker exec -it tljh-dev /bin/bash

python3 /srv/src/the-littlest-jupyterhub/bootstrap/bootstrap.py --admin admin --plugin /srv/src/tljh-oea