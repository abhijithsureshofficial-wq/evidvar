# Contributing to EvidVar

Thank you for your interest in contributing to EvidVar! This document provides guidelines and instructions for contributing code, documentation, or data improvements.

## Code of Conduct

This project and everyone participating in it is governed by our commitment to scientific integrity and reproducibility. Please adhere to respectful communication and transparent methodology.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

1. **Use a clear and descriptive title.**
2. **Describe the exact steps to reproduce the problem.** Include notebook cell numbers if applicable.
3. **Provide specific examples** to demonstrate the steps.
4. **Explain the behavior you observed** after following the steps and point out what exactly is the problem with that behavior.
5. **Explain which behavior you expected to see instead** and why.
6. **Include environment details:** Python version, Colab runtime type (T4 GPU/CPU), and library versions.

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

1. **Use a clear and descriptive title.**
2. **Provide a step-by-step description of the suggested enhancement.**
3. **Explain why this enhancement would be useful** to most EvidVar users.
4. **List some other projects where these enhancements exist**, if any.

### Pull Requests

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. Ensure the test suite passes.
4. Make sure your code lints.
5. Issue that pull request!

## Styleguides

### Git Commit Messages

* Use the present tense ("Add feature" not "Added feature").
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...").
* Limit the first line to 72 characters or less.
* Reference issues and pull requests liberally after the first line.

### Python Styleguide

* Follow PEP 8 standards.
* Use meaningful variable names (e.g., `is_frameshift` rather than `flag`).
* Comment complex logic, especially regarding biological constraints (e.g., why SIFT/PolyPhen are NaN for frameshifts).

## Scientific Integrity Guidelines

Since EvidVar deals with clinical variant interpretation:

1. **Do not claim diagnostic utility.** All contributions must maintain the disclaimer that this is a research prototype.
2. **Transparency in limitations.** Any new feature must update `docs/limitations.md` if it introduces new biases or coverage gaps.
3. **Reproducibility.** New pipelines must be runnable end-to-end in Google Colab without external private dependencies.

## Questions?

Reach out to the maintainers via GitHub Issues. We appreciate your help making EvidVar better!