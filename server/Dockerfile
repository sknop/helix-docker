# Basics
#
FROM sknop/perforce-base
MAINTAINER Sven Erik Knop <sknop@perforce.com>

# Install Helix Versioning Engine (P4D)

RUN apt-get update && apt-get install -y perforce-server

# Volumes for server roots and triggers
VOLUME /p4

ENV P4PORT 1666 

EXPOSE 1666

COPY run.sh /
CMD ["/run.sh"]
