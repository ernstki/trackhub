import os
import sys
import click

@click.group()
def cli():
    pass

@cli.command()
def gen():
    click.echo("Generating... (not really)")

if __name__ == '__main__':
    cli()
