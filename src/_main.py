import click
import subprocess

from src.utils import create_team_and_directory, create_user_account


@click.group()
def cli():
    """Main entry point for the CLI application.

    Manage user and team project accounts on a linux box using Canvas provided group file.
    
    
    """
    pass

@cli.command()
def greet():
    """Simple command that greets the user."""
    click.echo("Hello! Welcome to the CLI application.")

@cli.group()
def manage():
    """Subcommand group for managing resources."""
    pass

@manage.command()
@click.argument('name')
def create(name):
    """Creates a resource with the given NAME."""
    click.echo(f"Resource '{name}' created successfully.")

@manage.command()
@click.argument('name')
def delete(name):
    """Deletes a resource with the given NAME."""
    click.echo(f"Resource '{name}' deleted successfully.")

if __name__ == '__main__':
    cli()
