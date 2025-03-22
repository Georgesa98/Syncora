from click import command, argument, echo
from parsers.config import Config


@command(name="validate")
@argument("file_path")
def validate(file_path: str):
    x = Config(file_path)
    echo("file is valid")
