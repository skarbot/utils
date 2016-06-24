"""
Create Command Line
"""
import logging

import click

from utils import timelogs


@click.command()
@click.option('--username', prompt='Please enter your JIRA username',
              help='Enter the JIRA')
@click.option('--password', prompt=True, hide_input=True,
              help='Enter JIRA password')
def update_jira(username, password):
    """
    CLI option for JIRA time sync

    *username* for JIRA authentication
    *password* to connect to JIRA

    """
    logging.basicConfig()
    timelogs.update_jira(username, password)


@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    if debug:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(level=level)


if __name__ == '__main__':
    cli.add_command(update_jira)
    cli()