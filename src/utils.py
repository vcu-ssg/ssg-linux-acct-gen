"""

"""
import os
import re
import click
import subprocess
from loguru import logger
from src.logging import DEFAULT_LOG_LEVEL, set_logger, sniff_log_level

TEST = False

TERM_CODE = "24FA"
USER_SKELETON = "/etc/skel_for_cmsc408"
USER_FOLDER = f"/home/{TERM_CODE}"
WWW_ROOT = f"/var/www/html/{TERM_CODE}"
DB_TEAM_ROOT = f"{TERM_CODE}_teams"
DB_USER_ROOT = f"{TERM_CODE}_users"
DB_HR_ROOT = f"{TERM_CODE}_hr"
USER_LOWER_UID = 3000
GROUP_LOWER_GID = 3000

logger.remove()
early_log_level = sniff_log_level()
if early_log_level is None:
    early_log_level=DEFAULT_LOG_LEVEL

set_logger( early_log_level )

def get_users_with_uid_above(min_uid=USER_LOWER_UID):
    """Return a list of users with a UID greater than min_uid from /etc/passwd."""
    users = []
    
    # Read /etc/passwd and extract user details
    with open("/etc/passwd", "r") as passwd_file:
        for line in passwd_file:
            fields = line.split(":")
            username = fields[0]   # Username is the first field
            uid = int(fields[2])   # UID is the third field
            
            # Check if UID is greater than the specified min_uid
            if (uid >= min_uid) and (username.startswith(f"{TERM_CODE}_")):
                users.append(username)
    
    return users

def list_users_on_server():
    """ list users with uid above threshhold """
    for i,user in enumerate(get_users_with_uid_above()):
        print( user )

def get_groups_with_gid_above(min_gid=GROUP_LOWER_GID):
    """Return a list of groups with a GID greater than or equal to min_gid from /etc/group."""
    groups = []
    
    # Read /etc/group and extract group details
    with open("/etc/group", "r") as group_file:
        for line in group_file:
            fields = line.split(":")
            group_name = fields[0]  # Group name is the first field
            gid = int(fields[2])    # GID is the third field
            
            # Check if GID is greater than or equal to the specified min_gid
            if (gid >= min_gid) and (group_name.startswith(f"{TERM_CODE}_")):
                groups.append(group_name)
    return groups

def list_groups_on_server():
    """ list groups with gid above threshhold """
    for i,group in enumerate(get_groups_with_gid_above()):
        print( group )

def get_next_available_uid(min_uid=USER_LOWER_UID):
    """Read /etc/passwd and determine the next available UID after min_uid."""
    used_uids = set()
    
    # Read /etc/passwd and extract the UIDs
    with open("/etc/passwd", "r") as passwd_file:
        for line in passwd_file:
            fields = line.split(":")
            uid = int(fields[2])  # UID is the third field
            used_uids.add(uid)
    
    # Start checking from the minimum UID
    next_uid = min_uid
    while next_uid in used_uids:
        next_uid += 1
    
    return next_uid

def get_next_available_gid(min_gid=GROUP_LOWER_GID):
    """Return the next available GID greater than or equal to min_gid from /etc/group."""
    used_gids = set()

    # Read /etc/group and extract GIDs
    with open("/etc/group", "r") as group_file:
        for line in group_file:
            fields = line.split(":")
            gid = int(fields[2])  # GID is the third field
            used_gids.add(gid)

    # Start checking from min_gid and find the next available GID
    next_gid = min_gid
    while next_gid in used_gids:
        next_gid += 1
    return next_gid

# Global variable to store sudo password
SUDO_PASSWORD = None

def get_sudo_password():
    """Prompt the user for their sudo password."""
    global SUDO_PASSWORD
    if SUDO_PASSWORD is None:
        SUDO_PASSWORD = click.prompt("Enter your sudo password", hide_input=True)
    return SUDO_PASSWORD

def run_command(command, use_sudo=False):
    """Run a shell command, optionally using sudo."""
    cmd = command
    try:
        if TEST:
            logger.info(f"testing: {command}")
        else:
            logger.debug(f"{command}")
            if use_sudo:
                sudo_password = get_sudo_password()
                cmd = f"echo {sudo_password} | sudo -S {command}"
            result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return result
    except subprocess.CalledProcessError as e:
        raise Exception(f"Command '{command}' failed with error:\n{e.stderr}")
    return 0

def clean_user_name(team_name):
    # Convert to lowercase (optional for consistency)
    if not team_name.startswith( TERM_CODE ):
        fixed_name = f"{TERM_CODE}_" + team_name.lower()
    else:
        fixed_name = team_name
    
    # Replace hyphens and other invalid characters with underscores
    fixed_name = re.sub(r'[^a-zA-Z0-9_]', '_', fixed_name)
    
    # Ensure the name is not longer than 64 characters
    fixed_name = fixed_name[:64]
    
    return fixed_name

