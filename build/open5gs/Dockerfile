FROM open5gs_image:latest

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --install-recommends \
      gettext && \
    apt-get clean
