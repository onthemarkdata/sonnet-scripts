# syntax=docker/dockerfile:1.4

FROM --platform=$BUILDPLATFORM ubuntu:latest AS builder

# Set build arguments for cross-compilation
ARG TARGETPLATFORM
ARG BUILDPLATFORM

# Set environment variables for localization and timezone settings
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    TZ="America/Chicago" \
    DEBIAN_FRONTEND=noninteractive

# Update and install required packages for building
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    locales git curl wget vim bash unzip \
    gcc build-essential openssl ca-certificates && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

# (Optional) Insert cross-compilation-specific build commands here
# Example: RUN make CC=gcc TARGET=$TARGETARCH

# Final multi-platform image
FROM --platform=$TARGETPLATFORM ubuntu:latest

# Set environment variables again in the final stage
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    TZ="America/Chicago" \
    DEBIAN_FRONTEND=noninteractive

# Copy artifacts from builder stage if applicable
# COPY --from=builder /path/to/binary /usr/local/bin/

# Install runtime dependencies if necessary
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales ca-certificates && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]
