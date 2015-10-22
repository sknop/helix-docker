# Basics
#
FROM sknop/perforce-base
MAINTAINER Sven Erik Knop <sknop@perforce.com>

# Install Helix Versioning Engine (P4D)

RUN apt-get update && apt-get install -y perforce-server

ENV P4PORT 1666
ENV P4ROOT /opt/perforce/servers/docker
ENV P4LOG log

EXPOSE ${P4PORT}

RUN mkdir -p ${P4ROOT}
RUN chown perforce:perforce ${P4ROOT}

# Volumes for server root

VOLUME ${P4ROOT}

USER perforce

COPY run.sh /
CMD ["/run.sh"]
