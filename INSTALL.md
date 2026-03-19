# Installation & Deployment Guide

Complete guide for installing and deploying Docker Cleanup Pro in various environments.

## Table of Contents

- [Installation Methods](#installation-methods)
- [Deployment Scenarios](#deployment-scenarios)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## Installation Methods

### 1. Install from PyPI (Recommended)

```bash
pip install docker-cleanup-pro
```

### 2. Install from Source

```bash
git clone https://github.com/ahmad0303/docker-cleanup-pro.git
cd docker-cleanup-pro
pip install -e .
```

### 3. Install in Virtual Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install
pip install docker-cleanup-pro
```

### 4. Install with Development Dependencies

```bash
pip install docker-cleanup-pro[dev]
```

### 5. System-Wide Installation (Linux/macOS)

```bash
sudo pip install docker-cleanup-pro
```

## Deployment Scenarios

### Scenario 1: Developer Workstation

**Use Case:** Clean up Docker periodically on development machine

**Installation:**
```bash
pip install docker-cleanup-pro
```

**Usage:**
```bash
# Weekly cleanup
docker-cleanup --safe
```

**Recommended Setup:**
- Run manually when disk space is low
- Or set up weekly cron job (see Cron Job section)

---

### Scenario 2: CI/CD Pipeline

**Use Case:** Clean up Docker resources after builds

**GitHub Actions Example:**
```yaml
# .github/workflows/cleanup.yml
name: Docker Cleanup
on:
  schedule:
    - cron: '0 2 * * 0'  # Weekly on Sunday at 2 AM

jobs:
  cleanup:
    runs-on: ubuntu-latest
    steps:
      - name: Install Docker Cleanup Pro
        run: pip install docker-cleanup-pro
      
      - name: Run Cleanup
        run: docker-cleanup --safe --keep-versions 2
```

**GitLab CI Example:**
```yaml
# .gitlab-ci.yml
docker-cleanup:
  stage: cleanup
  script:
    - pip install docker-cleanup-pro
    - docker-cleanup --safe
  only:
    - schedules
```

**Jenkins Example:**
```groovy
pipeline {
    agent any
    triggers {
        cron('H 2 * * 0')  // Weekly
    }
    stages {
        stage('Docker Cleanup') {
            steps {
                sh 'pip install docker-cleanup-pro'
                sh 'docker-cleanup --safe'
            }
        }
    }
}
```

---

### Scenario 3: Production Server (Cron Job)

**Use Case:** Scheduled cleanup on production Docker host

**Setup Steps:**

1. Install Docker Cleanup Pro:
```bash
sudo pip install docker-cleanup-pro
```

2. Create cleanup script:
```bash
sudo nano /usr/local/bin/docker-cleanup-scheduled
```

Add content:
```bash
#!/bin/bash
# Docker cleanup script

# Log file
LOG_FILE="/var/log/docker-cleanup.log"

# Run cleanup
echo "=== Docker Cleanup $(date) ===" >> $LOG_FILE
/usr/local/bin/docker-cleanup --safe >> $LOG_FILE 2>&1
echo "" >> $LOG_FILE
```

3. Make executable:
```bash
sudo chmod +x /usr/local/bin/docker-cleanup-scheduled
```

4. Add to crontab:
```bash
sudo crontab -e
```

Add line:
```cron
# Run Docker cleanup every Sunday at 2 AM
0 2 * * 0 /usr/local/bin/docker-cleanup-scheduled
```

---

### Scenario 4: Docker-in-Docker (DinD)

**Use Case:** Run cleanup inside a Docker container

**Dockerfile:**
```dockerfile
FROM docker:dind

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

# Install Docker Cleanup Pro
RUN pip3 install docker-cleanup-pro

# Entrypoint
ENTRYPOINT ["docker-cleanup"]
CMD ["--safe"]
```

**Build and Run:**
```bash
docker build -t docker-cleanup-pro .
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock docker-cleanup-pro --safe
```

---

### Scenario 5: Kubernetes CronJob

**Use Case:** Clean up Docker on Kubernetes nodes

**CronJob Manifest:**
```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: docker-cleanup
spec:
  schedule: "0 2 * * 0"  # Weekly on Sunday at 2 AM
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: docker-cleanup
            image: python:3.11-slim
            command:
            - /bin/bash
            - -c
            - |
              pip install docker-cleanup-pro
              docker-cleanup --safe
            volumeMounts:
            - name: docker-sock
              mountPath: /var/run/docker.sock
          volumes:
          - name: docker-sock
            hostPath:
              path: /var/run/docker.sock
          restartPolicy: OnFailure
```

---

### Scenario 6: Systemd Service (Linux)

**Use Case:** Run cleanup as a systemd timer

**Service File** (`/etc/systemd/system/docker-cleanup.service`):
```ini
[Unit]
Description=Docker Cleanup Service
After=docker.service

[Service]
Type=oneshot
ExecStart=/usr/local/bin/docker-cleanup --safe
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

**Timer File** (`/etc/systemd/system/docker-cleanup.timer`):
```ini
[Unit]
Description=Docker Cleanup Timer

[Timer]
OnCalendar=weekly
Persistent=true

[Install]
WantedBy=timers.target
```

**Enable and Start:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable docker-cleanup.timer
sudo systemctl start docker-cleanup.timer
```

**Check Status:**
```bash
sudo systemctl status docker-cleanup.timer
sudo systemctl list-timers
```

---

## Configuration

### Environment Variables

Set these before running:

```bash
# Python environment
export PYTHONUNBUFFERED=1

# Docker host (if not using default)
export DOCKER_HOST=tcp://localhost:2375
```

### Custom Settings File (Future Feature)

```yaml
# ~/.dockercleanup.yml
keep_versions: 5
keep_recent_days: 14
auto_confirm: true  # Skip confirmation prompts
```

---

## Troubleshooting

### Issue: Permission Denied

**Error:**
```
Permission denied while trying to connect to the Docker daemon socket
```

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Or run with sudo
sudo docker-cleanup --safe
```

---

### Issue: Docker Daemon Not Running

**Error:**
```
Error: Could not connect to Docker daemon
```

**Solution:**
```bash
# Check Docker status
sudo systemctl status docker

# Start Docker
sudo systemctl start docker
```

---

### Issue: Module Not Found

**Error:**
```
ModuleNotFoundError: No module named 'docker'
```

**Solution:**
```bash
# Install Docker SDK
pip install docker>=6.0.0

# Or reinstall docker-cleanup-pro
pip install --force-reinstall docker-cleanup-pro
```

---

### Issue: Cleanup Not Removing Enough

**Problem:** Still running out of disk space

**Solutions:**

1. Use aggressive mode:
```bash
docker-cleanup --aggressive
```

2. Reduce retention:
```bash
docker-cleanup --safe --keep-versions 1 --keep-recent-days 1
```

3. Manual cleanup after:
```bash
docker-cleanup --safe
docker system prune -a -f
```

---

## Monitoring & Logging

### Basic Logging

```bash
# Log to file
docker-cleanup --safe > /var/log/docker-cleanup.log 2>&1

# With timestamp
docker-cleanup --safe 2>&1 | ts '[%Y-%m-%d %H:%M:%S]' >> /var/log/docker-cleanup.log
```

### Advanced Monitoring

```bash
# Email results
docker-cleanup --safe 2>&1 | mail -s "Docker Cleanup Report" admin@example.com

# Slack webhook
docker-cleanup --safe 2>&1 | curl -X POST -H 'Content-type: application/json' \
  --data "{\"text\":\"Docker Cleanup Completed\"}" \
  YOUR_SLACK_WEBHOOK_URL
```

---

## Best Practices

1. **Start with dry-run:**
   ```bash
   docker-cleanup --dry-run
   ```

2. **Use safe mode initially:**
   ```bash
   docker-cleanup --safe
   ```

3. **Schedule during low-usage periods:**
   - Weekend nights
   - Early morning hours

4. **Monitor disk space:**
   ```bash
   df -h
   docker system df
   ```

5. **Keep logs:**
   - Maintain cleanup history
   - Track space saved over time

6. **Test in staging first:**
   - Verify behavior in non-production
   - Adjust settings based on results

---

## Support

For issues or questions:
- GitHub Issues: https://github.com/ahmad0303/docker-cleanup-pro/issues
- Documentation: https://github.com/ahmad0303/docker-cleanup-pro#readme
