import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import Config
from pluggy import PluginManager


@pytest.hookimpl
def pytest_addoption(parser: Parser):
    group = parser.getgroup("bugtracker")
    group.addoption(
        "--bugtracker",
        action="store_true",
        dest="bugtracker",
    )
    group.addoption(
        "--bugtracker-config-file",
        action="store",
        dest="bugtracker_config_file_path",
        default="pytest-bugtracker.ini",
    )


@pytest.hookimpl
def pytest_addhooks(pluginmanager: PluginManager):
    from . import hooks

    pluginmanager.add_hookspecs(hooks)


@pytest.hookimpl(trylast=True)
def pytest_configure(config: Config):
    if not config.option.bugtracker:
        return

    from .worker import Worker

    worker = Worker(config)
    config.pluginmanager.register(worker, "bugtracker_worker")
