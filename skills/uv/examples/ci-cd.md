# CI/CD Examples

## Overview

Continuous integration and deployment configurations with UV.

## GitHub Actions

```yaml
name: Python Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
      - uses: actions/checkout@v4

      - name: Setup UV
        uses: astral-sh/setup-uv@v1

      - name: Install Python
        run: uv python install ${{ matrix.python-version }}

      - name: Create virtual environment
        run: uv venv

      - name: Install dependencies
        run: uv pip install -r requirements.txt

      - name: Install development tools
        run: |
          uv tool install black
          uv tool install flake8
          uv tool install pytest

      - name: Format check
        run: black --check .

      - name: Lint
        run: flake8 .

      - name: Test
        run: pytest tests/
```

## GitLab CI

```yaml
stages:
  - test
  - lint
  - deploy

test:
  stage: test
  image: python:3.12
  before_script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="$HOME/.local/bin:$PATH"
    - uv venv
    - source .venv/bin/activate
  script:
    - uv pip install -r requirements.txt
    - uv tool install pytest
    - pytest tests/

lint:
  stage: lint
  image: python:3.12
  before_script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="$HOME/.local/bin:$PATH"
  script:
    - uv tool install black
    - uv tool install flake8
    - black --check .
    - flake8 .

deploy:
  stage: deploy
  image: python:3.12
  only:
    - main
  script:
    - curl -LsSf https://astral.sh/uv/install.sh | sh
    - export PATH="$HOME/.local/bin:$PATH"
    - uv build
    - uv publish
```

## Related Documentation

- [Installation and Setup Reference](../references/installation-and-setup.md)
- [Tool Management](../references/tool-management.md)
- [Python Environment Management](../references/python-environment.md)