def clean_name_for_linux_group( name ):
    """ remove characters to create a valid linux group name """
    fixed_name = re.sub(r'[^a-zA-Z0-9]', '', name)
    fixed_name = fixed_name[:64]
    return fixed_name

def db_password( name ):
    """ return a database password for user account 'name' """
    passwd = f"Shout4_{name}_JOY"
    return passwd

def group_exists(groupname):
    """ Check if a group exists on the system """
    cmd = f"getent group {groupname}"
    logger.debug( cmd )
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def user_exists(username):
    """ Check if a group exists on the system """
    cmd = f"getent passwd {username}"
    logger.debug( cmd )
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def group_exists_raw( groupname ):
    return group_exists( clean_user_name( groupname ) )

def user_exists_raw( username ):
    return user_exists( clean_user_name( username ))

def create_directory_if_not_exists(directory):
    """Create the directory if it doesn't exist."""
    try:
        run_command( f"mkdir -p {directory}", use_sudo=True)
    except Exception as e:
        logger.error(f"Error creating directory {directory}: {e}")
        raise

def create_htaccess_file(html_folder, username):
    """Create an .htaccess file in the specified folder with hardcoded environment variables."""
    htaccess_content = f"""# Autogenerated by Dr. Leonard for {username}

# Deny access to .htaccess file itself
<Files .htaccess>
    Order Allow,Deny
    Deny from all
</Files>

# Enable URL rewriting
RewriteEngine On

# Environment variables for the DB connection
SetEnv SAMPLE_SERVER localhost
SetEnv SAMPLE_DB {DB_TEAM_ROOT}_{username}
SetEnv SAMPLE_USER {username}
SetEnv SAMPLE_PASS {db_password( username ) }
"""

    # Create the .htaccess file path
    htaccess_path = os.path.join(html_folder, ".htaccess")
    
    try:
        # Write the .htaccess content to the file
        command = f"""
echo "{htaccess_content}" | sudo tee {htaccess_path} > /dev/null
"""
        logger.debug("Running .htaccess create")
        run_command(command, use_sudo=False)
   
    except Exception as e:
        logger.error(f"Error creating .htaccess file: {e}")
        raise


def create_user_account(username):
    """ create user account with complementy user group """
    try:
        term_username = f"{username}"
        logger.debug(f"term_username: {username}")
        term_groupname = clean_name_for_linux_group( term_username )
        term_groupname = term_username
        logger.debug(f"term_groupname: {term_groupname}")

        if not group_exists( term_groupname ):
            gid = get_next_available_gid()
            run_command( f"groupadd -g {gid} {term_groupname}", use_sudo=True)

        if not user_exists( term_username ):
            uid = get_next_available_uid()
            run_command( f"useradd -u {uid} -g {term_groupname} -m -d {USER_FOLDER}/{term_username} -k {USER_SKELETON} -s /bin/bash {term_username}", use_sudo=True )
            run_command( f'echo "{term_username}:PASSWORD" | sudo -S chpasswd', use_sudo=True )
        html_folder = f"{USER_FOLDER}/{term_username}/public_html"
        create_directory_if_not_exists( html_folder )
        create_htaccess_file( html_folder, term_username )

        run_command( f"chown -R {term_username}:{term_groupname} {USER_FOLDER}/{term_username}", use_sudo=True)
        run_command( f"chmod -R 775 {USER_FOLDER}/{term_username}",use_sudo=True)
        create_directory_if_not_exists( WWW_ROOT )
        if not os.path.islink( f"{WWW_ROOT}/{term_username}" ):
            cmd = f"ln -s {USER_FOLDER}/{term_username}/public_html {WWW_ROOT}/{term_username}"
            run_command(cmd, use_sudo=True)
    except Exception as e:
        # If any command fails, this will print the error message with the command that failed
        logger.error(f"Error occurred: {e}")
        raise

def delete_user_account(username):
    """ delete user account and complementary user group """
    term_username = f"{username}"
    term_groupname = clean_name_for_linux_group( term_username )
    term_groupname = term_username
    try:
        if os.path.islink( f"{WWW_ROOT}/{term_username}" ):
            cmd = f"rm {WWW_ROOT}/{term_username}"
            run_command(cmd, use_sudo=True)

        html_folder = f"{USER_FOLDER}/{term_username}/public_html"
        run_command( f"rm -fR {html_folder}", use_sudo=True)
        if user_exists( term_username ):
            run_command(f"userdel -r {term_username}", use_sudo=True)
        if group_exists( term_groupname ):
            run_command(f"groupdel {term_groupname}", use_sudo=True)
        logger.success(f"User '{term_username}' and their group were deleted successfully.")
    except Exception as e:
        logger.error(f"Error occurred: {e}")
        raise


