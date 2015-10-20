FROM ubuntu:14.04
MAINTAINER Sven Erik Knop <george@mux.ro>

ENV DEBIAN_FRONTEND noninteractive

# Update package list and install wget
RUN apt-get update && apt-get install -y wget

# Preload perforce packages and install p4python (used for configuration)
RUN wget -q http://package.perforce.com/perforce.pubkey -O - | sudo apt-key add - && \
    echo 'deb http://package.perforce.com/apt/ubuntu trusty release' > /etc/apt/sources.list.d/perforce.sources.list && \
    apt-get update && \
    apt-get install -y perforce-p4python
