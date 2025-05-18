FROM linuxbase

ARG DUCKDB_VERSION="v1.2.2"
ARG TARGETARCH

RUN mkdir /apps

RUN set -eux; \
    apt-get update && apt-get install -y curl unzip gzip && \
    if [ "$TARGETARCH" = "amd64" ]; then \
        DUCKDB_DIST="linux-amd64"; \
        curl -LO https://github.com/duckdb/duckdb/releases/download/${DUCKDB_VERSION}/duckdb_cli-${DUCKDB_DIST}.zip && \
        unzip duckdb_cli-${DUCKDB_DIST}.zip -d /usr/local/ && \
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

# RUN set -eux; \
#     apt-get update && apt-get install -y curl unzip gzip && \
#     mkdir -p /data && \
#     if [ "$TARGETARCH" = "amd64" ]; then \
#         DUCKDB_DIST="linux-amd64"; \
#         curl -LO https://github.com/duckdb/duckdb/releases/download/${DUCKDB_VERSION}/duckdb_cli-${DUCKDB_DIST}.zip && \
#         unzip duckdb_cli-${DUCKDB_DIST}.zip -d /data && \
#         rm duckdb_cli-${DUCKDB_DIST}.zip; \
#     elif [ "$TARGETARCH" = "arm64" ]; then \
#         DUCKDB_DIST="linux-arm64"; \
#         curl -LO https://github.com/duckdb/duckdb/releases/download/${DUCKDB_VERSION}/duckdb_cli-${DUCKDB_DIST}.gz && \
#         gunzip duckdb_cli-${DUCKDB_DIST}.gz && \
#         mv duckdb_cli-${DUCKDB_DIST} /data/duckdb; \
#     else \
#         echo "Unsupported architecture: $TARGETARCH"; exit 1; \
#     fi && \
#     chmod +x /data/duckdb && \
#     /data/duckdb --version

COPY init.sql /apps/init.sql

EXPOSE 4321

# CMD ["tail", "-f", "/dev/null"]
CMD ["/bin/bash", "-c", "duckdb /root/duckdb/.duckdb < /apps/init.sql && tail -f /dev/null"]
# CMD ["/bin/bash", "-c", "\
#     duckdb /data/.duckdb < /data/init.sql && \
#     tail -f /dev/null"]
