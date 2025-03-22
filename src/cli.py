from click import group, prompt, echo, argument
from parsers.config import Config
from database.connection import ConnectionDb
from commands.init import init
from commands.validate import validate


@group()
def cli():
    ConnectionDb()


cli.add_command(validate)
cli.add_command(init)


if __name__ == "__main__":
    cli()
