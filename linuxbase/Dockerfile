FROM ubuntu:latest

# Set environment variables for localization and timezone settings
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    TZ="America/Chicago" \
    DEBIAN_FRONTEND=noninteractive

# Update and install required packages including ca-certificates
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    locales git curl wget vim bash \
    gcc build-essential openssl ca-certificates && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]