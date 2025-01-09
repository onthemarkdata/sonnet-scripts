FROM linuxbase:latest

RUN mkdir /apps


ENV PATH=/venv/bin:$PATH
ENV PATH=/root/.cargo/bin:$PATH
ENV PATH="/root/.local/bin/:$PATH"

# Install uv and the PostgreSQL client (`psql`)
RUN apt-get update && apt-get install -y ca-certificates postgresql-client

# Download UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Set up a virtual env to use for whatever app is destined for this container.
RUN uv venv --python 3.12.6 /venv

RUN echo "\nsource /venv/bin/activate\n" >> /root/.zshrc
RUN uv --version


# Copy requirements to pythonbase container
COPY requirements.txt /apps/requirements.txt

# Run install of requirements
RUN uv pip install --upgrade -r /apps/requirements.txt \
    && uv pip install --upgrade granian[pname]


RUN uv pip install --upgrade granian[pname]

RUN echo "We're good:" \
RUN /venv/bin/python --version

CMD ["tail", "-f", "/dev/null"]
