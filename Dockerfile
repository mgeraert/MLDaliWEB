FROM python:3.8


WORKDIR /MLDaliWeb
COPY . /MLDaliWeb

# INSTALL FLASK
RUN pip install Flask==0.12
RUN pip install flask_login==0.4.1
RUN pip install flask_sqlalchemy==2.5.1
run pip install pyserial==3.4
run pip install GitPython==3.1.24

ENTRYPOINT ["python"]

CMD ["__init__.py"]

# docker image build -t reval-test .
# docker run -v C:\Coding\reval-database:/reval-equip/database -p 5000:5000 -d reval-test



#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #
# ssh root@<IPV4_ADDRESS>
# sudo curl   -sSL   -o /usr/bin/docker-volume-plugin-dostorage   https://github.com/omallo/docker-volume-plugin-dostorage/releases/download/v0.4.0/docker-volume-plugin-dostorage_linux_amd64
# sudo chmod +x /usr/bin/docker-volume-plugin-dostorage
# sudo docker-volume-plugin-dostorage --access-token=<TOKEN_FROM_DIGITAL_OCEAN> &
# sudo service docker restart
# sudo mkfs.ext4 /dev/disk/by-id/scsi-0DO_Volume_volume-reval
# docker volume create --driver dostorage --name volume-reval
# git clone https://github.com/deenr/reval-equip.git app
# cd app
# docker image build -t reval-build .
# docker run --name reval-container -v volume-reval:/reval-equip/database -p 5000:5000 -d reval-build
# docker ps
# docker volume inspect volume-reval



# df -h
# docker logs <name>
# docker exec -ti <name> sh
#  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #  #