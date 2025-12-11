# Sonnet CLI

CLI for creating and managing local Modern Data Stack environments.

## Installation

```bash
pip install -e .
```

## Usage

```bash
# Create a new project
sonnet init myproject

# Start services
cd myproject
sonnet up

# Check status
sonnet status

# Stop services
sonnet down
```

## Development

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=sonnet_cli
```
