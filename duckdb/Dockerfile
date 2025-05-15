FROM linuxbase

# Set build arguments explicitly
ARG DUCKDB_VERSION="v1.2.2"
ARG TARGETARCH

# Install architecture-specific DuckDB CLI binary
RUN set -eux; \
    if [ "$TARGETARCH" = "amd64" ]; then \
        DUCKDB_DIST="linux-amd64"; \
        curl -LO https://github.com/duckdb/duckdb/releases/download/${DUCKDB_VERSION}/duckdb_cli-${DUCKDB_DIST}.zip && \
        unzip duckdb_cli-${DUCKDB_DIST}.zip -d /usr/local/bin && \
        rm duckdb_cli-${DUCKDB_DIST}.zip; \
    elif [ "$TARGETARCH" = "arm64" ]; then \
        DUCKDB_DIST="linux-arm64"; \
        curl -LO https://github.com/duckdb/duckdb/releases/download/${DUCKDB_VERSION}/duckdb_cli-${DUCKDB_DIST}.gz && \
        gunzip duckdb_cli-${DUCKDB_DIST}.gz && \
        mv duckdb_cli-${DUCKDB_DIST} /usr/local/bin/duckdb; \
    else \
        echo "Unsupported architecture: $TARGETARCH"; exit 1; \
    fi && \
    chmod +x /usr/local/bin/duckdb && \
    duckdb --version

# Explicitly copy the DuckDB initialization script for automatic setup
COPY init.sql /init.sql

# Expose the correct DuckDB UI port explicitly (4213)
EXPOSE 4213

# Explicitly keep the container running persistently
CMD ["tail", "-f", "/dev/null"]