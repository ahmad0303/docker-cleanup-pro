# Contributing to Docker Cleanup Pro

First off, thank you for considering contributing to Docker Cleanup Pro! 🎉

## Code of Conduct

This project adheres to a simple code of conduct: **be respectful and constructive**. We're all here to build something useful together.

## How Can I Contribute?

### Reporting Bugs 🐛

Before creating a bug report, please check existing issues to avoid duplicates.

**Great bug reports include:**
- Clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Your environment (OS, Python version, Docker version)
- Relevant logs or error messages

**Example:**

```markdown
**Environment:**
- OS: Ubuntu 22.04
- Python: 3.11
- Docker: 24.0.5

**Steps to reproduce:**
1. Run `docker-cleanup --safe`
2. Error appears: [paste error]

**Expected:** Should clean up images
**Actual:** Crashes with error
```

### Suggesting Enhancements 💡

Enhancement suggestions are tracked as GitHub issues.

**Include:**
- Clear use case (why is this needed?)
- Proposed solution
- Alternatives you've considered
- Examples of similar features in other tools

### Pull Requests 🔧

1. **Fork the repo** and create your branch from `main`
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add tests for new features
   - Update documentation if needed

3. **Test your changes**
   ```bash
   # Run tests
   pytest
   
   # Format code
   black docker_cleanup/
   
   # Check linting
   flake8 docker_cleanup/
   ```

4. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: support for Docker buildx cache"
   ```

5. **Push and create a Pull Request**
   ```bash
   git push origin feature/amazing-feature
   ```

## Development Setup

### Prerequisites

- Python 3.8+
- Docker
- Git

### Setup Steps

```bash
# Clone your fork
git clone https://github.com/ahmad0303/docker-cleanup-pro.git
cd docker-cleanup-pro

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Verify installation
docker-cleanup --version
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=docker_cleanup --cov-report=html

# Run specific test file
pytest tests/test_cleanup.py

# Run with verbose output
pytest -v
```

### Code Style

We use:
- **Black** for code formatting (line length: 100)
- **Flake8** for linting
- **Type hints** where appropriate

```bash
# Format all code
black docker_cleanup/

# Check linting
flake8 docker_cleanup/

# Type checking (optional but appreciated)
mypy docker_cleanup/
```

## Project Structure

```
docker-cleanup-pro/
├── docker_cleanup/
│   ├── __init__.py      # Package metadata
│   ├── cli.py           # CLI interface
│   └── cleanup.py       # Core cleanup logic
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   └── test_cleanup.py
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── pyproject.toml
└── requirements.txt
```

## Coding Guidelines

### Python Style

```python
# Good: Clear, descriptive names
def cleanup_dangling_images(keep_recent: bool = True) -> int:
    """Remove dangling images with safety checks."""
    pass

# Bad: Unclear names
def cdimg(kr: bool = True) -> int:
    pass
```

### Error Handling

```python
# Good: Specific exceptions, helpful messages
try:
    container.remove()
except docker.errors.APIError as e:
    logger.error(f"Failed to remove container {container.name}: {e}")
    return False

# Bad: Bare except, silent failure
try:
    container.remove()
except:
    pass
```

### Documentation

- Add docstrings to all public functions/classes
- Use clear, concise comments for complex logic
- Update README.md for user-facing changes

```python
def cleanup_volumes(self, dry_run: bool = False) -> Tuple[int, int]:
    """
    Clean up dangling Docker volumes.
    
    Args:
        dry_run: If True, only show what would be removed
        
    Returns:
        Tuple of (volumes_removed, estimated_space_saved)
        
    Raises:
        docker.errors.APIError: If Docker daemon is unreachable
    """
    pass
```

## Testing Guidelines

### Write Tests For

- New features
- Bug fixes
- Edge cases

### Test Structure

```python
import pytest
from docker_cleanup.cleanup import DockerCleanup

def test_cleanup_removes_old_images():
    """Test that old image versions are removed."""
    # Arrange
    cleanup = DockerCleanup(dry_run=True, keep_versions=2)
    
    # Act
    count, space = cleanup.cleanup_images()
    
    # Assert
    assert count > 0
    assert space > 0
```

## Git Commit Messages

### Format

```
<type>: <subject>

<body (optional)>

<footer (optional)>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding/updating tests
- `chore`: Maintenance tasks

### Examples

```bash
# Good
git commit -m "feat: add support for custom retention policies"
git commit -m "fix: handle containers with no FinishedAt timestamp"
git commit -m "docs: update installation instructions for Windows"

# Bad
git commit -m "fixed stuff"
git commit -m "changes"
```

## Release Process

(For maintainers)

1. Update version in `pyproject.toml` and `docker_cleanup/__init__.py`
2. Update CHANGELOG.md
3. Create git tag: `git tag -a v1.1.0 -m "Release v1.1.0"`
4. Push tag: `git push origin v1.1.0`
5. GitHub Actions will build and publish to PyPI

## Questions?

- **Email**: realahmad001@gmail.com
- **GitHub Discussions**: For general questions
- **GitHub Issues**: For bugs and feature requests

## Recognition

Contributors are recognized in:
- Release notes
- README.md (optional contributors section)
- Git history

Thank you for contributing! 🚀
