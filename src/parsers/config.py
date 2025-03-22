from datetime import datetime
from utils.file_helpers import read_json_file, write_json_file, ensure_exists
from click import echo


class Metadata:
    def __init__(self, name: str = "", version: float = 0.0):
        self.name = name
        self.version = version
        self.created_at = datetime.now().isoformat()
        self.updated_at = datetime.now().isoformat()

    def to_dict(self):
        return self.__dict__


class Environment:
    def __init__(
        self,
        target_os: str = "",
        architecture: str = "",
        dependencies: str = [],
        runtime: str = "",
    ):
        self.target_os = target_os
        self.architecture = architecture
        self.dependencies = dependencies
        self.runtime = runtime

    def to_dict(self):
        return self.__dict__


class Project:
    def __init__(
        self,
        name: str = "",
        path: str = "",
        env: Environment = None,
        commands: str = [],
        ports: int = [],
    ):
        self.name = name
        self.path = path
        self.env = env
        self.commands = commands
        self.ports = ports

    def to_dict(self):
        return {
            "name": self.name,
            "path": self.path,
            "environment": self.env.to_dict(),
            "commands": self.commands,
            "ports": self.ports,
        }


class SyncSettings:
    def __init__(self, sync_mode: str = "manual", ignore_files=None):
        self.sync_mode = sync_mode
        self.ignore_files = ignore_files

    def to_dict(self):
        return self.__dict__


class Workspace:
    def __init__(
        self,
        metadata: Metadata = None,
        projects: Project = None,
        sync_settings: SyncSettings = None,
    ):
        self.metadata = metadata or Metadata()
        self.projects = projects or {}
        self.sync_settings = sync_settings or SyncSettings()

    def to_dict(self):
        return {
            "metadata": self.metadata.to_dict(),
            "projects": {
                name: project.to_dict() for name, project in self.projects.items()
            },
            "sync_settings": self.sync_settings.to_dict(),
        }


class Config:
    def __init__(self, file_path="./syncora.json"):
        self.file_path = file_path
        self.workspace = Workspace()
        if ensure_exists(self.file_path):
            data = read_json_file(self.file_path)
            self.workspace = self.parse_workspace(data)
        else:
            echo(
                "you need to initialize a file first if the file already initialized add the path in the argument"
            )

    def initialize(self, name, version):
        self.workspace.metadata.name = name
        self.workspace.metadata.version = version
        write_json_file(self.file_path, self.workspace.to_dict())

    def parse_workspace(self, data: dict):
        metadata = Metadata(
            data.get("metadata").get("name", ""),
            data.get("metadata").get("version", 0.0),
        )
        projects: dict = data.get("projects", {})
        for project_name, project_data in projects.items():
            env = Environment(
                project_data.get("target_os", []),
                project_data.get("architecture", ""),
                project_data.get("dependencies", []),
                project_data.get("runtime", ""),
            )
            projects[project_name] = Project(
                project_name,
                project_data.get("path", ""),
                env,
                project_data.get("commands", []),
                project_data.get("ports", []),
            )
        sync_settings = SyncSettings(
            data.get("sync_settings", {}).get("sync_mode", "manual"),
            data.get("sync_settings", {}).get("ignore_files", []),
        )
        return Workspace(metadata, projects, sync_settings)
