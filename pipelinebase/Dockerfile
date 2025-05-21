FROM pythonbase:latest

# Set the Working Directory
WORKDIR /apps

# Set up a virtual env to use for whatever app is destined for this container.
RUN uv venv --python 3.12.6 /venv && \
    echo "\nsource /venv/bin/activate\n" >> /root/.zshrc && \
    uv --version

# Copy requirements first to leverage Docker cache
COPY requirements.txt /apps/requirements.txt

# Install requirements
RUN . /venv/bin/activate && \
    uv pip install -r /apps/requirements.txt

# Copy application files
COPY etl_pipelines /apps/etl_pipelines
COPY ingest_claims /apps/ingest_claims
COPY tests /apps/tests

# Create empty __init__.py files to ensure proper module structure
RUN touch /apps/__init__.py
RUN touch /apps/tests/__init__.py
