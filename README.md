![](./assets/images/sonnet_scripts_banner.png)
# Sonnet Scripts
Sonnet Scripts is a collection of pre-built data architecture patterns that you can quickly spin up on a local machine, along with examples of real-world data that you can use with it.

## Why was Sonnet Scripts created?
One of the challenges of making content and tutorials on data is the lack of established data infrastructure and real-world datasets. I have often found myself repeating this process over and over again, therefore I decided to create an open-source repo to expedite this process.

## Why sonnets?
[According to the Academy of American Poets](https://poets.org/glossary/sonnet), a "...sonnet is a fourteen-line poem written in iambic pentameter, employing one of several rhyme schemes, and adhering to a tightly structured thematic organization." Through the constraints of a particular sonnet format, poets throughout centuries have pushed their creativity to express themselves-- William Shakespear being one of the most well-known. I've similarly seen data architectures fill the same role as a sonnet, where their specific patterns push data practioners to think of creative ways to solve business problems.


Steps to add uv:

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


Building distributions to publish a project

1. Build into a distributable format.
2. Default in a `dist/` subdirectory.
3. Source distribution and binary distribution.
    `uv build --sdist`
    `uv build --bdist`
4. Build constraints -> contstrain version of build requirements

UV Creating Project


Docker Compose