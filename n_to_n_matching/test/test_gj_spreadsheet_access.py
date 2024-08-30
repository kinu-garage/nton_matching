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
from gj.spreadsheet_access import GjToubanAccess2024 as GTA

@pytest.fixture
def touban_accessor():
    return GTA()

@pytest.fixture
def path_to_202406():
    return 'n_to_n_matching/test/20240602-updated_gjls_student-master.xlsx'

@pytest.fixture
def xls_file_obj(path_to_202406):
    """
    @rtype openpyxl.workbook.workbook.Workbook
    """
    wb = xl.load_workbook(path_to_202406)
    return wb

@pytest.fixture
def _master_sheet(xls_file_obj):
    return GTA.get_a_sheet_by_name(xls_file_obj, GTA.MASTERSHEET_2024)

def test_get_a_sheet_by_name(_master_sheet, touban_accessor):
    """
    @description: Verifying the title of the "Master" sheet ends with the intended suffix.
    """
    assert _master_sheet.title == GTA.MASTERSHEET_2024

def test_get_candidates_tosho(_master_sheet, touban_accessor):
    candidate_rows, row_ids = touban_accessor.get_candidates(_master_sheet, touban_accessor.NAME_TOSHOIIN)
    assert candidate_rows, f"Array of candidate not meeting criteria: '{candidate_rows}'"
    for row in candidate_rows:
        assert row[0].row in row_ids, f"Row returned does NOT match the row ID requested: '{row[0].row}'"
    
def test_gj_xls_to_personobj(path_to_202406):
    gj2024 = GTA()
    person_bank = gj2024.gj_xls_to_personobj(path_to_202406)
    #assert len(person_bank.persons) == 269
    persons = person_bank.persons
    assert len(persons) == 269
