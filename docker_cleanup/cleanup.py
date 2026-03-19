"""
Core cleanup logic for Docker Cleanup Pro.
Handles safe removal of images, volumes, and containers.
"""

import docker
from datetime import datetime, timedelta
from typing import Dict, Tuple
import json
from pathlib import Path


class DockerCleanup:
    """Main cleanup class with safety features."""

    def __init__(
        self,
        dry_run: bool = False,
        keep_versions: int = 3,
        keep_recent_days: int = 7,
    ):
        """
        Initialize Docker cleanup.

        Args:
            dry_run: If True, only show what would be removed
            keep_versions: Number of image versions to keep per repository
            keep_recent_days: Keep containers stopped within this many days
        """
        self.client = docker.from_env()
        self.dry_run = dry_run
        self.keep_versions = keep_versions
        self.keep_recent_days = keep_recent_days
        self.rollback_file = Path.home() / ".docker-cleanup-rollback.json"
        self.stats = {
            "images_removed": 0,
            "containers_removed": 0,
            "volumes_removed": 0,
            "space_saved": 0,
        }

    def get_disk_usage(self) -> Dict:
        """Get current Docker disk usage."""
        try:
            df = self.client.df()
            return {
                "images": df.get("Images", []),
                "containers": df.get("Containers", []),
                "volumes": df.get("Volumes", []),
                "build_cache": df.get("BuildCache", []),
            }
        except Exception as e:
            print(f"Warning: Could not get disk usage: {e}")
            return {}

    def save_rollback_state(self, removed_items: Dict):
        """Save removed items for potential rollback."""
        try:
            with open(self.rollback_file, "w") as f:
                json.dump(
                    {
                        "timestamp": datetime.now().isoformat(),
                        "removed": removed_items,
                    },
                    f,
                    indent=2,
                )
            print(f"Rollback state saved to {self.rollback_file}")
        except Exception as e:
            print(f"Warning: Could not save rollback state: {e}")

    def cleanup_images(self) -> Tuple[int, int]:
        """
        Clean up unused images, keeping the last N versions.

        Returns:
            Tuple of (images_removed, space_saved)
        """
        print("\nCleaning up images...")

        # Group images by repository
        images_by_repo = {}
        for image in self.client.images.list():
            for tag in image.tags:
                if ":" in tag:
                    repo = tag.split(":")[0]
                    if repo not in images_by_repo:
                        images_by_repo[repo] = []
                    images_by_repo[repo].append(image)

        # Sort by creation date and remove old versions
        removed_count = 0
        space_saved = 0
        removed_images = []

        for repo, images in images_by_repo.items():
            # Sort by created date (newest first)
            images.sort(key=lambda x: x.attrs["Created"], reverse=True)

            # Keep only the last N versions
            to_remove = images[self.keep_versions :]

            for image in to_remove:
                try:
                    size = image.attrs.get("Size", 0)
                    tags = image.tags or [image.short_id]

                    if self.dry_run:
                        print(
                            f"  [DRY RUN] Would remove: " f"{tags[0]} ({self._format_size(size)})"
                        )
                    else:
                        self.client.images.remove(image.id, force=False)
                        print(f"  Removed: {tags[0]} " f"({self._format_size(size)})")
                        removed_images.append({"id": image.id, "tags": tags, "size": size})
                        space_saved += size

                    removed_count += 1
                except docker.errors.APIError as e:
                    if "image is being used" in str(e):
                        print(f"Skipped (in use): {tags[0]}")
                    else:
                        print(f"Error removing {tags[0]}: {e}")

        # Remove dangling images
        dangling = self.client.images.list(filters={"dangling": True})
        for image in dangling:
            try:
                size = image.attrs.get("Size", 0)
                if self.dry_run:
                    print(
                        f"  [DRY RUN] Would remove dangling: "
                        f"{image.short_id} "
                        f"({self._format_size(size)})"
                    )
                else:
                    self.client.images.remove(image.id, force=False)
                    print(f"  Removed dangling: {image.short_id} " f"({self._format_size(size)})")
                    removed_images.append(
                        {
                            "id": image.id,
                            "tags": ["<none>"],
                            "size": size,
                        }
                    )
                    space_saved += size

                removed_count += 1
            except docker.errors.APIError as e:
                print(f"Error removing dangling image: {e}")

        if not self.dry_run and removed_images:
            self.save_rollback_state({"images": removed_images})

        return removed_count, space_saved

    def cleanup_containers(self) -> Tuple[int, int]:
        """
        Clean up old stopped containers.

        Returns:
            Tuple of (containers_removed, space_saved)
        """
        print("\nCleaning up containers...")

        cutoff_date = datetime.now() - timedelta(days=self.keep_recent_days)
        removed_count = 0
        space_saved = 0
        removed_containers = []

        for container in self.client.containers.list(all=True):
            # Skip running containers
            if container.status == "running":
                continue

            # Check if container is recent
            finished_at = container.attrs["State"].get("FinishedAt", "")
            if finished_at and finished_at != "0001-01-01T00:00:00Z":
                try:
                    finished_date = datetime.fromisoformat(finished_at.replace("Z", "+00:00"))
                    if finished_date.replace(tzinfo=None) > cutoff_date:
                        continue
                except Exception:
                    pass

            try:
                size = container.attrs.get("SizeRw", 0)
                name = container.name

                if self.dry_run:
                    print(f"  [DRY RUN] Would remove: {name} " f"(status: {container.status})")
                else:
                    container.remove(v=False)
                    print(f"  Removed: {name} " f"(status: {container.status})")
                    removed_containers.append({"id": container.id, "name": name, "size": size})
                    space_saved += size

                removed_count += 1
            except docker.errors.APIError as e:
                print(f"Error removing {container.name}: {e}")

        if not self.dry_run and removed_containers:
            self.save_rollback_state({"containers": removed_containers})

        return removed_count, space_saved

    def cleanup_volumes(self) -> Tuple[int, int]:
        """
        Clean up dangling volumes safely.

        Returns:
            Tuple of (volumes_removed, space_saved)
        """
        print("\nCleaning up volumes...")

        removed_count = 0
        space_saved = 0
        removed_volumes = []

        # Get dangling volumes (not attached to any container)
        dangling = self.client.volumes.list(filters={"dangling": True})

        for volume in dangling:
            try:
                name = volume.name

                if self.dry_run:
                    print(f"  [DRY RUN] Would remove: {name}")
                else:
                    volume.remove(force=False)
                    print(f"  Removed: {name}")
                    removed_volumes.append({"name": name})

                removed_count += 1
            except docker.errors.APIError as e:
                print(f"Error removing volume {volume.name}: {e}")

        if not self.dry_run and removed_volumes:
            self.save_rollback_state({"volumes": removed_volumes})

        return removed_count, space_saved

    def cleanup_build_cache(self) -> int:
        """
        Clean up build cache.

        Returns:
            Space saved in bytes
        """
        print("\nCleaning up build cache...")

        try:
            if self.dry_run:
                result = self.client.df()
                cache_size = sum(item.get("Size", 0) for item in result.get("BuildCache", []))
                print(f"  [DRY RUN] Would remove build cache " f"({self._format_size(cache_size)})")
                return 0
            else:
                result = self.client.api.prune_builds()
                space_saved = result.get("SpaceReclaimed", 0)
                print(f"  Removed build cache " f"({self._format_size(space_saved)})")
                return space_saved
        except Exception as e:
            print(f"Error cleaning build cache: {e}")
            return 0

    def run_cleanup(
        self,
        include_images: bool = True,
        include_containers: bool = True,
        include_volumes: bool = True,
        include_build_cache: bool = True,
    ):
        """
        Run the complete cleanup process.

        Args:
            include_images: Clean up images
            include_containers: Clean up containers
            include_volumes: Clean up volumes
            include_build_cache: Clean up build cache
        """
        print("Docker Cleanup Pro")
        print("=" * 50)

        if self.dry_run:
            print("DRY RUN MODE - Nothing will be removed")

        total_removed = 0
        total_space = 0

        # Run cleanup operations
        if include_images:
            count, space = self.cleanup_images()
            self.stats["images_removed"] = count
            total_space += space
            total_removed += count

        if include_containers:
            count, space = self.cleanup_containers()
            self.stats["containers_removed"] = count
            total_space += space
            total_removed += count

        if include_volumes:
            count, space = self.cleanup_volumes()
            self.stats["volumes_removed"] = count
            total_space += space
            total_removed += count

        if include_build_cache:
            space = self.cleanup_build_cache()
            total_space += space

        self.stats["space_saved"] = total_space

        # Print summary
        print("\n" + "=" * 50)
        print("Cleanup Summary")
        print("=" * 50)
        print(f"Images removed:     {self.stats['images_removed']}")
        print(f"Containers removed: {self.stats['containers_removed']}")
        print(f"Volumes removed:    {self.stats['volumes_removed']}")
        print(f"Space saved:        {self._format_size(total_space)}")

        if not self.dry_run and total_removed > 0:
            print(f"\nRollback info saved to: {self.rollback_file}")

        print("=" * 50)

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format bytes to human-readable size."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} PB"
