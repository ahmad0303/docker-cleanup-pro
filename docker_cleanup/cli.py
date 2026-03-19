"""
Command-line interface for Docker Cleanup Pro.
"""

import argparse
import sys
from docker_cleanup.cleanup import DockerCleanup
from docker_cleanup import __version__


def create_parser():
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        description=(
            "Docker Cleanup Pro - Smart Docker cleanup that "
            "saves disk space without breaking things"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Safe cleanup with defaults
  docker-cleanup --safe

  # Dry run to see what would be removed
  docker-cleanup --dry-run

  # Keep more image versions
  docker-cleanup --safe --keep-versions 5

  # Clean everything including recent containers
  docker-cleanup --aggressive

  # Only clean images and build cache
  docker-cleanup --images --build-cache
        """,
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"Docker Cleanup Pro {__version__}",
    )

    # Cleanup modes
    mode_group = parser.add_argument_group("Cleanup Modes")
    mode_group.add_argument(
        "--safe",
        action="store_true",
        help=(
            "Safe mode: removes unused images (keeps last 3), "
            "old containers (7+ days), and dangling volumes"
        ),
    )
    mode_group.add_argument(
        "--aggressive",
        action="store_true",
        help=(
            "Aggressive mode: removes more aggressively "
            "(keeps last 1 version, 1 day old containers)"
        ),
    )
    mode_group.add_argument(
        "--dry-run",
        action="store_true",
        help=("Show what would be removed without actually " "removing anything"),
    )

    # Specific cleanup options
    cleanup_group = parser.add_argument_group("Specific Cleanup Options")
    cleanup_group.add_argument(
        "--images",
        action="store_true",
        help="Only clean up images",
    )
    cleanup_group.add_argument(
        "--containers",
        action="store_true",
        help="Only clean up containers",
    )
    cleanup_group.add_argument(
        "--volumes",
        action="store_true",
        help="Only clean up volumes",
    )
    cleanup_group.add_argument(
        "--build-cache",
        action="store_true",
        help="Only clean up build cache",
    )

    # Configuration options
    config_group = parser.add_argument_group("Configuration Options")
    config_group.add_argument(
        "--keep-versions",
        type=int,
        default=3,
        metavar="N",
        help=("Number of image versions to keep per repository " "(default: 3)"),
    )
    config_group.add_argument(
        "--keep-recent-days",
        type=int,
        default=7,
        metavar="N",
        help=("Keep containers stopped within N days (default: 7)"),
    )

    return parser


def confirm_cleanup(dry_run: bool) -> bool:
    """Ask user for confirmation before cleanup."""
    if dry_run:
        return True

    try:
        response = input("\n This will remove Docker resources. " "Continue? [y/N]: ")
        return response.lower() in ["y", "yes"]
    except KeyboardInterrupt:
        print("\n\n Cleanup cancelled")
        return False


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Handle modes
    if args.aggressive:
        keep_versions = 1
        keep_recent_days = 1
        print("Running in AGGRESSIVE mode")
    elif args.safe:
        keep_versions = args.keep_versions
        keep_recent_days = args.keep_recent_days
        print("Running in SAFE mode")
    else:
        keep_versions = args.keep_versions
        keep_recent_days = args.keep_recent_days

    # Determine what to clean
    specific_cleanup = any(
        [
            args.images,
            args.containers,
            args.volumes,
            args.build_cache,
        ]
    )

    if specific_cleanup:
        include_images = args.images
        include_containers = args.containers
        include_volumes = args.volumes
        include_build_cache = args.build_cache
    else:
        include_images = True
        include_containers = True
        include_volumes = True
        include_build_cache = True

    # Confirm before proceeding
    if not confirm_cleanup(args.dry_run):
        sys.exit(0)

    try:
        cleanup = DockerCleanup(
            dry_run=args.dry_run,
            keep_versions=keep_versions,
            keep_recent_days=keep_recent_days,
        )

        cleanup.run_cleanup(
            include_images=include_images,
            include_containers=include_containers,
            include_volumes=include_volumes,
            include_build_cache=include_build_cache,
        )

        print("\nCleanup completed successfully!")

    except Exception as e:
        print(f"\nError during cleanup: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
