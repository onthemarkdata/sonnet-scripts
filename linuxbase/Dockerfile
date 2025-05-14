FROM --platform=$BUILDPLATFORM alpine:3.18 AS builder

# Set build arguments for cross-compilation
ARG TARGETPLATFORM
ARG BUILDPLATFORM
ARG TARGETARCH
RUN echo "Sonnet Scripts running on $BUILDPLATFORM, building for $TARGETPLATFORM"

# Set environment variables for localization and timezone settings
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    TZ="America/Chicago"

# Install minimal build dependencies
RUN apk add --no-cache \
    ca-certificates openssl \
    git curl wget bash unzip \
    build-base libc6-compat gcc musl-dev && \
    rm -rf /var/lib/apk/lists/*

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
    locales ca-certificates && \
    locale-gen en_US.UTF-8 && \
    rm -rf /var/lib/apt/lists/*

CMD ["/bin/bash"]
