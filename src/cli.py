from click import group, prompt, echo, argument
from parsers.config import Config
from utils.file_helpers import ensure_exists
from database.connection import ConnectionDb


@group()
def cli():
    ConnectionDb()


@cli.command()
def init():
    if not ensure_exists("./syncora.json"):
        name = prompt("please enter a name for the project", type=str)
        version = prompt("enter the version of the project", type=float)
        Config().initialize(name, version)
    else:
        echo("file already been initialized")


@cli.command()
@argument("file_path")
def validate(file_path: str):
    x = Config(file_path)
    echo("file is valid")


if __name__ == "__main__":
    cli()
