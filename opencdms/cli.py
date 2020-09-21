"""Console script for opencdms."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for opencdms."""
    # See click documentation at https://click.palletsprojects.com/
    click.echo("Replace this message by putting your code into "
               "opencdms.cli.main")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
