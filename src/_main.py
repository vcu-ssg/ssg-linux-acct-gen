import click
import subprocess

from src.utils import create_user_bundle, delete_user_bundle, create_team_bundle, delete_team_bundle
from src.file_utils import list_groups_in_csv_file, list_users_in_csv_file, list_groups_and_users_in_csv_file, \
      create_connections_from_csv_file, populate_hr_databases_from_csv_file
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
    """ Subcommand group to work with solo teams or users """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())  # Show help if no subcommand is provided

@solo.command()
@click.option("--sql", type=click.Path(exists=True, dir_okay=False, readable=True), \
              help="SQL file to load into the database")
@click.option("--database", help="Database name to receive the SQL")
@click.pass_context
def load_sql(ctx, sql, database):
    """ Load a SQL file into a database """
    if not sql or not database:
        click.echo(ctx.get_help())  # Show help message if required params are missing
        ctx.exit(1)  # Exit with error
    # Add logic to load SQL file into the database
    click.echo(f"Loading SQL from {sql} into database {database}")

@solo.command()
@click.argument("username")
def create_user(username):
    """ create DB user bundle """
    create_user_bundle( username )

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

##
## BUILD commands
##

@cli.group()
def build():
    """ Subcommand group for building resources on server. """
    pass

@build.command()
def teams():
    """ Creates team resources"""
    click.echo(f"Teams created successfully.")

@build.command()
def users():
    """ Creates user resources"""
    click.echo(f"Users created successfully.")

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
def users():
    """ Lists linux users on server """
    click.echo(f"(Not operational).")

@server.command()
def groups():
    """ Lists linux groups on server """
    click.echo(f"(Not operational).")

@server.command()
def db_users():
    """ Lists database users on server """
    click.echo(f"(Not operational).")


@server.command()
def databases():
    """ Lists databases on server """
    click.echo(f"(Not operational).")

if __name__ == '__main__':
    cli()
