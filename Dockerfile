FROM python:3.11-slim

# Metadata
LABEL maintainer="realahmad001@gmail.com"
LABEL description="Docker Cleanup Pro - Smart Docker cleanup tool"
LABEL version="1.0.0"

# Install Docker CLI (needed to communicate with Docker daemon)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    docker.io && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY docker_cleanup/ ./docker_cleanup/
COPY setup.py pyproject.toml README.md LICENSE ./

# Install the package
RUN pip install --no-cache-dir -e .

# Create non-root user for security
RUN useradd -m -u 1000 cleanupuser && \
    chown -R cleanupuser:cleanupuser /app

# Switch to non-root user
USER cleanupuser

# Default command
ENTRYPOINT ["docker-cleanup"]
CMD ["--help"]

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD docker-cleanup --version || exit 1
