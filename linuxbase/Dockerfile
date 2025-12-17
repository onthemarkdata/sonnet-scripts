FROM --platform=$BUILDPLATFORM ubuntu:24.04 AS builder

# Set build arguments for cross-compilation
ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETARCH
RUN echo "Sonnet Scripts running on $BUILDPLATFORM, building for $TARGETPLATFORM"

# Set environment variables for localization and timezone settings
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    TZ="America/Chicago" \
    DEBIAN_FRONTEND=noninteractive

# Update and install required packages for common build dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
    locales git curl wget vim bash unzip \
    gcc build-essential openssl ca-certificates && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

# (Placeholder) Insert cross-compilation-specific build commands here
# RUN if [ "$TARGETARCH" = "arm64" ]; then \
#       echo "Compiling ARM-specific binaries..."; \
#     elif [ "$TARGETARCH" = "amd64" ]; then \
#       echo "Compiling AMD-specific binaries..."; \
#     fi

# Final multi-platform image
FROM --platform=$TARGETPLATFORM ubuntu:24.04

# Copy artifacts from builder stage if applicable
COPY --from=builder /bin/bash /usr/local/bin/

# Install runtime dependencies if necessary
RUN apt-get update && apt-get install -y --no-install-recommends \
    locales ca-certificates make git && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]
