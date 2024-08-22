#!/usr/bin/env python

# Copyright 2024 Kinu Garage Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");130s/nton_matching/n_to_n_matching/test/test_algorithm.py
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

import openpyxl as xl
import pytest

from n_to_n_matching.spreadsheet_access import Cell, Row

@pytest.fixture
def cell_titles():
    titles = ["title1", "title2", "title3", "title4"]
    return titles

@pytest.fixture
def cell_titles_with_empty(cell_titles):
    cell_titles.insert(1, "")
    return cell_titles

@pytest.fixture
def a_row(cell_titles):
    row = Row()
    row.set_row_by_strs(cell_titles)
    return row

def _test_set_row_by_cells():
    raise NotImplementedError()

def test_set_row_by_strs_num(cell_titles, a_row):
    assert len(a_row._cells_in_a_row) == len(cell_titles)

def test_set_row_by_strs_with_empty_cell(cell_titles_with_empty, a_row):
    assert len(a_row._cells_in_a_row) == len(cell_titles_with_empty)

def test_get_col_title(cell_titles, a_row):
    INDEX_TEST = 2
    assert cell_titles[INDEX_TEST] == a_row.get_col_title(INDEX_TEST)

def test_get_col_id(cell_titles, a_row):
    TITLE_TEST = "title3"

    index_test = cell_titles.index(TITLE_TEST)
    assert index_test == a_row.get_col_id(TITLE_TEST)
