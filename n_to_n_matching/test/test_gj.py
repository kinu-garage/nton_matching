#!/usr/bin/env python

# Copyright 2024 Kinu Garage Inc.
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

"""Tests for the Hospital-Resident algorithm."""

import itertools 
import numpy as np
import pytest

from gj.test_data import (
    fixture_dates_0, fixture_dates_1, fixture_persons_1, game_obj,
    input_dates_obj, input_dates_yaml, input_guardians_yaml, input_persons_obj,
    max_allowed_days_per_person, path_touban_master_sheet
)
from gj.spreadsheet_access import GjToubanAccess2024
from gj.util import GjUtil
from n_to_n_matching.gj_rsc_matching import GjVolunteerMatching
from n_to_n_matching.match_game import GjVolunteerAllocationGame
from n_to_n_matching.person_player import ResponsibilityLevel
from n_to_n_matching.util import Util
#from n_to_n_matching.test_main import fixture_dates_0, fixture_dates_1, fixture_persons_1
from n_to_n_matching.workdate_player import DateRequirement, WorkDate


def _assert_assignees(list_assignees):
        assert len(list_assignees) == 0

def test_create_from_dict_dates(fixture_dates_0, input_dates_obj):
    # Input and output same length
    assert len(input_dates_obj) == len(fixture_dates_0)
    obj_ids = set()
    dates_list, reqs = input_dates_obj
    # Assigne field in the output instances is empty
    for date in dates_list:
        _assert_assignees(date.assignees_leader)
        _assert_assignees(date.assignees_committee)
        _assert_assignees(date.assignees_noncommittee)
        assert not date in obj_ids
        obj_ids.add(date)

def test_find_dates_need_attention(game_obj):
    dates_need_attention, dates_lgtm = game_obj.find_dates_need_attention(
        game_obj._dates)
    assert len(dates_need_attention) == 4
    assert len(dates_lgtm) == 0

def test_total_slots_required(game_obj):
    needed_leader, needed_committee, needed_general = GjUtil.total_slots_required(game_obj._dates)
    _EXPECTED_LEADER = 4
    _EXPECTED_COMMITTEE = 9
    _EXPECTED_NONCOMMITTEE = 13
    assert needed_leader == _EXPECTED_LEADER
    assert needed_committee == _EXPECTED_COMMITTEE
    assert needed_general == _EXPECTED_NONCOMMITTEE

def test_total_persons_available(game_obj):
    avaialable_leader, avaialable_committee, avaialable_general, exempted = GjUtil.total_persons_available(game_obj._person_bank)
    _EXPECTED_LEADER = 2
    _EXPECTED_COMMITTEE = 5
    _EXPECTED_NONCOMMITTEE = 5
    #assert avaialable_leader == _EXPECTED_LEADER  # In the change made in 0.2, 'leader' is no longer in the input info.
    assert avaialable_committee == _EXPECTED_COMMITTEE
    assert avaialable_general == _EXPECTED_NONCOMMITTEE

def _verify_allowance(_game_obj, allowance_obj_per_responsibility, expected_max, expected_unluck):
    """
    @deprecated
    """
    assert allowance_obj_per_responsibility[_game_obj.ATTR_MAX_STINT_OPPORTUNITIES] == expected_max
    assert allowance_obj_per_responsibility[_game_obj.ATTR_UNLUCKY_PERSON_NUMS] == expected_unluck

@pytest.fixture
def _expected_allowance():
    _EXPECTED_LEADER_MAX = 1
    _EXPECTED_LEADER_UNLUCKY = 1
    _EXPECTED_COMMITTEE_MAX = 1
    _EXPECTED_COMMITTEE_UNLUCKY = 4
    _EXPECTED_NONCOMMITTEE_MAX = 2
    _EXPECTED_NONCOMMITTEE_UNLUCKY = 3
    _EXPECTEDS = [
        [_EXPECTED_LEADER_MAX, _EXPECTED_LEADER_UNLUCKY],
        [_EXPECTED_COMMITTEE_MAX, _EXPECTED_COMMITTEE_UNLUCKY],
        [_EXPECTED_NONCOMMITTEE_MAX, _EXPECTED_NONCOMMITTEE_UNLUCKY]]
    return _EXPECTEDS

def _test_max_allowed_days_per_person(game_obj, per_responsibility, _expected_allowance_set):
    assert per_responsibility[game_obj.ATTR_MAX_STINT_OPPORTUNITIES] == _expected_allowance_set[0]
    assert per_responsibility[game_obj.ATTR_UNLUCKY_PERSON_NUMS] == _expected_allowance_set[1]

