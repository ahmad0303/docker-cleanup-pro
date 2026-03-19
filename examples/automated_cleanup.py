#!/usr/bin/env python3
"""
Example: Automated cleanup for CI/CD pipelines.

This script shows how to use Docker Cleanup Pro in automated environments
like CI/CD pipelines, cron jobs, or scheduled tasks.
"""

import sys
from docker_cleanup.cleanup import DockerCleanup


def automated_cleanup(max_space_threshold_gb: float = 50.0):
    """
    Run automated cleanup if disk usage is high.
    
    Args:
        max_space_threshold_gb: Run cleanup if Docker is using more than this many GB
    """
    
    # Initialize cleanup
    cleanup = DockerCleanup(dry_run=False, keep_versions=2, keep_recent_days=3)
    
    # Get current disk usage
    usage = cleanup.get_disk_usage()
    
    # Calculate total size (approximate)
    total_size = 0
    for category in ['images', 'containers', 'volumes']:
        if category in usage:
            total_size += sum(item.get('Size', 0) for item in usage.get(category, []))
    
    total_size_gb = total_size / (1024**3)
    
    print(f"Current Docker disk usage: {total_size_gb:.2f} GB")
    
    if total_size_gb > max_space_threshold_gb:
        print(f"Threshold exceeded ({max_space_threshold_gb} GB). Running cleanup...")
        
        # Run cleanup
        cleanup.run_cleanup()
        
        print("Automated cleanup completed successfully!")
        return 0
    else:
        print(f"Disk usage is below threshold. No cleanup needed.")
        return 0


def scheduled_maintenance():
    """
    Run regular scheduled maintenance cleanup.
    Use this in cron jobs for weekly/monthly cleanup.
    """
    
    print("Running scheduled Docker maintenance...")
    
    cleanup = DockerCleanup(dry_run=False, keep_versions=3, keep_recent_days=7)
    
    # Run full cleanup
    cleanup.run_cleanup()
    
    # Print summary
    print("\nMaintenance Summary:")
    print(f"  Images removed: {cleanup.stats['images_removed']}")
    print(f"  Containers removed: {cleanup.stats['containers_removed']}")
    print(f"  Volumes removed: {cleanup.stats['volumes_removed']}")
    print(f"  Space saved: {cleanup._format_size(cleanup.stats['space_saved'])}")
    
    return 0


if __name__ == '__main__':
    # Example: Run automated cleanup if usage > 50GB
    # sys.exit(automated_cleanup(max_space_threshold_gb=50.0))
    
    # Example: Run scheduled maintenance
    sys.exit(scheduled_maintenance())
