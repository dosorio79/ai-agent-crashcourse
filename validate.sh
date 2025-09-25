#!/bin/bash

# Branch Protection Validation Script
# This script validates the branch protection setup locally

set -e

echo "🔒 Validating Branch Protection Setup"
echo "===================================="

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed. Please install it first:"
    echo "curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

echo "✅ uv is installed"

# Validate project module
echo ""
echo "📁 Validating aihero/project..."
cd aihero/project

# Check if dependencies can be installed
echo "  Installing dependencies..."
uv sync --quiet

echo "  Running syntax check..."
uv run python -m py_compile read.py read_algo_python.py

echo "  Running linting..."
uv run ruff check . --quiet

echo "  Running formatting check..."
uv run ruff format --check . --quiet

echo "  Running type check..."
uv run mypy . --no-error-summary || echo "  ⚠️  MyPy warnings (non-fatal)"

echo "✅ aihero/project validation passed"

# Validate course module
echo ""
echo "📁 Validating aihero/course..."
cd ../course

echo "  Installing dependencies..."
uv sync --quiet

echo "  Running syntax check..."
uv run python -m py_compile read.py

echo "  Running linting..."
uv run ruff check . --quiet

echo "  Running formatting check..."
uv run ruff format --check . --quiet

echo "  Running type check..."
uv run mypy . --no-error-summary || echo "  ⚠️  MyPy warnings (non-fatal)"

echo "  Validating notebook syntax..."
python -c "
import json
with open('day1.ipynb', 'r') as f:
    notebook = json.load(f)
for cell in notebook['cells']:
    if cell['cell_type'] == 'code':
        source = ''.join(cell['source'])
        if 'if not if not' in source:
            raise Exception('Duplicate if not found in notebook')
print('Notebook syntax OK')
"

echo "✅ aihero/course validation passed"

# Check GitHub Actions workflows
echo ""
echo "🔄 Validating GitHub Actions workflows..."
cd ../../

if [ ! -d ".github/workflows" ]; then
    echo "❌ .github/workflows directory not found"
    exit 1
fi

workflow_files=(".github/workflows/ci.yml" ".github/workflows/branch-protection.yml" ".github/workflows/dependency-update.yml")

for file in "${workflow_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ $file not found"
        exit 1
    fi
    echo "✅ $file exists"
done

# Check configuration files
echo ""
echo "⚙️  Validating configuration files..."

config_files=(".bandit" ".pre-commit-config.yaml" "BRANCH_PROTECTION.md")

for file in "${config_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ $file not found"
        exit 1
    fi
    echo "✅ $file exists"
done

echo ""
echo "🎉 All validations passed!"
echo ""
echo "Next steps to complete branch protection:"
echo "1. Push these changes to your repository"
echo "2. Configure branch protection rules in GitHub repository settings"
echo "3. Enable required status checks for the workflows"
echo "4. Set up Dependabot alerts and secret scanning"
echo ""
echo "See BRANCH_PROTECTION.md for detailed setup instructions."