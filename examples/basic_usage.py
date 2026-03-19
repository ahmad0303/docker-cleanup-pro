#!/usr/bin/env python3
"""
Example: Basic cleanup usage with Docker Cleanup Pro.

This script demonstrates how to use Docker Cleanup Pro programmatically.
"""

from docker_cleanup.cleanup import DockerCleanup


def main():
    """Run a basic cleanup operation."""
    
    # Initialize cleanup in dry-run mode
    print("Running dry-run cleanup to preview changes...\n")
    cleanup = DockerCleanup(dry_run=True, keep_versions=3, keep_recent_days=7)
    
    # Run cleanup
    cleanup.run_cleanup(
        include_images=True,
        include_containers=True,
        include_volumes=True,
        include_build_cache=True
    )
    
    print("\n" + "="*50)
    print("To actually perform cleanup, run:")
    print("  docker-cleanup --safe")
    print("="*50)


if __name__ == '__main__':
    main()
