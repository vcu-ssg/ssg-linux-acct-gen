"""

"""
import subprocess
from loguru import logger

TEST = True

def run_command(command):
    """ run_command """
    logger.debug(f"{command}")
    try:
        # Run the command and check for any errors.
        if TEST:
            logger.info(f"testing: {command}")
        else:
            result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            logger.info(f"{result.stdout}")
    except subprocess.CalledProcessError as e:
        # Raise an exception with a custom error message that includes the command and the stderr output.
        raise Exception(f"Command '{command}' failed with error:\n{e.stderr}")
    return

def create_user_account(username,team):
    try:
        run_command( f"groupadd 24FA_{username}" )
        run_command( f"adduser 24FA_{username} -d /home/24FA/24FA_{username} -m -k /etc/skel_for_cmsc508 -g 24FA_{username} -G {team}" )
        run_command( f'echo "24FA_{username}:PASSWORD" | chpasswd' )

        logger.success(f"User '{username}' created successfully.")

    except Exception as e:
        # If any command fails, this will print the error message with the command that failed
        print(f"Error occurred: {e}")
    
def create_team_and_directory(group_name):
    """ set up user directory """
    try:
        base_dir = f"/home/24FA/{group_name}"
        
        # Run all commands, exceptions will be raised and handled if any command fails
        run_command(f"mkdir -p {base_dir}")
        run_command(f"cp -r /etc/skel_for_cmsc508/. {base_dir}")
        run_command(f"chmod -R 775 {base_dir}")
        run_command(f"groupadd {group_name}")
        run_command(f"chgrp -R {group_name} {base_dir}")
        run_command(f"ln -s {base_dir}/public_html /var/www/html/24FA/{group_name}")
        
        logger.success(f"All commands for {group_name} executed successfully.")
    
    except Exception as e:
        # If any command fails, this will print the error message with the command that failed
        print(f"Error occurred: {e}")



UID_START_VALUE = 3000

# Note use of term "23FA" leader

## Commands to add project teams
## There is no project team account, just a project team group with membership to individual users

"""
mkdir /home/23FA/23FA_group00;
cp -r /etc/skel_for_cmsc508/. /home/23FA/23FA_group00;
chmod -R 775 /home/23FA/23FA_group00/;
groupadd 23FA_group00;
chgrp -R 23FA_group00 /home/23FA/23FA_group00;
ln -s /home/23FA/23FA_group00/public_html /var/www/html/23FA/23FA_group00;

## Commands to delete project teams
rm -fR /home/23FA/23FA_group00;
rm -fR /var/www/html/23FA/23FA_group00;
groupdel 23FA_group00;

## Commands to create user and group account
## project teams need to be created first!
groupadd 23FA_abdulmelikna;
adduser 23FA_abdulmelikna -d /home/23FA/23FA_abdulmelikna -m -k /etc/skel_for_cmsc508 -g 23FA_abdulmelikna -G group01
echo "23FA_abdulmelikna:V00935024" | chpasswd;

## Commands to delete user
userdel -rf 23FA_abdulmelikna

## Command to create an HTACCESS file for project team or user
echo "# .htaccess Configuration file for userdir" > /home/23FA/23FA_group00/public_html/.htaccess;
echo SetEnv SAMPLE_SERVER localhost >> /home/23FA/23FA_group00/public_html/.htaccess;
echo SetEnv SAMPLE_DB 23FA_groups_group00 >> /home/23FA/23FA_group00/public_html/.htaccess;
echo SetEnv SAMPLE_USER 23FA_group00 >> /home/23FA/23FA_group00/public_html/.htaccess;
echo SetEnv SAMPLE_PASS Shout4_group00_GOTEAM >> /home/23FA/23FA_group00/public_html/.htaccess;

## Create HTACCESS for user
echo "# autocreated .htaccess for userdir" > /home/23FA/23FA_abdulmelikna/public_html/.htaccess ;
echo SetEnv SAMPLE_SERVER localhost >> /home/23FA/23FA_abdulmelikna/public_html/.htaccess;
echo SetEnv SAMPLE_DB 23FA_users_abdulmelikna >> /home/23FA/23FA_abdulmelikna/public_html/.htaccess;
echo SetEnv SAMPLE_USER 23FA_abdulmelikna >> /home/23FA/23FA_abdulmelikna/public_html/.htaccess;
echo SetEnv SAMPLE_PASS Shout4_abdulmelikna_GOME >> /home/23FA/23FA_abdulmelikna/public_html/.htaccess;

## Commands to drop project database and users
drop database 23FA_groups_group00;
drop user '23FA_group00'@'localhost';
drop user '23FA_group00'@'%';
FLUSH PRIVILEGES;

## Commands to create project team databases
create database 23FA_groups_group00;
create user '23FA_group00'@'localhost' identified by 'Shout4_group00_GOTEAM';
create user '23FA_group00'@'%' identified by 'Shout4_group00_GOTEAM';
grant all privileges on 23FA_groups_group00.* to '23FA_group00'@'localhost';
grant all privileges on 23FA_groups_group00.* to '23FA_group00'@'%';
FLUSH PRIVILEGES;

## Commands to create users databases
create user '23FA_abdulmelikna'@'%' identified by 'Shout4_abdulmelikna_GOME';
create user '23FA_abdulmelikna'@'localhost' identified by 'Shout4_abdulmelikna_GOME';
create database 23FA_users_abdulmelikna;
grant all privileges on 23FA_users_abdulmelikna.* to '23FA_abdulmelikna'@'%';
grant all privileges on 23FA_users_abdulmelikna.* to '23FA_abdulmelikna'@'localhost';
grant all privileges on 23FA_groups_group01.* to '23FA_abdulmelikna'@'%';
grant all privileges on 23FA_groups_group01.* to '23FA_abdulmelikna'@'localhost';
create database 23FA_hr_abdulmelikna;
grant all privileges on 23FA_hr_abdulmelikna.* to '23FA_abdulmelikna'@'%';
grant all privileges on 23FA_hr_abdulmelikna.* to '23FA_abdulmelikna'@'localhost';
FLUSH PRIVILEGES;

## Commands to drop user databases
drop database 23FA_users_abdulmelikna;
drop database 23FA_hr_abdulmelikna;
drop user '23FA_abdulmelikna'@'localhost';
drop user '23FA_abdulmelikna'@'%';
FLUSH PRIVILEGES;

## Commands to populate user databases
mysql -u 23FA_abdulmelikna -D 23FA_hr_abdulmelikna --password=Shout4_abdulmelikna_GOME < HR.sql

"""
