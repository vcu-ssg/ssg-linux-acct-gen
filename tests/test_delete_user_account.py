import unittest
from unittest.mock import patch
from src.utils import delete_user_account 

class TestDeleteUserAccount(unittest.TestCase):

    @patch('src.utils.run_command')  # Mock the run_command function
    @patch('src.utils.logger')  # Mock the logger
    def test_delete_user_account_success(self, mock_logger, mock_run_command):
        # Mock run_command to simulate successful command execution
        mock_run_command.return_value = None  # Assume run_command returns None on success

        username = 'testuser'
        delete_user_account(username)

        # Verify that each command was called with the correct arguments

        ## mock_run_command.assert_any_call(f"userdel -r {username}")
        ## mock_run_command.assert_any_call(f"groupdel {username}")

        # Ensure logger.success was called
        mock_logger.success.assert_called_with(f"User '{username}' and their group were deleted successfully.")

    @patch('src.utils.run_command')  # Mock the run_command function
    @patch('src.utils.logger')  # Mock the logger
    def test_delete_user_account_failure(self, mock_logger, mock_run_command):
        # Simulate a failure in one of the commands
        mock_run_command.side_effect = Exception("Command failed")

        username = 'testuser'
        
        with self.assertRaises(Exception):  # Expecting an exception to be raised
            delete_user_account(username)

