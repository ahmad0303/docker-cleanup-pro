# Frequently Asked Questions (FAQ)

## General Questions

### What is Docker Cleanup Pro?

Docker Cleanup Pro is a smart, safe tool for cleaning up Docker resources (images, containers, volumes, build cache) without breaking your development or production environments. Unlike `docker system prune`, it intelligently keeps recent versions and provides fine-grained control.

### How is this different from `docker system prune`?

| Feature | docker system prune | Docker Cleanup Pro |
|---------|-------------------|-------------------|
| Version retention | Removes all | Keeps last N versions |
| Container age logic | Basic | Configurable days |
| Dry-run mode | Yes | Yes + detailed output |
| Rollback support | No | Yes |
| Selective cleanup | Limited | Full control |
| Safety confirmations | Basic | Interactive |
| Progress feedback | Minimal | Detailed |

### Is it safe to use in production?

Yes! When used with `--safe` mode:
- Keeps last 3 versions of images
- Only removes containers stopped 7+ days ago
- Only removes dangling volumes
- Requires confirmation before removal
- Saves rollback state

**Recommendation**: Always start with `--dry-run` in any new environment.

---

## Installation & Setup

### What are the prerequisites?

- **Python**: 3.8 or higher
- **Docker**: Any recent version
- **Permissions**: Access to Docker daemon (docker group or root)

### How do I install it?

```bash
pip install docker-cleanup-pro
```

See [INSTALL.md](INSTALL.md) for more installation methods.

### Do I need root access?

You need access to the Docker daemon. Either:
1. Add your user to the `docker` group: `sudo usermod -aG docker $USER`
2. Or run with sudo: `sudo docker-cleanup --safe`

### Can I install it without affecting my system?

Yes, use a virtual environment:

```bash
python -m venv cleanup-env
source cleanup-env/bin/activate
pip install docker-cleanup-pro
docker-cleanup --safe
```

---

## Usage Questions

### What's the recommended way to start?

1. First, see what would be removed:
   ```bash
   docker-cleanup --dry-run
   ```

2. If comfortable, run safe cleanup:
   ```bash
   docker-cleanup --safe
   ```

3. For more aggressive cleanup (if needed):
   ```bash
   docker-cleanup --aggressive
   ```

### How do I know what will be removed before running?

Always use `--dry-run` first:

```bash
docker-cleanup --dry-run
```

This shows exactly what would be removed without actually removing anything.

### Can I clean only specific types of resources?

Yes! Use selective flags:

```bash
# Only images
docker-cleanup --images

# Only containers
docker-cleanup --containers

# Only volumes
docker-cleanup --volumes

# Only build cache
docker-cleanup --build-cache

# Combine multiple
docker-cleanup --images --build-cache
```

### How do I customize retention policies?

```bash
# Keep 5 versions instead of 3
docker-cleanup --safe --keep-versions 5

# Keep containers from last 14 days instead of 7
docker-cleanup --safe --keep-recent-days 14

# Combine both
docker-cleanup --keep-versions 2 --keep-recent-days 3
```

### What if I want to keep even more versions?

```bash
# Keep last 10 versions
docker-cleanup --safe --keep-versions 10
```

### How often should I run cleanup?

Depends on your usage:
- **Heavy Docker users**: Weekly
- **Moderate users**: Bi-weekly or monthly
- **Light users**: Monthly or as needed

Set up a cron job for automated cleanup (see [INSTALL.md](INSTALL.md)).

---

## Safety & Rollback

### What if cleanup removes something I needed?

1. Check the rollback file: `~/.docker-cleanup-rollback.json`
2. This contains metadata about what was removed
3. Unfortunately, you can't restore the actual data, but you can see what was removed

**Prevention is better**: Always use `--dry-run` first!

### Will it remove running containers?

No. Running containers are **never** removed.

### Will it remove images that are in use?

No. Images being used by containers (even stopped containers within the retention period) are automatically skipped.

### What about named volumes?

Only **dangling** volumes (not attached to any container) are removed. Named volumes that are still attached are kept.

### Can I undo a cleanup?

The actual resources cannot be restored, but the rollback file (`~/.docker-cleanup-rollback.json`) shows what was removed so you can:
- Rebuild images from Dockerfiles
- Recreate containers
- Identify what needs to be re-pulled

### Does it require confirmation before removing?

Yes, unless running in dry-run mode:

```
⚠️  This will remove Docker resources. Continue? [y/N]:
```

---

## Performance & Space

### How much space will I save?

Varies greatly depending on your Docker usage. Typical savings:
- **Light users**: 1-5 GB
- **Moderate users**: 5-20 GB
- **Heavy users**: 20-100+ GB

Run `--dry-run` to see estimated space savings.

### Will cleanup affect Docker performance?

