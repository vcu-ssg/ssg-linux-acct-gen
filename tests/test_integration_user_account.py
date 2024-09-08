"""
"""
import os
import unittest
import subprocess
from src.utils import USER_FOLDER, WWW_ROOT, create_user_account, delete_user_account, create_team_group_and_directory, delete_team_group_and_directory

class TestUserIntegration(unittest.TestCase):

    def setUp(self):
        """ Ensure the test environment is clean before each test """
        username = 'testuser'
        testteam = 'testteam'
        subprocess.run(f"userdel -r {username}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(f"groupdel {username}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(f"groupdel {testteam}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def tearDown(self):
        """ Clean up after each test """
        username = 'testuser'
        testteam = 'testteam'
        subprocess.run(f"userdel -r {username}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(f"groupdel {username}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        subprocess.run(f"groupdel {testteam}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def test_delete_user_account_integration(self):
        """ verify delete user account using real commands """
        username = 'testuser'
        
        # First, create the user and group
        create_user_account(username)

        # Verify that the user was created
        result = subprocess.run(f"getent passwd {username}", shell=True, stdout=subprocess.PIPE)
        self.assertIn(f"{username}", result.stdout.decode(), "User was not created")

        # Now, run the function to delete the user and group
        delete_user_account(username)
        
        # Verify that the user was deleted
        result = subprocess.run(f"getent passwd {username}", shell=True, stdout=subprocess.PIPE)
        self.assertNotIn(f"{username}", result.stdout.decode(), "User was not deleted")

        # Verify that the group was deleted
        result = subprocess.run(f"getent group {username}", shell=True, stdout=subprocess.PIPE)
        self.assertNotIn(f"{username}", result.stdout.decode(), "Group was not deleted")

    def test_delete_team_and_directory_integration(self):
        """ verify delete_team_and_directory using real commands """
        group_name = 'testteam'
        
        # Create the team and directory
        create_team_group_and_directory(group_name)

        # Verify that the group was created
        result = subprocess.run(f"getent group {group_name}", shell=True, stdout=subprocess.PIPE)
        self.assertIn(f"{group_name}", result.stdout.decode(), "Group was not created")

        # Verify that the team directory was created
        base_dir = f"{USER_FOLDER}/{group_name}"
        self.assertTrue(os.path.exists(base_dir), "Team directory was not created")

        # Verify that the symbolic link was created
        symlink_path = f"{WWW_ROOT}/{group_name}"
        self.assertTrue(os.path.islink(symlink_path), "Symbolic link was not created")

        # Now delete the team and directory
        delete_team_group_and_directory(group_name)

        # Verify that the group was deleted
        result = subprocess.run(f"getent group {group_name}", shell=True, stdout=subprocess.PIPE)
        self.assertNotIn(f"{group_name}", result.stdout.decode(), "Group was not deleted")

        # Verify that the team directory was deleted
        self.assertFalse(os.path.exists(base_dir), "Team directory was not deleted")

        # Verify that the symbolic link was deleted
        self.assertFalse(os.path.islink(symlink_path), "Symbolic link was not deleted")

if __name__ == '__main__':
    unittest.main()