def create_database_and_user( user_name, user_root ):
    """ create a database """
    try:
        cmd = f"CREATE DATABASE IF NOT EXISTS {user_root}_{user_name};"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)
        cmd = f"CREATE USER IF NOT EXISTS '{user_name}'@'localhost' identified by '{db_password(user_name)}';"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)
        cmd = f"CREATE USER IF NOT EXISTS '{user_name}'@'%' identified by '{db_password(user_name)}';"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)
        cmd = f"grant all privileges on {user_root}_{user_name}.* to '{user_name}'@'localhost'; flush privileges;"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)
        cmd = f"grant all privileges on {user_root}_{user_name}.* to '{user_name}'@'%'; flush privileges;"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)
    except Exception as e:
        # If any command fails, this will print the error message with the command that failed
        logger.error(f"Error occurred: {e}")

def add_user_to_group( username, groupname ):
    """ Add user to team group"""
    # sudo usermod -aG groupname username
    try:
        cmd = f"usermod -aG {groupname} {username}"
        run_command( cmd, use_sudo=True )
    except Exception as e:
        logger.error(f"Error adding user to group: {e}")

def remove_user_from_group( username, groupname ):
    """ Add user to team group"""
    # sudo usermod -aG groupname username
    try:
        cmd = f"deluser {username} {groupname}"
        run_command( cmd, use_sudo=True )
    except Exception as e:
        logger.error(f"Error removeing user from group: {e}")


def grant_database_to_user(db_name, additional_user_name ):
    """ Grant privileges to an additional user on the specified database """
    try:
        # Grant privileges to the user for localhost
        cmd = f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{additional_user_name}'@'localhost'; flush privileges;"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)

        # Grant privileges to the user for any host ('%')
        cmd = f"GRANT ALL PRIVILEGES ON {db_name}.* TO '{additional_user_name}'@'%'; flush privileges;"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)

    except Exception as e:
        # Handle any errors during the command execution
        logger.error(f"Error occurred: {e}")

def revoke_database_from_user(db_name, additional_user_name):
    """ Revoke privileges from an additional user on the specified database """
    try:
        # Revoke privileges from the user for localhost
        cmd = f"REVOKE ALL PRIVILEGES ON {db_name}.* FROM '{additional_user_name}'@'localhost'; flush privileges;"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)

        # Revoke privileges from the user for any host ('%')
        cmd = f"REVOKE ALL PRIVILEGES ON {db_name}.* FROM '{additional_user_name}'@'%'; flush privileges;"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)

    except Exception as e:
        # Handle any errors during the command execution
        logger.error(f"Error occurred: {e}")


def drop_database_and_user(user_name, user_root):
    """ drop a database and corresponding users """
    try:
        cmd = f"DROP DATABASE IF EXISTS {user_root}_{user_name};"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)
        cmd = f"DROP USER IF EXISTS '{user_name}'@'localhost'; flush privileges;"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)
        cmd = f"DROP USER IF EXISTS '{user_name}'@'%'; flush privileges"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)
 
    except Exception as e:
        # If any command fails, this will print the error message with the command that failed
        logger.error(f"Error occurred: {e}")

def populate_hr_database( user_name, user_root, hr_data_file ):
    """ populate HR database for user """
    # mysql -u 23FA_abdulmelikna -D 23FA_hr_abdulmelikna --password=Shout4_abdulmelikna_GOME < HR.sql
    try:
        cmd = f"DROP DATABASE IF EXISTS {user_root}_{user_name}"
        run_command(f'mysql -e "{cmd}"', use_sudo=True)
        create_database_and_user( user_name, user_root );
        cmd = f"mysql -u {user_name} -D {user_root}_{user_name} --password={db_password(user_name)} < {hr_data_file}"
        run_command( cmd )
    except Exception as e:
        # If any command fails, this will print the error message with the command that failed
        logger.error(f"Error occurred (populate_hr_database): {e}")

def create_team_database_and_user( group_name ):
    """ set up team database """
    create_database_and_user( group_name, DB_TEAM_ROOT )

def create_user_database_and_user( user_name ):
    """ set up individual user database """
    create_database_and_user( user_name, DB_USER_ROOT )

def create_hr_database_and_user( user_name ):
    """ set up individual user database """
    create_database_and_user( user_name, DB_HR_ROOT )

def drop_team_database_and_user( group_name ):
    """ set up team database """
    drop_database_and_user( group_name, DB_TEAM_ROOT )

def drop_user_database_and_user( user_name ):
    """ set up individual user database """
    drop_database_and_user( user_name, DB_USER_ROOT )

def drop_hr_database_and_user( user_name ):
    """ set up individual user database """
    drop_database_and_user( user_name, DB_HR_ROOT )

