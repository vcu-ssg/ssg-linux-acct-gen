import unittest
from unittest.mock import patch
from src.utils import create_user_account  # Assuming create_user_account is in src/mymodule.py

class TestCreateUserAccount(unittest.TestCase):

    @patch('src.utils.run_command')  # Mock the run_command function
    @patch('src.utils.logger')  # Mock the logger
    def test_create_user_account_success(self, mock_logger, mock_run_command):
        # Mock run_command to simulate successful command execution
        mock_run_command.return_value = None  # Assume run_command returns None on success

        username = 'testuser'
        create_user_account(username)

        # Verify that each command was called with the correct arguments
        mock_run_command.assert_any_call(f"useradd -U -m -d /home/24FA/{username} -k /etc/skel_for_cmsc408 {username}")
        mock_run_command.assert_any_call(f'echo "{username}:PASSWORD" | chpasswd')

        # Ensure logger.success was called
        mock_logger.success.assert_called_with(f"User '{username}' created successfully.")

    @patch('src.utils.run_command')  # Mock the run_command function
    @patch('src.utils.logger')  # Mock the logger
    def test_create_user_account_failure(self, mock_logger, mock_run_command):
        # Simulate a failure in one of the commands
        mock_run_command.side_effect = Exception("Command failed")

        username = 'testuser'
        
        with self.assertRaises(Exception):  # Expecting an exception to be raised
            create_user_account(username)

        # Ensure that logger.success was never called since there was an error
        mock_logger.success.assert_not_called()

if __name__ == '__main__':
    unittest.main()
