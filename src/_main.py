import click
import subprocess

from src.utils import create_user_bundle, delete_user_bundle, create_team_bundle, delete_team_bundle
from src.file_utils import list_groups_in_csv_file, list_users_in_csv_file, list_groups_and_users_in_csv_file, \
      create_connections_from_csv_file, populate_hr_databases_from_csv_file
from src.logging import DEFAULT_LOG_LEVEL, set_logger

DEFAULT_GROUP_CSV_FILE = "semester-project-groups.csv"
DEFAULT_HR_DDL_FILE = "hr-ddl.sql"

@click.group()
@click.option("--log-level",help="log level (DEBUG, etc.)",default=DEFAULT_LOG_LEVEL)
def cli(log_level):
    """Main entry point for the CLI application.

    Manage user and team project accounts on a linux box using Canvas provided group file.
    
    
    """
    set_logger( log_level=log_level)
    pass

@cli.command()
@click.argument("username")
def create_user(username):
    """ create a user bundle """
    create_user_bundle( username )

@cli.command()
@click.argument("username")
def delete_user( username ):
    """ delete a user bundle """
    delete_user_bundle( username )

@cli.command()
@click.argument("teamname")
def create_team(teamname):
    """ create a team bundle """
    create_team_bundle( teamname )

@cli.command()
@click.argument("teamname")
def delete_team( teamname ):
    """ delete a team bundle """
    delete_team_bundle( teamname )

@cli.command()
@click.option("--team-file",help="csv groups downloaded from Canvas",default=DEFAULT_GROUP_CSV_FILE)
def list_teams_in_file( team_file ):
    """ List teams in group file """
    list_groups_in_csv_file( team_file )

@cli.command()
@click.option("--team-file",help="csv groups downloaded from Canvas",default=DEFAULT_GROUP_CSV_FILE)
def list_users_in_file( team_file ):
    """ List users in group file """
    list_users_in_csv_file( team_file )

@cli.command()
@click.option("--team-file",help="csv groups downloaded from Canvas",default=DEFAULT_GROUP_CSV_FILE)
def list_teams_and_users_in_file( team_file ):
    """ List users in group file """
    list_groups_and_users_in_csv_file( team_file )

@cli.group()
def build():
    """Subcommand group for building resources."""
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
def connections( team_file ):
    """ Connects users to teams, creating as necessary """
    create_connections_from_csv_file( team_file )

@build.command()
@click.option("--team-file",help="csv groups downloaded from Canvas",default=DEFAULT_GROUP_CSV_FILE)
@click.option("--hr-ddl-file",help="hr DDL file",default=DEFAULT_HR_DDL_FILE)
def populate_hr_database( team_file, hr_ddl_file ):
    """ Connects users to teams, creating as necessary """
    populate_hr_databases_from_csv_file( team_file, hr_ddl_file )


if __name__ == '__main__':
    cli()
