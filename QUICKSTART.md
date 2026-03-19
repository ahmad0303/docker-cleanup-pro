# Quick Start Guide

Get Docker Cleanup Pro running in under 2 minutes!

## ⚡ Super Quick Start

```bash
# 1. Install
pip install docker-cleanup-pro

# 2. Run
docker-cleanup --safe
```

That's it! You're cleaning up Docker resources safely.

## 🎯 First Time User Path

### Step 1: Check What Docker Is Using

```bash
docker system df
```

Example output:
```
TYPE            TOTAL   ACTIVE   SIZE      RECLAIMABLE
Images          42      12       15.2GB    12.8GB (84%)
Containers      28      3        2.1GB     2.0GB (95%)
Local Volumes   8       2        850MB     600MB (70%)
Build Cache     152     0        3.2GB     3.2GB (100%)
```

### Step 2: Preview Cleanup (Dry Run)

```bash
docker-cleanup --dry-run
```

You'll see:
```
🚀 Docker Cleanup Pro
==================================================
🔍 DRY RUN MODE - Nothing will be removed

🖼️  Cleaning up images...
  [DRY RUN] Would remove: myapp:v1.0.0 (245.32 MB)
  [DRY RUN] Would remove: myapp:v0.9.0 (238.15 MB)
  ...

📊 Cleanup Summary
==================================================
Images removed:     15
Containers removed: 8
Volumes removed:    3
Space saved:        8.5 GB
```

### Step 3: Run Actual Cleanup

```bash
docker-cleanup --safe
```

Confirm when prompted:
```
⚠️  This will remove Docker resources. Continue? [y/N]: y
```

### Step 4: Verify Results

```bash
docker system df
```

You should see reduced disk usage!

## 🎓 Common Usage Patterns

### Pattern 1: Weekly Maintenance
```bash
# Every week, run safe cleanup
docker-cleanup --safe
```

### Pattern 2: Emergency Space Recovery
```bash
# When disk is full, use aggressive mode
docker-cleanup --aggressive
```

### Pattern 3: CI/CD Server Cleanup
```bash
# Keep fewer versions on build servers
docker-cleanup --safe --keep-versions 1
```

### Pattern 4: Selective Cleanup
```bash
# Only clean images and build cache
docker-cleanup --images --build-cache
```

## 🔧 Customization Examples

### Keep More Versions
```bash
# Keep last 5 versions of each image
docker-cleanup --safe --keep-versions 5
```

### Different Retention Period
```bash
# Remove containers older than 14 days
docker-cleanup --safe --keep-recent-days 14
```

### Combine Settings
```bash
# Custom safe cleanup
docker-cleanup --keep-versions 2 --keep-recent-days 3
```

## 📋 Pre-Flight Checklist

Before running cleanup, verify:

- [ ] Docker is running: `docker ps`
- [ ] You have Docker access: `docker images`
- [ ] You know what to keep (check running containers)
- [ ] You've backed up anything critical
- [ ] You've run `--dry-run` first

## 🚨 Safety Tips

1. **Always start with dry-run**:
   ```bash
   docker-cleanup --dry-run
   ```

2. **Use safe mode first**:
   ```bash
   docker-cleanup --safe
   ```

3. **Check what's running**:
   ```bash
   docker ps
   ```

4. **Keep important images**:
   Running containers' images are automatically kept!

5. **Review the summary**:
   Read what was removed before closing the terminal.

## 🎯 Goal-Based Quick Commands

### Goal: "I just want to free up space safely"
```bash
docker-cleanup --safe
```

### Goal: "I want to see what would be removed first"
```bash
docker-cleanup --dry-run
```

### Goal: "I need space NOW"
```bash
docker-cleanup --aggressive
```

### Goal: "Only clean up old images"
```bash
docker-cleanup --images
```

### Goal: "I'm running low on space and need maximum cleanup"
```bash
docker-cleanup --aggressive --keep-versions 1
```

## 📱 One-Liner Commands

### Safe cleanup
```bash
pip install docker-cleanup-pro && docker-cleanup --safe
```

### Preview only
```bash
pip install docker-cleanup-pro && docker-cleanup --dry-run
```

### Install and get help
```bash
pip install docker-cleanup-pro && docker-cleanup --help
```

## 🔄 Automated Setup

### Linux/macOS Cron Job
```bash
# Edit crontab
crontab -e

# Add this line for weekly cleanup on Sundays at 2 AM
0 2 * * 0 /usr/local/bin/docker-cleanup --safe
```

### GitHub Actions
```yaml
- name: Cleanup Docker
  run: |
    pip install docker-cleanup-pro
    docker-cleanup --safe
```

## ❓ Quick Troubleshooting

### Problem: "Permission denied"
**Solution**:
```bash
sudo usermod -aG docker $USER
# Then log out and back in
```

### Problem: "Cannot connect to Docker"
**Solution**:
```bash
sudo systemctl start docker
```

### Problem: "Not freeing enough space"
**Solution**:
```bash
# Use aggressive mode
docker-cleanup --aggressive

# Or reduce retention
docker-cleanup --keep-versions 1 --keep-recent-days 1
```

## 📚 Learn More

- **Full documentation**: [README.md](README.md)
- **Installation guide**: [INSTALL.md](INSTALL.md)
- **FAQ**: [FAQ.md](FAQ.md)
- **Examples**: Check `examples/` directory

## 🎉 Next Steps

Now that you've got the basics:

1. ⭐ Star the repo if you find it useful
2. 📖 Read the full [README.md](README.md) for advanced features
3. 🤝 Contribute improvements
4. 💬 Share with other Docker users

---

**Ready to clean up Docker like a pro? Run:**
```bash
docker-cleanup --safe
```
