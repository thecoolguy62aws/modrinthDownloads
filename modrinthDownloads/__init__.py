from importlib.metadata import version

try:
    __version__ = version('modrinthDownloads')
except ModuleNotFoundError:
    __version__ = "developement"