def test_max_allowed_days_per_person_leader(game_obj, max_allowed_days_per_person, _expected_allowance):
    per_responsibility = max_allowed_days_per_person[ResponsibilityLevel.LEADER]
    _test_max_allowed_days_per_person(game_obj, per_responsibility, _expected_allowance[0])

def test_max_allowed_days_per_person_commitee(game_obj, max_allowed_days_per_person, _expected_allowance):
    per_responsibility = max_allowed_days_per_person[ResponsibilityLevel.COMMITTEE]
    _test_max_allowed_days_per_person(game_obj, per_responsibility, _expected_allowance[1])

def test_max_allowed_days_per_person_noncommitee(game_obj, max_allowed_days_per_person, _expected_allowance):
    per_responsibility = max_allowed_days_per_person[ResponsibilityLevel.GENERAL]
    _test_max_allowed_days_per_person(game_obj, per_responsibility, _expected_allowance[2])

def wip_test_volunteer_april(input_guardians, input_dates):
    """Test the algorithm produces a valid solution."""
    game = VolunteerAllocation.create_from_dictionaries(
        resident_preferences, hospital_preferences, hospital_capacities
        )    

    matching_table = VolunteerAllocation.solve(input_guardians, input_dates)
    matched_dates = set(matching_table.keys())

    # Assert all input dates are listed in the result.
    assert set(input_dates) == matched_dates
    for date in matched_dates.dates:
        # assert each day 'required_personnel' is met.
        date_input = input_dates["date"]
        assert len(date.assignees) >= date_input

        for assignee in date.assignees:
        # TODO Assert in each date there's no duplicate players.
            print("TBD")
            
    matched_guardians = {r for guardians_matched in matching_table.values() for r in guardians_matched}
    for guardian in input_guardians:
        # Assert all input guardians are in the result.
        if guardian.matching:
            assert guardian in matched_guardians
        # Assert non-matched guardian is NOT in the result.            
        else:
            assert guardian not in matched_guardians

        # Assert no guardian is missing in the result.
        # Testing this way is kind of like a duplicate of checking `guardian.matching` but for now do it so..
        assert guardian in matched_guardians

        # TODO Assert guardian is assigned to 1 or more dates.
        assert guardian.dates

def test_get_assigned_dates(input_persons_obj, input_dates_obj, game_obj):
    dates_list, reqs = input_dates_obj
    date = dates_list[0]
    person = input_persons_obj[0]
    # Assign ther `person` to the `date`
    game_obj.assign_responsibility(date, person)
    # The person at 0th element in `input_persons_obj` is a leader.
    assert 1 == len(date.assignees_leader)
    # Expect len(assigned date) == 1.
    assert 1 == GjUtil.get_assigned_dates(person.id, dates_list)[0]

def test_dates_list_to_dict(input_dates_obj):
    dates_list, reqs = input_dates_obj
    dates_dict = GjVolunteerMatching.dates_list_to_dict(dates_list)
    for date_str, sub_dict in dates_dict.items():
        # Format of each `date_entry` instance must be the one defined in `dates_list_to_dict`. See its docstring.
        assert sub_dict
        assert isinstance(sub_dict[WorkDate.ATTR_SCHOOL_OFF], bool)

def _test_1(fixture_dates_1):
    #dates_input = Util.read_yaml_to_dict(base_url, "dates.yml")
    dates_input = fixture_dates_1

    solution = GjVolunteerAllocationGame.create_from_dictionaries(
        dates_input, guardian_input).solve()
    #for date, guardians in solution.items():
    #    print(f"{date}\n\tLeader: {guardians[WorkDate.ATTR_LIST_ASSIGNED_LEADER]}\n\t{guardians}")
    GjVolunteerAllocationGame.print_tabular_stdout(solution)

def _test_2():
    #guardian_input = Util.read_yaml_to_dict(base_url, "guardian.yml")
    guardian_input = fixture_persons_3()

    _test_1(guardian_input)

def test_3(path_touban_master_sheet, fixture_dates_1):
    touban_accessor = GjToubanAccess2024()
    guardian_input = touban_accessor.gj_xls_to_personobj(path_touban_master_sheet)

    solution = GjVolunteerAllocationGame.create_from_dictionaries_2(
        fixture_dates_1, guardian_input).solve()    

def test_calc_stint(game_obj):
    _needed_members = 21
    _available_members = 36
    max_stint, available_extra, unlucky = game_obj.calc_stint(_needed_members, _available_members)
    assert 1 == max_stint
    assert 15 == available_extra
    assert 0 == unlucky
