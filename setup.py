"""
Setup file for Docker Cleanup Pro.
For modern installations, use pyproject.toml.
This file exists for backwards compatibility with older pip versions.
"""

from setuptools import setup, find_packages

# Read long description from README
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="docker-cleanup-pro",
    version="1.0.0",
    author="Ahmad Bilal",
    author_email="realahmad001@gmail.com",
    description="Smart Docker cleanup that saves disk space without breaking things",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahmad0303/docker-cleanup-pro",
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=[
        "docker>=6.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "docker-cleanup=docker_cleanup.cli:main",
        ],
    },
    keywords="docker cleanup disk-space devops containers",
    project_urls={
        "Bug Tracker": "https://github.com/ahmad0303/docker-cleanup-pro/issues",
        "Documentation": "https://github.com/ahmad0303/docker-cleanup-pro#readme",
        "Source Code": "https://github.com/ahmad0303/docker-cleanup-pro",
    },
)
