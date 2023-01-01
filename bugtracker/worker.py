import uuid

import pytest
from _pytest.config import Config
from _pytest.reports import TestReport

from bugtracker.trackers import YandexTrackerConfiguration


class Worker:
    yandex_bugtracker: YandexTrackerConfiguration

    def __init__(self, config: Config, /):
        self.config = config

    @pytest.hookimpl(trylast=True)
    def pytest_yc_bugtracker_initial_config(self, config):
        ytracker_configuration = YandexTrackerConfiguration()
        ytracker_configuration.init_config(config.option.bugtracker_config_file_path)
        return ytracker_configuration

    @pytest.hookimpl(trylast=True)
    def pytest_yc_bugtracker_initial_task_title(self, config: Config):
        return f"[failed:{uuid.uuid4()}]"

    @pytest.hookimpl
    def pytest_runtestloop(self):
        self.yandex_bugtracker = self.config.hook.pytest_yc_bugtracker_initial_config(config=self.config)[0]
        self.task_title = self.config.hook.pytest_yc_bugtracker_initial_task_title(config=self.config)[0]

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        result: TestReport = outcome.get_result()
        if result.when == 'call' and result.failed:
            self.yandex_bugtracker.create_issue(self.task_title, result)
