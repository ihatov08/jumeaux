#!/usr/bin/env python
# -*- coding:utf-8 -*-

import datetime
import os
import pytest

from owlmixin.util import load_yaml

from jumeaux.addons.dump.html import Executor
from jumeaux.models import Response, DumpAddOnPayload

NORMAL_BODY = """<!DOCTYPE html>
<html>
<head>
  <title>タイトル</title>
  <meta name="format-detection" content="telephone=no">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
  <script type="text/javascript" charset="utf-8">
    var hoge = 1 > 2;
  </script>
</head>
<body>
  <div id="main">
    <span>Main contents</span>
  </div>
</body>
</html>
""".replace(os.linesep, '').replace('  ', '')

CORRUPTION_BODY_BYTES: bytes = \
    '<!DOCTYPE html><html><head><title>タイトル</title></head>'.encode('utf8') + \
    '<body><div>コンテンツ</div></body></html>'.encode('euc-jp')

NORMAL_CASE = ("Normal",
               """
               force: False 
               """,
               Response.from_dict({
                   "body": NORMAL_BODY.encode('euc-jp'),
                   "encoding": 'euc-jp',
                   "headers": {
                       "content-type": "text/html; charset=euc-jp"
                   },
                   "url": "http://test",
                   "status_code": 200,
                   "elapsed": datetime.timedelta(seconds=1)
               }),
               NORMAL_BODY.encode('euc-jp'),
               'euc-jp',
               """<html>
 <head>
  <title>
   タイトル
  </title>
  <meta content="telephone=no" name="format-detection"/>
  <meta content="text/html; charset=utf-8" http-equiv="Content-Type"/>
  <script charset="utf-8" type="text/javascript">
   var hoge = 1 > 2;
  </script>
 </head>
 <body>
  <div id="main">
   <span>
    Main contents
   </span>
  </div>
 </body>
</html>""".encode('euc-jp'),
               'euc-jp'
               )

CORRUPTION_CASE = ("Corruption",
                   """
                   force: False 
                   """,
                   Response.from_dict({
                       "body": CORRUPTION_BODY_BYTES,
                       "encoding": 'euc-jp',
                       "headers": {
                           "content-type": "text/html; charset=euc-jp"
                       },
                       "url": "http://test",
                       "status_code": 200,
                       "elapsed": datetime.timedelta(seconds=1)
                   }),
                   CORRUPTION_BODY_BYTES,
                   'euc-jp',
                   """<html>
 <head>
  <title>
   ��帥�ゃ�����
  </title>
 </head>
 <body>
  <div>
   コンテンツ
  </div>
 </body>
</html>""".encode('euc-jp', errors='replace'),
                   'euc-jp'
                   )


class TestExec:
    @pytest.mark.parametrize(
        'title, config_yml, response, body, encoding, expected_body, expected_encoding', [
            NORMAL_CASE,
            CORRUPTION_CASE,
        ]
    )
    def test(self, title, config_yml, response, body, encoding, expected_body, expected_encoding):
        payload: DumpAddOnPayload = DumpAddOnPayload.from_dict({
            'response': response,
            'body': body,
            'encoding': encoding,
        })

        actual: DumpAddOnPayload = Executor(load_yaml(config_yml)).exec(payload)

        assert expected_body == actual.body
        assert expected_encoding == actual.encoding.get()
