"""
Tests for the cleanup module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from docker_cleanup.cleanup import DockerCleanup


def can_connect_to_docker():
    """Check if Docker daemon is available."""
    try:
        import docker
        client = docker.from_env()
        client.ping()
        return True
    except:
        return False


class TestDockerCleanup:
    """Tests for DockerCleanup class."""
    
    @patch('docker_cleanup.cleanup.docker.from_env')
    def test_init_default_values(self, mock_docker):
        """Test initialization with default values."""
        cleanup = DockerCleanup()
        
        assert cleanup.dry_run is False
        assert cleanup.keep_versions == 3
        assert cleanup.keep_recent_days == 7
        assert cleanup.stats == {
            "images_removed": 0,
            "containers_removed": 0,
            "volumes_removed": 0,
            "space_saved": 0
        }
    
    @patch('docker_cleanup.cleanup.docker.from_env')
    def test_init_custom_values(self, mock_docker):
        """Test initialization with custom values."""
        cleanup = DockerCleanup(dry_run=True, keep_versions=5, keep_recent_days=14)
        
        assert cleanup.dry_run is True
        assert cleanup.keep_versions == 5
        assert cleanup.keep_recent_days == 14
    
    @patch('docker_cleanup.cleanup.docker.from_env')
    def test_format_size_bytes(self, mock_docker):
        """Test size formatting in bytes."""
        result = DockerCleanup._format_size(500)
        assert result == "500.00 B"
    
    @patch('docker_cleanup.cleanup.docker.from_env')
    def test_format_size_kilobytes(self, mock_docker):
        """Test size formatting in kilobytes."""
        result = DockerCleanup._format_size(1024)
        assert result == "1.00 KB"
    
    @patch('docker_cleanup.cleanup.docker.from_env')
    def test_format_size_megabytes(self, mock_docker):
        """Test size formatting in megabytes."""
        result = DockerCleanup._format_size(1024 * 1024)
        assert result == "1.00 MB"
    
    @patch('docker_cleanup.cleanup.docker.from_env')
    def test_format_size_gigabytes(self, mock_docker):
        """Test size formatting in gigabytes."""
        result = DockerCleanup._format_size(1024 * 1024 * 1024)
        assert result == "1.00 GB"
    
    @patch('docker_cleanup.cleanup.docker.from_env')
    def test_dry_run_mode(self, mock_docker):
        """Test that dry run mode doesn't actually remove anything."""
        mock_client = MagicMock()
        mock_docker.return_value = mock_client
        
        # Setup mock images
        mock_image = MagicMock()
        mock_image.tags = ['test:v1.0.0']
        mock_image.short_id = 'abc123'
        mock_image.attrs = {'Created': '2026-01-01', 'Size': 1024 * 1024}
        
        mock_client.images.list.return_value = [mock_image]
        
        cleanup = DockerCleanup(dry_run=True, keep_versions=0)
        count, space = cleanup.cleanup_images()
        
        # In dry run, we count but don't actually remove
        assert count >= 0
        # Should not call remove in dry run mode
        mock_client.images.remove.assert_not_called()
    
    @patch('docker_cleanup.cleanup.docker.from_env')
    def test_get_disk_usage(self, mock_docker):
        """Test getting Docker disk usage."""
        mock_client = MagicMock()
        mock_docker.return_value = mock_client
        
        mock_client.df.return_value = {
            "Images": [],
            "Containers": [],
            "Volumes": [],
            "BuildCache": []
        }
        
        cleanup = DockerCleanup()
        usage = cleanup.get_disk_usage()
        
        assert "images" in usage
        assert "containers" in usage
        assert "volumes" in usage
        assert "build_cache" in usage


class TestCleanupOperations:
    """Tests for specific cleanup operations."""
    
    @patch('docker_cleanup.cleanup.docker.from_env')
    def test_cleanup_with_no_resources(self, mock_docker):
        """Test cleanup when there are no resources to remove."""
        mock_client = MagicMock()
        mock_docker.return_value = mock_client
        
        # Empty lists - nothing to clean
        mock_client.images.list.return_value = []
        mock_client.containers.list.return_value = []
        mock_client.volumes.list.return_value = []
        mock_client.df.return_value = {"BuildCache": []}
        
        cleanup = DockerCleanup()
        cleanup.run_cleanup()
        
        # Should handle empty case gracefully
        assert cleanup.stats["images_removed"] == 0
        assert cleanup.stats["containers_removed"] == 0
        assert cleanup.stats["volumes_removed"] == 0


@pytest.mark.integration
class TestDockerIntegration:
    """Integration tests requiring actual Docker daemon."""
    
    @pytest.mark.skipif(not can_connect_to_docker(), reason="Docker daemon not available")
    def test_real_docker_connection(self):
        """Test that we can connect to real Docker daemon."""
        cleanup = DockerCleanup()
        usage = cleanup.get_disk_usage()
        
        # Should return dict with expected keys
        assert isinstance(usage, dict)