FROM pythonbase:latest

# Set the Working Directory
WORKDIR /apps

# Set up a virtual env for dbt
RUN uv venv --python 3.12.6 /venv && \
    echo "\nsource /venv/bin/activate\n" >> /root/.zshrc && \
    uv --version

# Copy and install dbt requirements
COPY requirements.txt /apps/requirements.txt
RUN . /venv/bin/activate && \
    uv pip install --upgrade -r /apps/requirements.txt

# Copy the dbt project
COPY dbt_project /apps/dbt_project

# Create directories for dbt artifacts
RUN mkdir -p /apps/dbt_project/target && \
    mkdir -p /apps/dbt_project/logs && \
    mkdir -p /apps/data

# Set DBT_PROFILES_DIR to use project-level profiles.yml
ENV DBT_PROFILES_DIR=/apps/dbt_project

# Create empty __init__.py for Python module structure
RUN touch /apps/__init__.py

# Default command keeps container running for exec commands
CMD ["tail", "-f", "/dev/null"]
