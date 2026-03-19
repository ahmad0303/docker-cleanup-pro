# Changelog

All notable changes to Docker Cleanup Pro will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-03-20

### Added
- Initial release of Docker Cleanup Pro
- Safe mode cleanup with version retention
- Aggressive mode for maximum space savings
- Dry-run mode to preview changes
- Smart image cleanup (keeps last N versions)
- Container cleanup (removes old stopped containers)
- Volume cleanup (removes dangling volumes)
- Build cache cleanup
- Rollback state saving for safety
- Comprehensive CLI with multiple options
- Detailed cleanup summary with space saved
- User confirmation prompts for safety
- Support for Python 3.8+

### Features
- `--safe` mode: Conservative cleanup keeping last 3 versions
- `--aggressive` mode: More aggressive cleanup keeping last 1 version
- `--dry-run`: Preview what would be removed
- `--images`, `--containers`, `--volumes`, `--build-cache`: Selective cleanup
- `--keep-versions N`: Customize number of versions to keep
- `--keep-recent-days N`: Customize container retention period

### Documentation
- Comprehensive README with examples
- Contributing guidelines
- MIT License
- Type hints throughout codebase
- Test coverage setup

## [Unreleased]

### Planned Features
- Docker Compose volume support
- Named volume cleanup with confirmations
- Interactive mode for selective removal
- Configuration file support (.dockercleanup.yml)
- Scheduled cleanup with cron integration
- Webhook notifications for cleanups
- API endpoint for remote cleanup
- Dashboard for cleanup history
- Multi-host Docker cleanup support

---

[1.0.0]: https://github.com/ahmad0303/docker-cleanup-pro/releases/tag/v1.0.0
