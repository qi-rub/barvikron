FROM andrewosh/binder-base
MAINTAINER Michael Walter <michael.walter@gmail.com>

USER root
RUN apt-get update

USER main
ADD .binder-requirements.txt requirements.txt
RUN /home/main/anaconda2/envs/python3/bin/pip install -r requirements.txt