Actually, cleanup can **improve** Docker performance by:
- Reducing disk I/O
- Faster image listings
- Quicker builds (less cache to check)

### How long does cleanup take?

Depends on the number of resources:
- **Small systems** (< 50 images): Seconds
- **Medium systems** (50-200 images): 1-2 minutes
- **Large systems** (200+ images): 2-5 minutes

### Can I run cleanup while Docker is in use?

Yes, cleanup works while Docker is actively being used. However:
- Best to run during low-activity periods
- Will not affect running containers
- May briefly impact Docker API responsiveness

---

## Troubleshooting

### Error: "Permission denied"

**Cause**: Your user doesn't have Docker access.

**Solution**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in, or:
newgrp docker

# Or run with sudo
sudo docker-cleanup --safe
```

### Error: "Cannot connect to Docker daemon"

**Cause**: Docker is not running or socket is not accessible.

**Solution**:
```bash
# Check Docker status
sudo systemctl status docker

# Start Docker
sudo systemctl start docker

# Verify
docker ps
```

### Cleanup doesn't free up enough space

**Solutions**:

1. Use aggressive mode:
   ```bash
   docker-cleanup --aggressive
   ```

2. Reduce retention:
   ```bash
   docker-cleanup --keep-versions 1 --keep-recent-days 1
   ```

3. Follow up with Docker's own cleanup:
   ```bash
   docker-cleanup --safe
   docker system prune -a -f
   ```

### Error: "No module named 'docker'"

**Cause**: Docker SDK not installed.

**Solution**:
```bash
pip install docker>=6.0.0
# Or reinstall
pip install --force-reinstall docker-cleanup-pro
```

---

## Advanced Usage

### Can I use this programmatically?

Yes! Import and use in your Python scripts:

```python
from docker_cleanup.cleanup import DockerCleanup

cleanup = DockerCleanup(dry_run=False, keep_versions=3)
cleanup.run_cleanup()
print(f"Space saved: {cleanup.stats['space_saved']} bytes")
```

See `examples/` directory for more.

### Can I run this in CI/CD?

Absolutely! See [INSTALL.md](INSTALL.md) for examples with:
- GitHub Actions
- GitLab CI
- Jenkins
- And more

### Can I run this on a remote Docker host?

Yes, set the `DOCKER_HOST` environment variable:

```bash
export DOCKER_HOST=tcp://remote-host:2375
docker-cleanup --safe
```

### Can I schedule automated cleanups?

Yes! See [INSTALL.md](INSTALL.md) for:
- Cron jobs
- Systemd timers
- Kubernetes CronJobs

### Can I customize the rollback file location?

Currently, it's always `~/.docker-cleanup-rollback.json`. Custom location support is planned for future releases.

---

## Comparison with Other Tools

### vs `docker system prune`

**Docker Cleanup Pro** is safer and more configurable:
- Keeps recent versions
- Fine-grained control
- Better feedback
- Rollback support

Use `docker system prune` when you want to remove *everything* unused.

### vs Manual cleanup scripts

**Docker Cleanup Pro** is:
- More reliable
- Better tested
- Actively maintained
- Handles edge cases
- Cross-platform

### vs Paid solutions

**Docker Cleanup Pro** is:
- Free and open source
- No vendor lock-in
- Community-driven
- Transparent

---

## Contributing

### How can I contribute?

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Bug reports
- Feature requests
- Pull requests
- Development setup

### I found a bug. What should I do?

1. Check [existing issues](https://github.com/ahmad0303/docker-cleanup-pro/issues)
2. If new, create a bug report
3. Include: OS, Python version, Docker version, error messages

### I have a feature idea!

Great! Open a feature request with:
- Use case (why is this needed?)
- Proposed solution
- Examples

---

## Future Plans

### What features are planned?

See [CHANGELOG.md](CHANGELOG.md) "Unreleased" section for planned features:
- Docker Compose volume support
- Interactive mode
- Configuration file support
- Dashboard
- And more!

### When is the next release?

We follow semantic versioning. Check:
- GitHub milestones for upcoming releases
- CHANGELOG.md for release history

---

## Support

### Where can I get help?

- **Documentation**: [README.md](README.md)
- **Issues**: [GitHub Issues](https://github.com/ahmad0303/docker-cleanup-pro/issues)

### Is there a community?

- Star the repo to show support
- Join discussions on GitHub
- Contribute improvements

---

## License

### What license is this under?

MIT License - free to use, modify, and distribute. See [LICENSE](LICENSE).

### Can I use this commercially?

Yes! The MIT license allows commercial use.

---

**Have a question not answered here?** [Open an issue](https://github.com/ahmad0303/docker-cleanup-pro/issues) and we'll add it to the FAQ!
