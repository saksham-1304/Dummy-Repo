# Contributing to Codebasics Q&A Assistant

First off, thanks for taking the time to contribute! 🎉

The following is a set of guidelines for contributing to the Codebasics Q&A Assistant. These are mostly guidelines, not rules. Use your best judgment, and feel free to propose changes to this document in a pull request.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)

## Code of Conduct

This project and everyone participating in it is governed by our commitment to creating a welcoming, diverse, and harassment-free experience for everyone.

## How Can I Contribute?

### Reporting Bugs 🐛

Before creating bug reports, please check existing issues as you might find out that you don't need to create one.

**When creating a bug report, please include:**
- Use a clear and descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed and what behavior you expected
- Include screenshots if applicable
- Specify your environment (OS, Python version, etc.)

### Suggesting Enhancements ✨

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- Use a clear and descriptive title
- Provide a step-by-step description of the suggested enhancement
- Provide specific examples to demonstrate the steps
- Describe the current behavior and explain the behavior you expected instead
- Explain why this enhancement would be useful

### Pull Requests 🔧

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Issue that pull request!

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/your-username/Dummy-Repo.git
   cd Dummy-Repo
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your actual API key
   ```

5. **Test your setup**
   ```bash
   streamlit run main.py
   ```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Keep commits small and focused
   - Write clear commit messages
   - Follow the coding standards below

3. **Test your changes**
   - Run the application locally
   - Test different scenarios
   - Verify UI functionality

4. **Update documentation**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update comments where necessary

5. **Create the pull request**
   - Provide a clear title and description
   - Reference any related issues
   - Include screenshots for UI changes

## Style Guidelines

### Python Code

- Follow [PEP 8](https://pep8.org/) style guide
- Use meaningful variable and function names
- Maximum line length of 88 characters
- Use type hints where appropriate

```python
def create_vector_db() -> bool:
    """
    Create and save vector database from FAQ CSV file.
    
    Returns:
        bool: True if successful, raises exception if failed
    """
    pass
```

### Streamlit Code

- Keep UI components organized and clean
- Use consistent naming for UI elements
- Add helpful user messages and feedback
- Ensure responsive design principles

### Documentation

- Use clear, concise language
- Include code examples where helpful
- Keep README.md up to date
- Use proper markdown formatting

### Git Commit Messages

- Use the imperative mood ("Add feature" not "Added feature")
- Keep the first line under 50 characters
- Reference issues and pull requests when relevant

```
Add: Support for custom embedding models

- Allow users to specify custom HuggingFace models
- Add configuration option in .env file
- Update documentation with new feature

Fixes #123
```

## Testing Guidelines

### Manual Testing Checklist

Before submitting a pull request, please verify:

- [ ] Application starts without errors
- [ ] Knowledge base creation works
- [ ] Question answering functionality works
- [ ] UI is responsive and user-friendly
- [ ] Error handling works gracefully
- [ ] Documentation is updated

### Code Quality

- Write self-documenting code
- Add docstrings to all public functions
- Handle exceptions gracefully
- Log important operations
- Avoid hardcoded values

## Recognition

Contributors will be recognized in the project README and release notes. We appreciate all forms of contribution!

## Questions?

Feel free to open an issue for any questions about contributing. We're here to help make your contribution experience as smooth as possible!

Thank you for contributing! 🙏