import click
import subprocess

from src.utils import create_user_bundle, delete_user_bundle, create_team_bundle, delete_team_bundle, \
    list_groups_on_server, list_users_on_server, list_dbusers_on_server, list_databases_on_server, list_server_counts, \
    delete_users_on_server, delete_teams_on_server, delete_databases_on_server, delete_dbusers_on_server, populate_database
from src.file_utils import list_groups_in_csv_file, list_users_in_csv_file, list_groups_and_users_in_csv_file, \
      create_connections_from_csv_file, populate_hr_databases_from_csv_file, list_counts_in_file, \
      create_users_from_csv_file, create_groups_from_csv_file 
from src.logging import DEFAULT_LOG_LEVEL, set_logger

DEFAULT_GROUP_CSV_FILE = "semester-project-groups.csv"
DEFAULT_HR_DDL_FILE = "hr-ddl.sql"

##
## Main command line entry point
###

@click.group()
@click.option("--log-level",help="log level (DEBUG, etc.)",default=DEFAULT_LOG_LEVEL)
def cli(log_level):
    """Main entry point for the CLI application.

    Manage user and team project accounts on a linux box using Canvas provided group file.
    
    """
    set_logger( log_level=log_level)
    pass

##
## SOLO commands
##

@cli.group(invoke_without_command=True)
@click.pass_context
def solo(ctx):
    """ Subcommand group to work with solo teams or users

    Teams and users only differ in their database name, leveraging the roll-up feature of
    mysql database naming convention.

    Adds linux user account, group, and password.  Adds user and HR databases, and grants access to user.
    Teams don't get HR database, just team database.
    
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())  # Show help if no subcommand is provided

@solo.command()
@click.option("--sql", type=click.Path(exists=True, dir_okay=False, readable=True), \
              help="SQL file to load into the database")
@click.option("--database", help="Database name to receive the SQL", default=None)
@click.option("--username", help="Username loading the database", default=None)
@click.pass_context
def load_sql(ctx, sql, database, username):
    """ Load a SQL file into a database """
    if not sql or not database or not username:
        click.echo(ctx.get_help())  # Show help message if required params are missing
        ctx.exit(1)  # Exit with error
    # Add logic to load SQL file into the database
    populate_database( username, database, sql )
    

@solo.command()
@click.argument("username")
@click.option("--hr-ddl-file",help="hr DDL file",default=DEFAULT_HR_DDL_FILE)
def create_user(username,hr_ddl_file):
    """ create DB user bundle """
    create_user_bundle( username,hr_data_file=hr_ddl_file )

@solo.command()
@click.argument("username")
def delete_user( username ):
    """ delete DB user user bundle """
    delete_user_bundle( username )

@solo.command()
@click.argument("teamname")
def create_team(teamname):
    """ create a team bundle """
    create_team_bundle( teamname )

@solo.command()
@click.argument("teamname")
def delete_team( teamname ):
    """ delete a team bundle """
    delete_team_bundle( teamname )

##
## FILE commands
##

@cli.group()
def file():
    """ subcommand group for listing file resources """
    pass

@file.command()
@click.option("--team-file",help="csv groups downloaded from Canvas",default=DEFAULT_GROUP_CSV_FILE)
def teams( team_file ):
    """ List teams in group file """
    list_groups_in_csv_file( team_file )

@file.command()
@click.option("--team-file",help="csv groups downloaded from Canvas",default=DEFAULT_GROUP_CSV_FILE)
def users( team_file ):
    """ List users in group file """
    list_users_in_csv_file( team_file )

@file.command()
@click.option("--team-file",help="csv groups downloaded from Canvas",default=DEFAULT_GROUP_CSV_FILE)
def pairs( team_file ):
    """ List users in group file """
    list_groups_and_users_in_csv_file( team_file )

@file.command()
@click.option("--team-file",help="csv groups downloaded from Canvas",default=DEFAULT_GROUP_CSV_FILE)
def counts( team_file ):
    """ List counts of users, etc. group file """
    list_counts_in_file( team_file )

##
## BUILD commands
##

@cli.group()
def build():
    """ Subcommand group for building resources on server. """
    pass

@build.command()
@click.option("--team-file",help="csv groups downloaded from Canvas",default=DEFAULT_GROUP_CSV_FILE)
def teams( team_file ):
    """ Creates team resources"""
    create_groups_from_csv_file( team_file )

@build.command()
@click.option("--team-file",help="csv groups downloaded from Canvas",default=DEFAULT_GROUP_CSV_FILE)
def users( team_file ):
    """ Creates user resources"""
    create_users_from_csv_file( team_file )

@build.command()
@click.option("--team-file",help="csv groups downloaded from Canvas",default=DEFAULT_GROUP_CSV_FILE)
def pairs( team_file ):
    """ Connects users to teams, creating as necessary """
    create_connections_from_csv_file( team_file )

@build.command()
@click.option("--team-file",help="csv groups downloaded from Canvas",default=DEFAULT_GROUP_CSV_FILE)
@click.option("--hr-ddl-file",help="hr DDL file",default=DEFAULT_HR_DDL_FILE)
def populate_hr_database( team_file, hr_ddl_file ):
    """ Connects users to teams, creating as necessary """
    populate_hr_databases_from_csv_file( team_file, hr_ddl_file )

##
## SERVER commands
##

@cli.group()
def server():
    """
    Subcommand group for reviewing resources on the server.
    
    These commands are less opinionated.  They look at mysql, groups and passwd
    without making assumptions about how the accounts may have been created.

    Use the `file` commands to determine if server matches entries in file.
        
"""
    pass

@server.command()
@click.option('--delete', is_flag=True, help='Delete the specified item.', default=False)
@click.option('--term-code', help='Term code in name (e.g., 24FA, 23SP, etc.)', default="24FA")
def users( delete,term_code ):
    """ Lists linux users on server """
    if not delete:
        list_users_on_server( term_code=term_code )
    else:
        delete_users_on_server( term_code=term_code )

@server.command()
@click.option('--delete', is_flag=True, help='Delete the specified item.', default=False)
def groups( delete ):
    """ Lists linux groups on server """
    if not delete:
        list_groups_on_server()
    else:
        delete_teams_on_server()

@server.command()
@click.option('--delete', is_flag=True, help='Delete the specified item.', default=False)
@click.option('--term-code', help='Term code in name (e.g., 24FA, 23SP, etc.)', default="24FA")
def dbusers( delete,term_code ):
    """ Lists database users on server """
    if not delete:
        list_dbusers_on_server( term_code=term_code )
    else:
        delete_dbusers_on_server( term_code=term_code )


@server.command()
@click.option('--delete', is_flag=True, help='Delete the specified item.', default=False)
@click.option('--term-code', help='Term code in name (e.g., 24FA, 23SP, etc.)', default="24FA")
def databases( delete,term_code ):
    """ Lists databases on server """
    if not delete:
        list_databases_on_server( term_code=term_code )
    else:
        delete_databases_on_server( term_code=term_code )

@server.command()
def counts():
    """ show server statistics """
    list_server_counts()

if __name__ == '__main__':
    cli()
