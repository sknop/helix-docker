# Basics
#
FROM ubuntu:14.04
MAINTAINER Sven Erik Knop <sknop@perforce.com>

# Install Helix Versioning Engine (P4D)

RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install -y wget
RUN wget -q https://package.perforce.com/perforce.pubkey -O - | apt-key add -
RUN echo "deb http://package.perforce.com/apt/ubuntu trusty release" > /etc/apt/sources.list.d/perforce.sources.list
RUN apt-get update && DEBIAN_FRONTEND="noninteractive" apt-get install -y perforce-server
RUN mkdir -p /p4/1
VOLUME /p4
# RUN /opt/perforce/sbin/configure-perforce-server.sh main -n -p 1666 -r /p4/1 -u perforce -P Password --unicode --case 1

EXPOSE 1666

CMD ["/opt/perforce/sbin/p4d", "-r/p4/1", "-p1666"]


# ENV CONTEXT_PATH ROOT
# COPY provision.bash /provision
# COPY launch.bash /launch

# RUN ["/provision"]

# Launching Helix

# WORKDIR /opt/jira
# CMD ["/launch"]
