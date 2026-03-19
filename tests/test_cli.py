"""
Tests for the CLI module.
"""

import pytest
from unittest.mock import patch, MagicMock
from docker_cleanup.cli import create_parser, main
import sys


class TestCLIParser:
    """Tests for argument parser."""
    
    def test_parser_creation(self):
        """Test that parser is created successfully."""
        parser = create_parser()
        assert parser is not None
    
    def test_safe_mode_flag(self):
        """Test --safe flag parsing."""
        parser = create_parser()
        args = parser.parse_args(['--safe'])
        assert args.safe is True
    
    def test_aggressive_mode_flag(self):
        """Test --aggressive flag parsing."""
        parser = create_parser()
        args = parser.parse_args(['--aggressive'])
        assert args.aggressive is True
    
    def test_dry_run_flag(self):
        """Test --dry-run flag parsing."""
        parser = create_parser()
        args = parser.parse_args(['--dry-run'])
        assert args.dry_run is True
    
    def test_keep_versions_option(self):
        """Test --keep-versions option."""
        parser = create_parser()
        args = parser.parse_args(['--keep-versions', '5'])
        assert args.keep_versions == 5
    
    def test_keep_recent_days_option(self):
        """Test --keep-recent-days option."""
        parser = create_parser()
        args = parser.parse_args(['--keep-recent-days', '14'])
        assert args.keep_recent_days == 14
    
    def test_specific_cleanup_images(self):
        """Test --images flag."""
        parser = create_parser()
        args = parser.parse_args(['--images'])
        assert args.images is True
    
    def test_specific_cleanup_containers(self):
        """Test --containers flag."""
        parser = create_parser()
        args = parser.parse_args(['--containers'])
        assert args.containers is True
    
    def test_specific_cleanup_volumes(self):
        """Test --volumes flag."""
        parser = create_parser()
        args = parser.parse_args(['--volumes'])
        assert args.volumes is True
    
    def test_specific_cleanup_build_cache(self):
        """Test --build-cache flag."""
        parser = create_parser()
        args = parser.parse_args(['--build-cache'])
        assert args.build_cache is True
    
    def test_combined_flags(self):
        """Test combining multiple flags."""
        parser = create_parser()
        args = parser.parse_args(['--safe', '--dry-run', '--keep-versions', '2'])
        assert args.safe is True
        assert args.dry_run is True
        assert args.keep_versions == 2


class TestCLIMain:
    """Tests for main CLI function."""
    
    @patch('docker_cleanup.cli.DockerCleanup')
    @patch('docker_cleanup.cli.confirm_cleanup')
    def test_main_safe_mode(self, mock_confirm, mock_cleanup_class):
        """Test main function with safe mode."""
        mock_confirm.return_value = True
        mock_cleanup = MagicMock()
        mock_cleanup_class.return_value = mock_cleanup
        
        with patch.object(sys, 'argv', ['docker-cleanup', '--safe']):
            main()
        
        # Should create cleanup instance
        mock_cleanup_class.assert_called_once()
        # Should run cleanup
        mock_cleanup.run_cleanup.assert_called_once()
    
    @patch('docker_cleanup.cli.DockerCleanup')
    @patch('docker_cleanup.cli.confirm_cleanup')
    def test_main_dry_run_no_confirmation(self, mock_confirm, mock_cleanup_class):
        """Test that dry run doesn't need confirmation."""
        mock_cleanup = MagicMock()
        mock_cleanup_class.return_value = mock_cleanup
        
        with patch.object(sys, 'argv', ['docker-cleanup', '--dry-run']):
            main()
        
        # Confirm should return True for dry run
        mock_confirm.assert_called_once_with(True)
    
    @patch('docker_cleanup.cli.DockerCleanup')
    @patch('docker_cleanup.cli.confirm_cleanup')
    def test_main_user_cancels(self, mock_confirm, mock_cleanup_class):
        """Test user canceling the operation."""
        mock_confirm.return_value = False
        
        with patch.object(sys, 'argv', ['docker-cleanup', '--safe']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0
    
    @patch('docker_cleanup.cli.DockerCleanup')
    @patch('docker_cleanup.cli.confirm_cleanup')
    def test_main_aggressive_mode(self, mock_confirm, mock_cleanup_class):
        """Test main function with aggressive mode."""
        mock_confirm.return_value = True
        mock_cleanup = MagicMock()
        mock_cleanup_class.return_value = mock_cleanup
        
        with patch.object(sys, 'argv', ['docker-cleanup', '--aggressive']):
            main()
        
        # Should initialize with aggressive settings
        call_args = mock_cleanup_class.call_args
        assert call_args[1]['keep_versions'] == 1
        assert call_args[1]['keep_recent_days'] == 1
    
    @patch('docker_cleanup.cli.DockerCleanup')
    @patch('docker_cleanup.cli.confirm_cleanup')
    def test_main_specific_cleanup(self, mock_confirm, mock_cleanup_class):
        """Test main function with specific cleanup options."""
        mock_confirm.return_value = True
        mock_cleanup = MagicMock()
        mock_cleanup_class.return_value = mock_cleanup
        
        with patch.object(sys, 'argv', ['docker-cleanup', '--images', '--containers']):
            main()
        
        # Should only clean specified resources
        call_args = mock_cleanup.run_cleanup.call_args
        assert call_args[1]['include_images'] is True
        assert call_args[1]['include_containers'] is True
        assert call_args[1]['include_volumes'] is False
        assert call_args[1]['include_build_cache'] is False


class TestConfirmation:
    """Tests for confirmation prompt."""
    
    @patch('builtins.input')
    def test_confirm_yes(self, mock_input):
        """Test confirmation with 'yes' input."""
        from docker_cleanup.cli import confirm_cleanup
        mock_input.return_value = 'yes'
        assert confirm_cleanup(False) is True
    
    @patch('builtins.input')
    def test_confirm_y(self, mock_input):
        """Test confirmation with 'y' input."""
        from docker_cleanup.cli import confirm_cleanup
        mock_input.return_value = 'y'
        assert confirm_cleanup(False) is True
    
    @patch('builtins.input')
    def test_confirm_no(self, mock_input):
        """Test confirmation with 'no' input."""
        from docker_cleanup.cli import confirm_cleanup
        mock_input.return_value = 'no'
        assert confirm_cleanup(False) is False
    
    @patch('builtins.input')
    def test_confirm_empty(self, mock_input):
        """Test confirmation with empty input (default no)."""
        from docker_cleanup.cli import confirm_cleanup
        mock_input.return_value = ''
        assert confirm_cleanup(False) is False
    
    def test_confirm_dry_run_auto_yes(self):
        """Test that dry run mode auto-confirms."""
        from docker_cleanup.cli import confirm_cleanup
        assert confirm_cleanup(True) is True
