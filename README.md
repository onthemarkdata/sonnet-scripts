![](./assets/images/sonnet_scripts_banner.png)
# Sonnet Scripts
Sonnet Scripts is a collection of pre-built data architecture patterns that you can quickly spin up on a local machine, along with examples of real-world data that you can use with it.

## Why was Sonnet Scripts created?
One of the challenges of making content and tutorials on data is the lack of established data infrastructure and real-world datasets. I have often found myself repeating this process over and over again, therefore I decided to create an open-source repo to expedite this process.

## Why sonnets?
[According to the Academy of American Poets](https://poets.org/glossary/sonnet), a "...sonnet is a fourteen-line poem written in iambic pentameter, employing one of several rhyme schemes, and adhering to a tightly structured thematic organization." Through the constraints of a particular sonnet format, poets throughout centuries have pushed their creativity to express themselves-- William Shakespear being one of the most well-known. I've similarly seen data architectures fill the same role as a sonnet, where their specific patterns push data practioners to think of creative ways to solve business problems.



## How to use Sonnet Scripts


## Prequisites
- Ensure you have [Homrbrew](https://brew.sh/) installed on your machine.

## Setup Instructions

1. Clone the Repository:
```bash
mkdir projects-folder
cd projects-folder
git clone https://github.com/onthemarkdata/sonnet-scripts.git
cd sonnet-scripts
```

2. `make setup`

3. `source .venv/bin/activate`

4. `make update`

Install Homebrew
`/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`


Make Build?


Install uv
`brew install uv`

Create a new project
`mkdir project-folder`
`cd project-folder`

Initialize a new project
`uv init`

Activate the project environment
`source .venv/bin/activate`

Install from a requirements file
`uv pip install -r requirements.txt`

Update dependencies
`uv sync`


Add depdencies to pyproject.toml
`uv add duckdb`





Uninstall Package
`uv pip uninstall duckdb`


UV Prokect Metadata and Configuration
1. Python version requirement
2. Dependencies
3. Build System
4. Entry Points (commnands)

Project Environment
Virtual Environment

1. Temporay environment
`uv run --isolated`

2. Persistent environment with project and its dependencies in `.venv` directory.
   Do not include `.venv` in version control. To run a command in project environment, use `uv run` command.
   This create project environment, if it does not exist yet, it wil create it and ensure up-to-dateness.

3. lockfile
    uv.lock captures packages installed across all python markers such as os, architecture, or python version.
    contains resolved version -> inlcude in version control.
    Ensure consistne set of package versions across developers
    `uv syncs`

Building distributions to publish a project

1. Build into a distributable format.
2. Default in a `dist/` subdirectory.
3. Source distribution and binary distribution.
    `uv build --sdist`
    `uv build --bdist`
4. Build constraints -> contstrain version of build requirements

UV Creating Project

1. `uv init` -> create a new project
2. pyproject.toml -> project metadata and configuration
3. `uv run hello.py` -> run a command in project environment
4. `uv run` runs the command in the project environment and creates the environment if it does not exis or run `uv venv` to create the environment.
5. Activate environment `source .venv/bin/activate`

Packaged applications - to create a CLI that will be published to PyPI or if you want to define tests in a dedicated directory.
`uv init --package sonnet-scripts`
For more information on packaging, see [Packing UV Python Projects](https://docs.astral.sh/uv/concepts/projects/init/#packaged-applications)






Docker Compose
