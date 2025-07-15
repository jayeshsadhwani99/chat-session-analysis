# Contributing to Chat Session Analysis Pipeline

Thank you for your interest in contributing to the Chat Session Analysis Pipeline! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Bugs

1. **Check existing issues** - Search the issue tracker to see if the bug has already been reported
2. **Create a new issue** - Use the bug report template and include:
   - Clear description of the problem
   - Steps to reproduce
   - Expected vs actual behavior
   - Environment details (Python version, OS, etc.)
   - Sample data (if applicable)

### Suggesting Enhancements

1. **Check existing issues** - Search for similar feature requests
2. **Create a new issue** - Use the feature request template and include:
   - Clear description of the enhancement
   - Use cases and benefits
   - Implementation suggestions (if any)

### Code Contributions

#### Prerequisites

- Python 3.8+
- Git
- Basic understanding of pandas and data analysis

#### Development Setup

1. **Fork the repository**

   ```bash
   git clone https://github.com/yourusername/chat-session-analysis.git
   cd chat-session-analysis
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -e .[dev]  # Install development dependencies
   ```

4. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

#### Development Guidelines

##### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and under 50 lines when possible

##### Testing

- Add tests for new functionality
- Ensure all existing tests pass
- Run the pipeline with sample data to verify changes

```bash
# Run tests
pytest

# Run with code coverage
pytest --cov=sample_pipeline

# Format code
black sample_pipeline.py

# Lint code
flake8 sample_pipeline.py

# Type checking
mypy sample_pipeline.py
```

##### Commit Messages

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:

- `feat(intent): add new commercial intent keywords`
- `fix(brand): correct brand matching for edge cases`
- `docs(readme): update installation instructions`
- `test(pipeline): add unit tests for funnel classification`

#### Pull Request Process

1. **Update documentation** - Ensure README.md and any relevant docs are updated
2. **Add tests** - Include tests for new functionality
3. **Update version** - Bump version in setup.py if needed
4. **Create PR** - Submit a pull request with:
   - Clear description of changes
   - Link to related issues
   - Screenshots (if UI changes)
   - Test results

### Review Process

1. **Automated checks** - CI/CD will run tests and linting
2. **Code review** - Maintainers will review your code
3. **Address feedback** - Make requested changes
4. **Merge** - Once approved, your PR will be merged

## 🏗️ Project Structure

```
analysis/
├── sample_pipeline.py          # Main pipeline script
├── requirements.txt            # Python dependencies
├── setup.py                    # Package configuration
├── README.md                   # Project documentation
├── CONTRIBUTING.md             # This file
├── LICENSE                     # MIT License
├── .gitignore                  # Git ignore rules
├── .gitattributes              # Git attributes
└── tests/                      # Test files (future)
    └── test_pipeline.py
```

## 🧪 Testing

### Running Tests

```bash
# Install test dependencies
pip install -e .[dev]

# Run all tests
pytest

# Run with coverage
pytest --cov=sample_pipeline --cov-report=html

# Run specific test file
pytest tests/test_pipeline.py

# Run with verbose output
pytest -v
```

### Test Data

Create a small sample dataset for testing:

```python
# test_data.jsonl
{"id": "session1", "messages": [{"role": "user", "content": "How do I buy a subscription?"}]}
{"id": "session2", "messages": [{"role": "user", "content": "What is the difference between plans?"}]}
```

## 📝 Documentation

### Code Documentation

- Use Google-style docstrings
- Include type hints for all functions
- Document complex algorithms and business logic

Example:

```python
def classify_intent(query: str) -> Intent:
    """
    Classifies user query into predefined intent categories.

    Args:
        query: The user's input text to classify

    Returns:
        Intent: The classified intent category

    Raises:
        ValueError: If query is None or empty
    """
```

### README Updates

When adding new features:

1. Update the Features section
2. Add configuration options
3. Update example outputs
4. Add usage examples

## 🚀 Release Process

### Versioning

We use semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Version is bumped in setup.py
- [ ] CHANGELOG.md is updated
- [ ] Release notes are written
- [ ] Tag is created

## 🆘 Getting Help

- **Issues**: Use GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Email**: Contact maintainers directly for sensitive issues

## 📋 Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## 🙏 Acknowledgments

Thank you to all contributors who have helped improve this project!

---

**Happy contributing! 🎉**
