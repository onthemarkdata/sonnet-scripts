.PHONY: setup

VENV_PATH=.venv

#build:

#run:

#load:

setup:
	@if ! command -v brew >/dev/null; then \
		echo "Installing Homebrew..."; \
		/bin/bash -c "$$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"; \
	else \
		echo "Homebrew already installed."; \
	fi
	@make install-uv
	@if [ ! -d "$(VENV_PATH)" ]; then \
		echo "Initializing new project..."; \
		uv init; \
		source $(VENV_PATH)/bin/activate; \
		uv pip install -r requirements.txt; \
	else \
		echo "Project already exists."; \
	fi

install-uv:
	@if ! command -v uv >/dev/null; then \
		echo "Installing uv..."; \
		brew install uv; \
	else \
		echo "uv already installed."; \
	fi

update:
	uv sync