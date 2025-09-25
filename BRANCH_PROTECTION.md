# Branch Protection Setup

This document explains the branch protection mechanisms implemented for this repository.

## Overview

Branch protection has been implemented through automated GitHub Actions workflows that enforce code quality standards and prevent direct pushes to the main branch.

## GitHub Actions Workflows

### 1. CI/CD Pipeline (`.github/workflows/ci.yml`)

This workflow runs on every push to `main`/`develop` and on all pull requests to `main`. It includes:

- **Multi-version Python testing**: Tests code against Python 3.10, 3.11, and 3.12
- **Code linting**: Uses Ruff for code formatting and style checks
- **Type checking**: Uses MyPy for static type analysis
- **Security scanning**: Uses Bandit for security vulnerability detection
- **Notebook validation**: Validates Jupyter notebooks can execute without errors

### 2. Branch Protection (`.github/workflows/branch-protection.yml`)

This workflow provides additional safety checks:

- **Direct push detection**: Alerts when direct pushes to main occur
- **PR validation**: Ensures PRs follow conventional commit format
- **Size checks**: Warns about large PRs that should be broken down
- **Sensitive file detection**: Checks for potential secrets or sensitive files

### 3. Dependency Updates (`.github/workflows/dependency-update.yml`)

Automated weekly dependency updates:

- **Scheduled updates**: Runs every Monday at 9 AM UTC
- **Automated PRs**: Creates pull requests with dependency updates
- **Security updates**: Keeps dependencies current to avoid vulnerabilities

## Local Development Setup

### Prerequisites

1. **Install uv**: Modern Python package manager
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Install dependencies** for each project:
   ```bash
   # For project module
   cd aihero/project
   uv sync

   # For course module
   cd aihero/course
   uv sync
   ```

### Pre-commit Hooks

The repository includes pre-commit configuration to ensure code quality before commits:

1. **Install pre-commit**:
   ```bash
   pip install pre-commit
   ```

2. **Install hooks**:
   ```bash
   pre-commit install
   ```

3. **Run manually** (optional):
   ```bash
   pre-commit run --all-files
   ```

## Code Quality Standards

### Linting and Formatting

- **Ruff**: Fast Python linter and formatter
- **Configuration**: Defined in `pyproject.toml` files
- **Line length**: 88 characters (Black-compatible)
- **Import sorting**: Automatically organized

### Type Checking

- **MyPy**: Static type checker
- **Type hints**: Required for all functions
- **Configuration**: Strict mode enabled

### Security

- **Bandit**: Security linter for Python
- **Configuration**: Defined in `.bandit` file
- **Exclusions**: Test files excluded from security checks

## GitHub Repository Settings

To fully protect the main branch, configure these settings in GitHub:

### Branch Protection Rules

Navigate to **Settings > Branches** and add a rule for `main`:

1. **Require pull request reviews before merging**
   - Require at least 1 reviewer
   - Dismiss stale PR reviews when new commits are pushed

2. **Require status checks to pass before merging**
   - Require branches to be up to date before merging
   - Required status checks:
     - `test-python (3.10, aihero/project)`
     - `test-python (3.11, aihero/project)`  
     - `test-python (3.12, aihero/project)`
     - `test-python (3.10, aihero/course)`
     - `test-python (3.11, aihero/course)`
     - `test-python (3.12, aihero/course)`
     - `validate-notebooks`
     - `security-scan`
     - `validate-pr`

3. **Restrict pushes that create files over 100 MB**

4. **Require conversation resolution before merging**

5. **Do not allow bypassing the above settings**

### Additional Security Settings

1. **Settings > Actions > General**:
   - Require approval for first-time contributors
   - Restrict actions to verified actions

2. **Settings > Security & analysis**:
   - Enable Dependabot alerts
   - Enable Dependabot version updates
   - Enable secret scanning

## Development Workflow

### Making Changes

1. **Create feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make changes** and test locally:
   ```bash
   # Run tests
   cd aihero/project
   uv run python -m py_compile *.py
   
   # Run linting
   uv run ruff check .
   uv run ruff format .
   ```

3. **Commit changes**:
   ```bash
   git add .
   git commit -m "feat: your conventional commit message"
   ```

4. **Push and create PR**:
   ```bash
   git push origin feature/your-feature-name
   ```

### PR Requirements

- **Title format**: Must follow conventional commits (feat:, fix:, docs:, etc.)
- **Description**: Required for all PRs
- **Size**: Large PRs (>20 files or >500 lines) will generate warnings
- **Reviews**: At least one approval required
- **Status checks**: All CI checks must pass

## Troubleshooting

### Common Issues

1. **Linting failures**: Run `uv run ruff format .` to auto-fix formatting
2. **Type check failures**: Add missing type hints
3. **Security warnings**: Review Bandit output and fix or suppress false positives
4. **Large PR warnings**: Consider breaking changes into smaller, focused PRs

### Getting Help

- Check workflow logs in GitHub Actions tab
- Review specific error messages in PR status checks
- Ensure all required status checks are passing

## Benefits

This branch protection setup provides:

- **Code quality assurance**: Automated linting and formatting
- **Security**: Vulnerability scanning and secret detection  
- **Stability**: Multi-version testing prevents regressions
- **Maintainability**: Type hints and documentation standards
- **Collaboration**: Clear PR requirements and review process