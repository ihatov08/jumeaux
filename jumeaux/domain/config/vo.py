# -*- coding: utf-8 -*-
from owlmixin import OwlMixin, TOption, TDict, TList, OwlEnum

from jumeaux.addons import Addons


class NotifierType(OwlEnum):
    SLACK = "slack"


class QueryCustomization(OwlMixin):
    overwrite: TOption[TDict[TList[str]]]
    remove: TOption[TList[str]]


class PathReplace(OwlMixin):
    before: str
    after: str


class AccessPoint(OwlMixin):
    name: str
    host: str
    path: TOption[PathReplace]
    query: TOption[QueryCustomization]
    proxy: TOption[str]
    default_response_encoding: TOption[str]
    headers: TDict[str] = {}


class OutputSummary(OwlMixin):
    response_dir: str
    encoding: str = "utf8"
    logger: TOption[any]


class Concurrency(OwlMixin):
    threads: int
    processes: int


class Notifier(OwlMixin):
    type: NotifierType
    channel: str
    username: str = "jumeaux"
    icon_emoji: TOption[str]
    icon_url: TOption[str]

    @property
    def logging_message(self) -> str:
        return f"Send to {self.channel} by slack"


class Config(OwlMixin):
    one: AccessPoint
    other: AccessPoint
    output: OutputSummary
    threads: int = 1
    processes: TOption[int]
    max_retries: int = 3
    title: TOption[str]
    description: TOption[str]
    tags: TOption[TList[str]]
    # TODO: remove
    input_files: TOption[TList[str]]
    notifiers: TOption[TDict[Notifier]]
    addons: Addons
