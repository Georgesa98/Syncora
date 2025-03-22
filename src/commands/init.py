from click import prompt, echo, command
from utils.file_helpers import ensure_exists
from parsers.config import Config


@command(name="init")
def init():
    if not ensure_exists("./syncora.json"):
        name = prompt("please enter a name for the project", type=str)
        version = prompt("enter the version of the project", type=float)
        Config().initialize(name, version)
    else:
        echo("file already been initialized")
