FROM docker.arvancloud.ir/ubuntu:22.04

LABEL maintainer="abolfazlkameli0@gmail.com"

ENV PYTHONBUFFERED=1

WORKDIR /PetShop/

COPY ../requirements.txt /PetShop/

RUN apt-get update &&\
    apt-get install python3 python3-pip -y &&\
    apt-get clean

RUN pip3 install --no-cache-dir -r requirements.txt

COPY .. /PetShop/

RUN chmod +x /PetShop/docker/entrypoint.sh
ENTRYPOINT ["bash", "-c", "/PetShop/docker/entrypoint.sh"]
