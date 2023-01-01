from __future__ import annotations

import configparser
import os
import typing as t
from dataclasses import dataclass
from pathlib import Path

from _pytest.reports import TestReport
from yandex_tracker_client import TrackerClient as _TrackerClient


def create_description(report: TestReport, /) -> str:
    text = """
    \n-----------------------------------------------------------
    \n**Duration:** {duration}s
    \n**Test path:** {nodeid}
    \n**Allure report:** null
    \n**Assertion:**
        <{{read more
        %%(python) {assertion_text} %%
        }}>
    \n-----------------------------------------------------------
    """
    return text.format(
        duration=report.duration,
        nodeid=report.nodeid,
        assertion_text=report.longreprtext,
    )


@dataclass
class YandexTrackerTeam:
    tests_path: Path
    queue: str


class YandexTrackerConfiguration:
    def __init__(self):
        self._queue = None
        self._teams = []

    @property
    def queue(self) -> t.Optional[str]:
        return self._queue

    def init_config(self, settings_file_path: str, /) -> YandexTrackerConfiguration:
        general_section_name = f"Tracker:Yandex"

        parser = configparser.ConfigParser()
        parser.read(os.path.join(os.getcwd(), settings_file_path))

        self._queue = parser[general_section_name]['queue']

        section_teams = [
            section_name
            for section_name in parser
            if section_name.startswith(f'{general_section_name}:') and len(section_name) > 0
        ]

        for section_team in section_teams:
            tests_path = parser[section_team].get('tests_path')
            queue = parser[section_team].get('queue') or self.queue
            if tests_path is None or len(tests_path) == 0:
                continue
            # if not os.path.exists(tests_path):
            #     continue
            self._teams.append(
                YandexTrackerTeam(
                    tests_path=tests_path,
                    queue=queue,
                )
            )

        self._tracker_client = _TrackerClient(
            token=parser[general_section_name]['oauth-token'],
            org_id=parser[general_section_name]['x-org-id'],
        )
        return self

    def create_issue(self, title: str, report: TestReport, /) -> None:
        self._tracker_client.issues.create(
            queue=self.queue,
            summary=title,
            description=create_description(report),
            type={'name': 'Task'},  # Change type to dynamic (in .ini file block task-type)
        )
