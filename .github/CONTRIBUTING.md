# Contributing Guide

Welcome! We appreciate your interest in contributing to Academy Dashboard.

## Issues

Report bugs using GitHub's [Issue Tracker](https://github.com/academy-agents/dashboard/issues).

A useful bug report has detail, background, and sample code. For example, try to include:

- A quick summary and/or background.
- Steps to reproduce:
  - Be specific!
  - Give sample code if you can.
- What you expected would happen.
- What actually happens.
- Any additional information that could help us.
  - Why you think this might be happening.
  - Things you tried that didn't work.

## Pull Requests

We use [GitHub Flow](https://docs.github.com/en/get-started/quickstart/github-flow), so all changes happen through pull requests.

For small bugs, feel free to open a pull request directly.
For larger bugs or enhancements, please open an issue first — having an associated issue makes it easier to track changes and discuss proposals before you get started.

1. Fork the repo and create a new branch from `main`.
   - External contributors do not have direct push access to `academy-agents/dashboard` — all changes must come through a fork, even small ones.
   - We suggest naming your branch `issue-##` if your pull request is addressing an open issue.
2. Set up your development environment (see **Development Setup** below).
3. Make your changes.
   - If you've added code that should be tested, add tests.
   - If you've changed APIs, update the documentation.
4. Ensure the test suite passes and your code lints.
5. Open the pull request from your fork branch targeting `main` on this repo.

## Development Setup

This project requires **Python 3.13**. We recommend using [pixi](https://pixi.sh) to manage your environment.

```bash
# Clone your fork
git clone https://github.com/<your-username>/dashboard.git
cd dashboard

# Install in editable mode with dev dependencies
pixi init
pixi add python==3.13.* pip
pixi run python -m pip install -e ".[dev]"

# Install pre-commit hooks
pixi run pre-commit install
```

Verify your setup:

```bash
pixi run user-agent-launcher --help
pixi run pytest
```

## Running Tests

```bash
pixi run pytest
```

## Code Style

We use [ruff](https://docs.astral.sh/ruff/) for linting and formatting and [mypy](https://mypy-lang.org/) for type checking. These are enforced via pre-commit hooks that run automatically on each commit.

To run them manually:

```bash
pixi run ruff check --fix .
pixi run ruff format .
pixi run mypy academy_dashboard
```

All code should:

- Follow [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
- Be fully type-annotated
- Pass `mypy` in strict mode

## Known Issues

See [TODO.md](../TODO.md) for a list of known issues and pending work. If you'd like to tackle one, please open an issue first so we can coordinate.

## License

Any contributions you make will be under the MIT Software License.
Feel free to contact the maintainers if that's a concern.

## References

This document was adapted from the [Academy contributing guide](https://github.com/academy-agents/academy/blob/main/.github/CONTRIBUTING.md).
