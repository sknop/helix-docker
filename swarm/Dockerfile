FROM sknop/perforce-base
MAINTAINER Sven Erik Knop <sknop@perforce.com>

# Install Helix Swarm 

RUN apt-get update && \
    apt-get install -y helix-swarm && \
    apt-get install -y helix-swarm-triggers

# Ensure environment variables are set up correctly

# Run shell script that does all the work
# -h is default, needs to have proper parameter to run against existing server

COPY SetupSwarm.py /

EXPOSE 80

ENTRYPOINT ["/SetupSwarm.py"]
CMD ["-h"]
