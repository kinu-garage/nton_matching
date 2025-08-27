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

from gj.util import GjUtil
from gj.test_data import SampleToubanMaster202507
from gj.spreadsheet_access import GjToubanAccess2024 as GTA

@pytest.fixture
def touban_accessor():
    return GTA()

@pytest.fixture
def path_touban_master_sheet():
    return SampleToubanMaster202507.path_touban_master_sheet_20240602()

@pytest.fixture
def xls_file_obj(path_touban_master_sheet):
    """
    @rtype openpyxl.workbook.workbook.Workbook
    """
    wb = xl.load_workbook(path_touban_master_sheet)
    return wb

@pytest.fixture
def _master_sheet(xls_file_obj):
    return GTA.get_a_sheet_by_name(xls_file_obj, SampleToubanMaster202507.sheet_title())

def test_get_a_sheet_by_name(_master_sheet, touban_accessor):
    """
    @description: Verifying the title of the "Master" sheet ends with the intended suffix.
    """
    assert _master_sheet.title == SampleToubanMaster202507.sheet_title()

def test_get_candidates_tosho(_master_sheet, touban_accessor):
    candidate_rows, row_ids = touban_accessor.get_candidates(_master_sheet, touban_accessor.NAME_TOSHOIIN)
    assert candidate_rows, f"Array of candidate not meeting criteria: '{candidate_rows}'"
    for row in candidate_rows:
        assert row[0].row in row_ids, f"Row returned does NOT match the row ID requested: '{row[0].row}'"
    
def _test_gj_xls_to_personobj(path_touban_master_sheet_20240602):
    gj2024 = GTA()
    person_bank = gj2024.gj_xls_to_personobj(path_touban_master_sheet_20240602, sheet_name=GTA._MASTERSHEET_2024)
    persons = person_bank.persons
    assert len(persons) == 269

def test_cs_values_from_cell(touban_accessor):
    test_str = "5/27,6/4,6/11,6/18"
    expected = ["5/27", "6/4", "6/11", "6/18"]
    actual = touban_accessor.get_cs_values_from_cell(test_str)
    assert expected == actual, f"Expected: '{expected}', Actual: '{actual}'"

def test_write_back_to_xls(path_touban_master_sheet, touban_accessor):
    gta = GTA()
    person_bank = gta.gj_xls_to_personobj(path_touban_master_sheet, sheet_name=SampleToubanMaster202507.sheet_title())
    persons = person_bank.persons

    # Modify some data
    for person in persons:
        if person.name_jpn == "行列 一蔵":
            # TODO Modify assigned dates
            person. .assigned_dates = ["5/27", "6/4"]
    # TODO Write back to the .xlsx file
    # TODO Get the values from the .xlsx file and verify if the values are  the same.