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

from gj.grade_class import GjGrade, GjGradeGroup, GradeUtil

@pytest.fixture
def _grade_shou1_1():
    return GjGrade.ELEM_SHOU_1_1

def test_elem1_1_included_1stg(_grade_shou1_1):
    assert True == GradeUtil.included_grade(_grade_shou1_1, GjGradeGroup.ELEM_SHOU_1STG)

def test_elem1_1_included_kinder(_grade_shou1_1):
    assert False == GradeUtil.included_grade(_grade_shou1_1, GjGradeGroup.KINDER_YOCHIEN)

def test_elem1_1_included_elem_lower(_grade_shou1_1):
    assert True == GradeUtil.included_grade(_grade_shou1_1, GjGradeGroup.ELEM_SHOU_LOWER)

def test_elem1_1_included_elem_upper(_grade_shou1_1):
    assert False == GradeUtil.included_grade(_grade_shou1_1, GjGradeGroup.ELEM_SHOU_UPPER)

def test_elem1_1_included_elem(_grade_shou1_1):
    assert True == GradeUtil.included_grade(_grade_shou1_1, GjGradeGroup.ELEM_SHOU)

def test_elem1_1_included_midd(_grade_shou1_1):
    assert False == GradeUtil.included_grade(_grade_shou1_1, GjGradeGroup.MIDD_CHUU)
