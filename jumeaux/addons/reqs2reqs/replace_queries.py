# -*- coding:utf-8 -*-

"""For example of config

reqs2reqs:
  - name: addons.reqs2reqs.replace_queries
    config:
      items:
        - conditions:
            - path:
                items:
                  - regexp: /traffic
          queries:
            id: "dummy"
            time: "hogehoge"
"""

import logging
import copy
import re
from datetime import datetime, timedelta

from owlmixin import OwlMixin
from owlmixin.owlcollections import TList, TDict

from jumeaux.addons.conditions import RequestCondition, AndOr
from jumeaux.addons.reqs2reqs import Reqs2ReqsExecutor
from jumeaux.models import Request, Reqs2ReqsAddOnPayload

logger = logging.getLogger(__name__)


class Replacer(OwlMixin):
    conditions: TList[RequestCondition]
    and_or: AndOr = "and"
    negative: bool = False
    queries: TDict[TList[str]]

    def fulfill(self, req: Request) -> bool:
        return self.negative ^ (self.and_or.check(self.conditions.map(lambda x: x.fulfill(req))))


class Config(OwlMixin):
    items: TList[Replacer]


def special_parse(value: str):
    m = re.search(r'^\$DATETIME\((.+)\)\((.+)\)$', value)
    return (datetime.now() + timedelta(seconds=int(m[2]))).strftime(m[1]) \
        if m else value


def replace_queries(req: Request, queries: TDict[TList[str]]) -> Request:
    copied = copy.deepcopy(req.qs)
    copied.update(queries.map_values(lambda vs: vs.map(special_parse)))
    req.qs = copied
    return req


def apply_replacers(req: Request, replacers: TList[Replacer]) -> Request:
    return replacers.reduce(lambda t, x: replace_queries(t, x.queries) if x.fulfill(t) else t, req)


class Executor(Reqs2ReqsExecutor):
    def __init__(self, config: dict):
        self.config: Config = Config.from_dict(config or {})

    def exec(self, payload: Reqs2ReqsAddOnPayload) -> Reqs2ReqsAddOnPayload:
        return Reqs2ReqsAddOnPayload.from_dict({
            'requests': payload.requests.map(lambda req: apply_replacers(req, self.config.items))
        })
