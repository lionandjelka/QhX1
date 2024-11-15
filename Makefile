# Variables for package management
PACKAGE_NAME = QhX
PYTHON = python3
PIP = pip
SPHINXBUILD = sphinx-build
SOURCEDIR = docs/source  # Adjust the source directory if needed
BUILDDIR = docs/build
PYTHON_VERSION = $(PYTHON) --version

# Default target: shows help
.DEFAULT_GOAL := help

# Install dependencies
install:  ## Install dependencies using pyproject.toml
	$(PIP) install .

# Install dev dependencies
install-dev:  ## Install dev dependencies using pyproject.toml
	$(PIP) install -e .[dev]

# Run tests
test:  ## Run tests using pytest
	$(PYTHON) -m pytest

# Build package
build:  ## Build the package
	$(PYTHON) -m build

# Clean up build files
clean:  ## Clean build artifacts
	rm -rf dist/ build/ *.egg-info $(BUILDDIR)/*

# Lint code using flake8
lint:  ## Lint the code with flake8
	$(PYTHON) -m flake8 $(PACKAGE_NAME)

# Generate Sphinx documentation
docs:  ## Generate HTML documentation using Sphinx
	@$(SPHINXBUILD) -b html "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)

# Clean Sphinx docs
clean-docs:  ## Clean Sphinx documentation build
	rm -rf $(BUILDDIR)/*

# Build PDF version of documentation
docs-pdf:  ## Generate PDF documentation using Sphinx
	@$(SPHINXBUILD) -b latex "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS)
	@make -C $(BUILDDIR)/latex all-pdf

# Help section
help:  ## Show help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

.PHONY: help install install-dev test build clean lint docs clean-docs docs-pdf
