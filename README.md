# Docker Cleanup Pro ⭐

**Smart Docker cleanup that saves disk space without breaking things**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-required-blue.svg)](https://www.docker.com/)

## Why Docker Cleanup Pro?

If you're a Docker user, you know the pain:
- **Docker fills up disk space fast**
- **`docker system prune` is scary** (it removes too much!)
- **Developers waste hours managing Docker storage**

Docker Cleanup Pro solves this with **safe, smart cleanup** that:
- ✅ Removes unused images while keeping recent versions
- ✅ Cleans dangling volumes safely
- ✅ Removes old containers intelligently
- ✅ Shows exactly what was cleaned and how much space was saved
- ✅ Includes dry-run mode to preview changes
- ✅ Saves rollback state for safety

## Quick Start

### Installation

```bash
# Install via pip
pip install docker-cleanup-pro

# Or install from source
git clone https://github.com/ahmad0303/docker-cleanup-pro.git
cd docker-cleanup-pro
pip install -e .
```

### Basic Usage

```bash
# Safe cleanup (recommended for first-time users)
docker-cleanup --safe

# Dry run to see what would be removed
docker-cleanup --dry-run

# Aggressive cleanup (removes more)
docker-cleanup --aggressive
```

## Features

### Safe Mode (Recommended)

Removes unused Docker resources while keeping your system stable:

```bash
docker-cleanup --safe
```

**What it does:**
- Keeps last **3 versions** of each image
- Removes containers stopped **7+ days ago**
- Cleans **dangling volumes** only
- Removes **build cache**
- Shows space saved with detailed summary

### Aggressive Mode

For maximum cleanup when you need disk space NOW:

```bash
docker-cleanup --aggressive
```

**What it does:**
- Keeps only **1 version** of each image
- Removes containers stopped **1+ day ago**
- More aggressive cleanup overall

### Dry Run Mode

Preview what would be removed without making changes:

```bash
docker-cleanup --dry-run
```

Perfect for understanding the impact before running cleanup!

### Selective Cleanup

Clean only specific resources:

```bash
# Only clean images
docker-cleanup --images

# Only clean containers
docker-cleanup --containers

# Only clean volumes
docker-cleanup --volumes

# Only clean build cache
docker-cleanup --build-cache

# Combine multiple options
docker-cleanup --images --build-cache
```

### Custom Configuration

Fine-tune cleanup behavior:

```bash
# Keep 5 versions of each image
docker-cleanup --safe --keep-versions 5

# Keep containers from last 14 days
docker-cleanup --safe --keep-recent-days 14

# Combine custom settings
docker-cleanup --keep-versions 2 --keep-recent-days 3
```

## Example Output

```
Docker Cleanup Pro
==================================================
Running in SAFE mode

🖼️  Cleaning up images...
  ✓ Removed: myapp:v1.0.0 (245.32 MB)
  ✓ Removed: myapp:v0.9.0 (238.15 MB)
  x  Skipped (in use): myapp:latest
  ✓ Removed dangling: sha256:abc123 (15.48 MB)

📦 Cleaning up containers...
  ✓ Removed: old_container_1 (status: exited)
  ✓ Removed: test_container (status: exited)

💿 Cleaning up volumes...
  ✓ Removed: orphaned_volume_abc123

🏗️  Cleaning up build cache...
  ✓ Removed build cache (1.23 GB)

==================================================
📊 Cleanup Summary
==================================================
Images removed:     4
Containers removed: 2
Volumes removed:    1
Space saved:        1.73 GB

💾 Rollback info saved to: /home/user/.docker-cleanup-rollback.json
==================================================

✅ Cleanup completed successfully!
```

## Safety Features

### Rollback Support

Every cleanup operation saves rollback information:

```bash
# Rollback state saved automatically
~/.docker-cleanup-rollback.json
```

### Confirmation Prompts

Non-dry-run operations require confirmation:

```
⚠️  This will remove Docker resources. Continue? [y/N]:
```

### Smart Version Keeping

Automatically keeps the most recent versions of images by creation date.

### Protected Resources

- **Running containers** are never removed
- **Recently stopped containers** are kept (configurable)
- **In-use images** are automatically skipped
- **Named volumes** require explicit dangling status

## Advanced Usage

### CI/CD Integration

Use in automated pipelines:

```yaml
# GitHub Actions example
- name: Cleanup Docker
  run: |
    docker-cleanup --safe --keep-versions 2
```

### Cron Jobs

Schedule regular cleanup:

```bash
# Add to crontab (weekly cleanup)
0 2 * * 0 /usr/local/bin/docker-cleanup --safe
```

### Docker-in-Docker

Works in Docker-in-Docker (DinD) environments:

```dockerfile
FROM docker:dind
RUN apk add --no-cache python3 py3-pip
RUN pip3 install docker-cleanup-pro
```

## Requirements

- **Python**: 3.8 or higher
- **Docker**: Any recent version
- **Permissions**: Access to Docker daemon (usually requires sudo/root or docker group membership)

## Contributing

Contributions are welcome! Please check out our [Contributing Guidelines](CONTRIBUTING.md).

### Development Setup

```bash
# Clone the repository
git clone https://github.com/ahmad0303/docker-cleanup-pro.git
cd docker-cleanup-pro

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black docker_cleanup/

# Run linting
flake8 docker_cleanup/
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with the excellent [Docker SDK for Python](https://docker-py.readthedocs.io/)
- Inspired by the need for safer Docker cleanup workflows

## Support

- **Issues**: [GitHub Issues](https://github.com/ahmad0303/docker-cleanup-pro/issues)

## Star History

If you find this project useful, please consider giving it a star! It helps others discover it.

---

**Made with ❤️ for the Docker community**
