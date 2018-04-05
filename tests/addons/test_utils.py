#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pytest
from jumeaux.addons import utils


class TestFilter:
    data = {
        "id": 1,
        "name": "一朗",
        "age": 44,
        "favorites": [
            {
                "rank": 2,
                "name": "Orange"
            },
            {
                "rank": 1,
                "name": "Apple"
            }
        ],
        "nicknames": [
            "Ichi",
            "イチロー"
        ]
    }

    @pytest.mark.parametrize(
        'expected, expression', [
            (True, 'id == 1'),
            (False, 'id != 1'),
            (False, 'id == 2'),
            (True, 'age > 40'),
            (False, 'age > 45'),
            (True, '40 < age < 45'),
            (True, '"イチロー" in nicknames'),
            (True, '"イチ" not in nicknames'),
            (True, 'favorites.1.name == "Apple"'),
            (True, 'favorites[1].name == "Apple"'),
            (False, 'favorites.0.name == "Apple"'),
            (False, 'favorites[0].name == "Apple"'),
            (True, 'favorites|length == 2'),
            (False, 'favorites|length == 3'),
            (True, 'id == 1 and age == 44'),
            (False, 'id == 1 and age == 45'),
            (True, 'id == 1 or age == 44'),
            (True, 'id == 1 or age == 45'),
            (False, 'id == 2 or age == 45'),
            (True, 'age|string|reg("[0-9]{2}")'),
            (False, 'age|string|reg("[0-9]{3}")'),
            (False, '(id == 1 or not name) and (favorites|length == 0 or nicknames|length == 0)'),
            (True, 'id == 1 or (not name and favorites|length == 0) or nicknames|length == 0'),
            (True, '"Apple" in favorites|map(attribute="name")'),
            (False, '"Grape" in favorites|map(attribute="name")'),
        ]
    )
    def test_normal(self, expected, expression):
        actual = utils.filter(expression, self.data)
        assert expected == actual

