FROM linuxbase AS pythonbase

RUN mkdir /apps

# Set build arguments for cross-compilation
ARG TARGETARCH

# Set environment variables
ENV PATH=/venv/bin:$PATH \
    PATH=/root/.cargo/bin:$PATH \
    PATH="/root/.local/bin/:$PATH"

# Install uv, curl, and the PostgreSQL client (`psql`)
RUN apt-get update && apt-get install -y ca-certificates curl postgresql-client unzip make

# Download UV and MinIO Client (mc) based on architecture
RUN if [ "$TARGETARCH" = "amd64" ]; then \
        curl -LsSf https://astral.sh/uv/install.sh | sh \
        && curl -O https://dl.min.io/client/mc/release/linux-amd64/mc \
        && chmod +x mc \
        && mv mc /usr/local/bin/; \
    elif [ "$TARGETARCH" = "arm64" ]; then \
        curl -LsSf https://astral.sh/uv/install.sh | sh \
        && curl -O https://dl.min.io/client/mc/release/linux-arm64/mc \
        && chmod +x mc \
        && mv mc /usr/local/bin/; \
    else \
        echo "Unsupported architecture: $TARGETARCH" && exit 1; \
    fi

# Install DuckDB
ARG DUCKDB_VERSION="v1.2.2"

RUN set -eux; \
    apt-get update && apt-get install -y --no-install-recommends \
        curl ca-certificates gzip && \
    rm -rf /var/lib/apt/lists/* && \
    # pick the correct pre‑built binary for the platform
    if [ "$TARGETARCH" = "amd64" ]; then \
        DUCKDB_DIST="linux-amd64"; \
    elif [ "$TARGETARCH" = "arm64" ]; then \
        DUCKDB_DIST="linux-arm64"; \
    else \
        echo "Unsupported architecture: $TARGETARCH" && exit 1; \
    fi && \
    curl -fsSL "https://github.com/duckdb/duckdb/releases/download/${DUCKDB_VERSION}/duckdb_cli-${DUCKDB_DIST}.gz" \
      | gunzip -c > /usr/local/bin/duckdb && \
    chmod +x /usr/local/bin/duckdb && \
    duckdb --version   # quick sanity check

# Set up a virtual env to use for whatever app is destined for this container.
RUN uv venv --python 3.12.6 /venv && \
    echo "\nsource /venv/bin/activate\n" >> /root/.zshrc && \
    uv --version

# Copy application-specific files
COPY requirements.txt /apps/requirements.txt

# Run install of requirements
RUN . /venv/bin/activate && \
    uv pip install --upgrade -r /apps/requirements.txt && \
    uv pip install --upgrade granian[pname]

RUN echo "We're good:" && \
    /venv/bin/python --version

CMD ["/bin/bash", "-c", "trap 'exit 0' SIGTERM; while true; do sleep 1; done"]