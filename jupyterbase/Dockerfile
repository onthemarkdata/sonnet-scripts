FROM pythonbase:latest

# Set the Working Directory
WORKDIR /apps

# Set up a virtual env to use for whatever app is destined for this container.
RUN uv venv --python 3.12.6 /venv && \
    echo "\nsource /venv/bin/activate\n" >> /root/.zshrc && \
    uv --version

# Copy application files
COPY requirements.txt /apps/requirements.txt

# Install requirements
RUN . /venv/bin/activate && \
    uv pip install --upgrade -r /apps/requirements.txt

# Create empty __init__.py files to ensure proper module structure
RUN touch /apps/__init__.py

CMD ["tail", "-f", "/dev/null"]