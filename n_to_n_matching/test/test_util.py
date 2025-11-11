#!/usr/bin/env python

# Copyright 2025 Kinu Garage Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import date
import pytest

from n_to_n_matching.util import Util

def test_create_date_from_mmdd():
    date_a = date(2025, 5, 27)
    date_b = Util.create_date_from_mmdd("5/27", 2025)
    assert date_a == date_b

@pytest.fixture
def pairs_dates():
    return [[date(2025, 6, 30), "6/30"],
            [date(2025, 4, 15), "4/15"],
            [date(2026, 1, 1), "1/01"],
            [date(2026, 2, 27), "2/27"],]

def test_create_date_from_str_jpn(pairs_dates):
    for date_pair in pairs_dates:
        date_a, date_str = date_pair
        date_b = Util.create_date_from_str(date_str)
        assert date_a == date_b

def test_create_date_from_str_usa(pairs_dates):
    for date_pair in pairs_dates:
        date_a, date_str = date_pair
        date_b = Util.create_date_from_str(date_str, months_in_subsequent_year=[1, 2, 3, 4, 5])
        assert date_a == date_b
