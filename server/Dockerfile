# Basics
#
FROM sknop/perforce-base
MAINTAINER Sven Erik Knop <sknop@perforce.com>

# Install Helix Versioning Engine (P4D)

RUN apt-get update && apt-get install -y perforce-server

ENV P4PORT 1666
ENV P4ROOT /p4

EXPOSE ${P4PORT}

# Volumes for server root
VOLUME ${P4ROOT}

COPY run.sh /
CMD ["/run.sh"]
