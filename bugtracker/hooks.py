import pytest
from _pytest.config import Config
from _pytest.reports import TestReport

from bugtracker import YandexTrackerConfiguration


@pytest.hookspec
def pytest_yc_bugtracker_initial_config(config: Config) -> YandexTrackerConfiguration:
    pass


@pytest.hookspec
def pytest_yc_bugtracker_initial_task_title(config: Config) -> str:
    pass
