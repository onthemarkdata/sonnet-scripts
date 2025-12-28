FROM ubuntu:24.04

# Set environment variables for localization and timezone settings
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    TZ="America/Chicago" \
    DEBIAN_FRONTEND=noninteractive

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales ca-certificates make git curl && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]
