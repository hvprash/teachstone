# Source image
FROM ubuntu:22.04

# Create mytest user
RUN useradd -d /home/mytest -m -s /bin/bash mytest

# Set working dir
WORKDIR '/home/mytest'

# COPY files
COPY . /home/mytest

# Install packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    supervisor 

RUN pip3 install -r requirements.txt

# Install report-generator
COPY report-generator.py /usr/local/bin/report-generator
RUN chown mytest /usr/local/bin/report-generator
RUN chmod 755 /usr/local/bin/report-generator

# Set supervisord entrypoint
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ENTRYPOINT ["/usr/bin/supervisord"]
