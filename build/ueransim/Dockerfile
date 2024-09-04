FROM ueransim_image:latest

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --install-recommends \
      net-tools \
      iproute2 && \
    apt-get clean
