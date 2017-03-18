# -*- coding: utf-8 -*-

from typing import Optional, Any, Dict, List
from owlmixin import OwlMixin
from owlmixin.owlcollections import TList, TDict
from owlmixin.owlenum import OwlEnum


class Status(OwlEnum):
    SAME = "same"
    DIFFERENT = "different"
    FAILURE = "failure"


class AccessPoint(OwlMixin):
    def __init__(self, name, host, proxy=None):
        self.name: str = name
        self.host: str = host
        self.proxy: Optional[str] = proxy


class OutputSummary(OwlMixin):
    def __init__(self, response_dir='response', encoding='utf8', logger=None):
        self.response_dir: str = response_dir
        self.encoding: str = encoding
        self.logger: Optional[Any] = logger


class Addon(OwlMixin):
    def __init__(self, name, command: str = 'exec', config: dict = None):
        self.name: str = name
        self.command: str = command
        self.config: dict = config


class Addons(OwlMixin):
    def __init__(self, log, dump=None, after=None, request=None):
        self.log: Addon = Addon.from_dict(log)
        self.dump: TList[Addon] = Addon.from_optional_dicts(dump) or TList()
        self.after: TList[Addon] = Addon.from_optional_dicts(after) or TList()
        self.request: TList[Addon] = Addon.from_optional_dicts(request) or TList()


class Config(OwlMixin):
    def __init__(self, one, other, output, title=None, input_files=None, addons=None):
        self.one: AccessPoint = AccessPoint.from_dict(one)
        self.other: AccessPoint = AccessPoint.from_dict(other)
        self.output: OutputSummary = OutputSummary.from_dict(output)
        self.title: Optional[str] = title
        self.input_files: Optional[TList[str]] = TList(input_files) if input_files else None
        self.addons: Optional[Addons] = Addons.from_optional_dict(addons)


# --------


class Args(OwlMixin):
    def __init__(self, files, title: str, config: str, threads):
        self.files: TList[str] = TList(files)
        self.title: str = title
        self.config: Config = Config.from_yamlf(config)
        self.threads: int = int(threads)


class Request(OwlMixin):
    def __init__(self, path, qs=None, headers=None, name=None):
        self.path: str = path
        self.qs: TDict[TList[str]] = TDict(qs) if qs else {}
        self.headers: TDict[str] = TDict(headers) if headers else {}
        self.name: Optional[str] = name


class Proxy(OwlMixin):
    def __init__(self, http: str = None, https: str = None):
        self.http: Optional[str] = http
        self.https: Optional[str] = https

    @classmethod
    def from_host(cls, host: Optional[str]) -> 'Proxy':
        return Proxy.from_dict({
            'http': f"http://{host}",
            'https': f"https://{host}",
        }) if host else None


# --------

class ChallengeArg(OwlMixin):
    def __init__(self, seq: int, number_of_request: int, key: str, name: str,
                 session: object, host_one: str, host_other: str, path: str, res_dir: str,
                 qs: TDict[TList[str]], headers: TDict[str], proxy_one: Proxy, proxy_other: Proxy,
                 addons: Addons):
        self.seq: int = seq
        self.number_of_request: int = number_of_request
        self.key: str = key
        self.name: str = name
        self.session: object = session
        self.host_one: str = host_one
        self.host_other: str = host_other
        self.path: str = path
        self.res_dir: str = res_dir
        self.qs: TDict[TList[str]] = qs
        self.headers: TDict[str] = headers
        self.proxy_one: Optional[Proxy] = proxy_one
        self.proxy_other: Optional[Proxy] = proxy_other
        self.addons: Optional[Addons] = addons


# --------

class Report(OwlMixin):
    def __init__(self, key: str, title: str, summary: dict, trials: list):
        self.key: str = key
        self.title: str = title
        self.summary: Summary = Summary.from_dict(summary)
        self.trials: TList[Trial] = Trial.from_dicts(trials)


class Summary(OwlMixin):
    def __init__(self, one: dict, other: dict, status: TDict[str], paths: TDict[str], time: dict):
        self.one: AccessPoint = AccessPoint.from_dict(one)
        self.other: AccessPoint = AccessPoint.from_dict(other)
        self.status: StatusCounts = StatusCounts.from_dict(status)
        self.paths: TDict[str] = paths
        self.time: Time = Time.from_dict(time)


class StatusCounts(OwlMixin):
    def __init__(self, same: int = 0, different: int = 0, failure: int = 0):
        self.same: int = same
        self.different: int = different
        self.failure: int = failure


class Time(OwlMixin):
    def __init__(self, start: str, end: str, elapsed_sec: int):
        self.start: str = start  # yyyy/MM/dd hh:mm:ss
        self.end: str = end  # yyyy/MM/dd hh:mm:ss
        self.elapsed_sec: int = elapsed_sec


class Trial(OwlMixin):
    def __init__(self, name: str, headers: dict, queries: dict, one: dict, other: dict,
                 path: str, request_time: str, status: str):
        self.name: str = name
        self.headers: Dict[str, str] = headers
        self.queries: Dict[str, List[str]] = queries
        self.one: ResponseSummary = ResponseSummary.from_dict(one)
        self.other: ResponseSummary = ResponseSummary.from_dict(other)
        self.path: str = path
        self.request_time: str = request_time
        self.status: Status = Status(status)


class ResponseSummary(OwlMixin):
    def __init__(self, url: str, status_code: int = None, byte: int = None, response_sec: int = None,
                 content_type: str = None, file: Optional[str] = None):
        self.url: str = url
        self.status_code: Optional[int] = status_code
        self.byte: Optional[int] = byte
        self.response_sec: Optional[int] = response_sec
        self.content_type: Optional[str] = content_type
        self.file: Optional[str] = file


# ---

class ResponseAddOnPayload(OwlMixin):
    def __init__(self, response, body: bytes, encoding: str):
        self.response = response  # requests style
        self.body = body
        self.encoding = encoding