def get_dbusers_on_server():
    """ return list of mysql users and host """
    result = run_command("mysql -e 'select user,host from mysql.user'",use_sudo=True)
    return [item for item in result.stdout.split("\n") if item.startswith(f"{TERM_CODE}_") ]

def get_databases_on_server():
    """ return list of mysql users and host """
    result = run_command("mysql -e 'show databases'",use_sudo=True)
    return [item for item in result.stdout.split("\n") if item.startswith(f"{TERM_CODE}_") ]

def list_dbusers_on_server():
    """ print list of db users on server """
    for i,user in enumerate( get_dbusers_on_server()):
        print( user )

def list_databases_on_server():
    """ print list of databases on server """
    for i,db in enumerate( get_databases_on_server()):
        print( db )
    
def delete_database_on_server( database_name ):
    """ delete database on server """
    result = run_command(f'mysql -e "drop database {database_name};"', use_sudo=True)

def get_server_counts():
    """ return list of server counts """
    status = dict( users=len(get_users_with_uid_above()), groups=len(get_groups_with_gid_above()),dbusers=len(get_dbusers_on_server()), databases=len(get_databases_on_server()))
    return status

def list_server_counts():
    """ return list of server counts """
    status = get_server_counts()
    for key in status.keys():
        print(f"{key} : {status[key]}")

def create_user_bundle( user_name, hr_data_file=None ):
    """ do all things necessary to create a user """
    logger.debug(f"create_user_account: ")
    clean_name = clean_user_name( user_name )
    create_user_account( clean_name )
    logger.debug(f"create_user_database_and_user")
    create_user_database_and_user( clean_name )
    logger.debug(f"create_hr_database_and_user")
    create_hr_database_and_user( clean_name )
    if not hr_data_file is None:
        populate_hr_database( clean_name, DB_HR_ROOT, hr_data_file )
    logger.success(f"User bundle {clean_name} created.")

def populate_hr_db_raw( user_name, hr_data_file=None ):
    clean_name = clean_user_name( user_name )
    if not hr_data_file is None:
        populate_hr_database( clean_name, DB_HR_ROOT, hr_data_file )
        logger.success(f"Populated {DB_HR_ROOT}_{clean_name} with {hr_data_file}")

def delete_user_bundle( user_name ):
    """ do all things necessary to delete a user """
    click.echo(f"Goodbye {user_name}! I will delete you now.")
    clean_name = clean_user_name( user_name )
    drop_hr_database_and_user( clean_name )
    drop_user_database_and_user( clean_name )
    delete_user_account( clean_name )

def create_team_bundle( team_name ):
    """ do all things necessary to create a user """
    logger.debug(f"create_user_account: ")
    clean_name = clean_user_name( team_name )
    create_user_account( clean_name )
    logger.debug(f"create_team_database_and_user")
    create_team_database_and_user( clean_name )
    logger.success(f"Team bundle {clean_name} created.")

def delete_team_bundle( team_name ):
    """ do all things necessary to delete a team """
    click.echo(f"Goodbye {team_name}! I will delete you now.")
    clean_name = clean_user_name( team_name )
    drop_team_database_and_user( clean_name )
    delete_user_account( clean_name )

def create_connection( team_name, user_name ):
    clean_team = clean_user_name( team_name )
    clean_user = clean_user_name( user_name )
    add_user_to_group( clean_user, clean_team )
    grant_database_to_user( clean_team, clean_user )
    logger.success(f"User {clean_user} added to team {clean_team}.")

def delete_connection( team_name, user_name ):
    clean_team = clean_user_name( team_name )
    clean_user = clean_user_name( user_name )
    revoke_database_from_user( clean_team, clean_user )
    remove_user_from_group( clean_user, clean_team )
    logger.success(f"User {clean_user} removed from team {clean_team}.")

def delete_users_on_server():
    """ delete users with uid above threshhold """
    for i,user in enumerate(get_users_with_uid_above()):
        delete_user_bundle( user )

def delete_teams_on_server():
    """ delete teams with gid above threshhold """
    for i,group in enumerate(get_groups_with_gid_above()):
        delete_team_bundle( group )

def delete_dbusers_on_server():
    """ delete database users on server """
    for i,user in enumerate( get_dbusers_on_server()):
        delete_user_bundle( user )

def delete_databases_on_server():
    """ delete databases on server """
    for i,database in enumerate( get_databases_on_server()):
        delete_database_on_server( database )
        


"""

## Commands to drop user databases
drop database 23FA_users_abdulmelikna;
drop database 23FA_hr_abdulmelikna;
drop user '23FA_abdulmelikna'@'localhost';
drop user '23FA_abdulmelikna'@'%';
FLUSH PRIVILEGES;

## Commands to populate user databases
mysql -u 23FA_abdulmelikna -D 23FA_hr_abdulmelikna --password=Shout4_abdulmelikna_GOME < HR.sql

"""
