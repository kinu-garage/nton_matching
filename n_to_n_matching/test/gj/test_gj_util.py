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

import pytest

from gj.util import GjUtil
from n_to_n_matching.test_main import fixture_dates_202509
from n_to_n_matching.workdate_player import WorkDate


def test_guess_fiscal_year():
    dates = fixture_dates_202509()
    assert GjUtil.guess_fiscal_year(dates[WorkDate.ATTR_SECTION])  == "2025-2026"
