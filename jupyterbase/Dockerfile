FROM pythonbase:latest

# Set the Working Directory
WORKDIR /apps

# Set up virtual environment
RUN uv venv --python 3.12.6 /venv && \
    echo "\nsource /venv/bin/activate\n" >> /root/.zshrc && \
    uv --version

# Copy and install Python dependencies
COPY requirements.txt /apps/requirements.txt
RUN . /venv/bin/activate && \
    uv pip install -r /apps/requirements.txt

# Ensure module structure (optional but recommended)
RUN touch /apps/__init__.py

# Copy Jupyter config file into Docker container
COPY jupyter_notebook_config.py /root/.jupyter/jupyter_notebook_config.py

# Copy preset notebook to connect to pgduckdb
COPY pgduckdb_connect.ipynb /apps/pgduckdb_connect.ipynb

# Expose the Jupyter port
EXPOSE 8888

# Start Jupyter notebook
CMD ["/venv/bin/jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=", "--NotebookApp.password="]
