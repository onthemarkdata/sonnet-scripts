FROM python:3.12

# Set environment variables for localization and timezone settings
ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8 \
    TZ="America/Chicago" \
    DEBIAN_FRONTEND=noninteractive

RUN mkdir /apps

# Set build arguments for cross-compilation
ARG TARGETARCH
ARG DUCKDB_VERSION="v1.2.2"

# Set environment variables
ENV PATH=/root/.local/bin:/venv/bin:$PATH

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client gzip curl && \
    rm -rf /var/lib/apt/lists/*

# Install UV (Python package manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install MinIO client (architecture-specific)
RUN if [ "$TARGETARCH" = "amd64" ]; then \
        curl -O https://dl.min.io/client/mc/release/linux-amd64/mc; \
    elif [ "$TARGETARCH" = "arm64" ]; then \
        curl -O https://dl.min.io/client/mc/release/linux-arm64/mc; \
    else \
        echo "Unsupported architecture: $TARGETARCH" && exit 1; \
    fi && \
    chmod +x mc && \
    mv mc /usr/local/bin/mc

# Install DuckDB CLI (architecture-specific)
RUN if [ "$TARGETARCH" = "amd64" ]; then \
        DUCKDB_DIST="linux-amd64"; \
    elif [ "$TARGETARCH" = "arm64" ]; then \
        DUCKDB_DIST="linux-arm64"; \
    else \
        echo "Unsupported architecture: $TARGETARCH" && exit 1; \
    fi && \
    curl -fsSL "https://github.com/duckdb/duckdb/releases/download/${DUCKDB_VERSION}/duckdb_cli-${DUCKDB_DIST}.gz" \
        | gunzip -c > /usr/local/bin/duckdb && \
    chmod +x /usr/local/bin/duckdb && \
    duckdb --version

# Create Python virtual environment
RUN uv venv --python 3.12.6 /venv && \
    /venv/bin/python --version

# Run install of requirements
COPY requirements.txt /apps/requirements.txt
RUN uv pip install --upgrade -r /apps/requirements.txt

# Keep container running for interactive use
CMD ["tail", "-f", "/dev/null"]
