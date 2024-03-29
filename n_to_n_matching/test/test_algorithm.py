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
from hypothesis import given
import numpy as np
import pytest

from n_to_n_matching.match_game import GjVolunteerAllocationGame
from n_to_n_matching.gj_rsc_matching import GjVolunteerMatching
from n_to_n_matching.gj_util import GjUtil
from n_to_n_matching.util import Util
from n_to_n_matching.test_main import fixture_dates_0, fixture_dates_1, fixture_persons_1
from n_to_n_matching.workdate_player import WorkDate

@pytest.fixture
def input_guardians_yaml():
    return Util.read_yaml_to_dict(base_url, "test_guardians.yaml")

@pytest.fixture
def input_guardians_src():
    return fixture_persons_1()

@pytest.fixture
def input_dates_src():
    """
    @return: 
      [{ "id", "name", "phone", "email",
         "children": {"child_id"}, "role_id" }]
    """
    return fixture_dates_0()

@pytest.fixture
def input_dates_yaml():
    base_url = "tbd"
    return Util.read_yaml_to_dict(base_url, "test_volunteer-dates.yaml")

@pytest.fixture
def input_dates_obj(input_dates_src):
    """
    @summary Generated by GjVolunteerAllocationGame.create_from_dict_dates
    """
    return GjVolunteerAllocationGame.create_from_dict_dates(input_dates_src, clean=False)

@pytest.fixture
def input_persons_obj(input_guardians_src):
    return GjVolunteerAllocationGame.create_from_dict_persons(input_guardians_src)

@pytest.fixture
def game_obj(input_dates_src, input_guardians_src):
    """
    @summary As for now, the game obj returned by this fixture method is embeds specific input state,
        which is defined by the another fixture input `input_dates_src, input_guardians_src`.
    """
    return GjVolunteerAllocationGame.create_from_dictionaries(
        input_dates_src, input_guardians_src)

def _assert_assignees(list_assignees):
        assert len(list_assignees) == 0

def test_create_from_dict_dates(input_dates_src, input_dates_obj):
    # Input and output same length
    assert len(input_dates_obj) == len(input_dates_src)
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
    avaialable_leader, avaialable_committee, avaialable_general = GjUtil.total_persons_available(game_obj._person_bank)
    _EXPECTED_LEADER = 2
    _EXPECTED_COMMITTEE = 3
    _EXPECTED_NONCOMMITTEE = 5
    assert avaialable_leader == _EXPECTED_LEADER
    assert avaialable_committee == _EXPECTED_COMMITTEE
    assert avaialable_general == _EXPECTED_NONCOMMITTEE

def _verify_allowance(_game_obj, allowance_obj_per_role, expected_max, expected_unluck):
    assert allowance_obj_per_role[_game_obj.ATTR_MAX_OCCURRENCE_PER_ROLE] == expected_max
    assert allowance_obj_per_role[_game_obj.ATTR_UNLUCKY_PERSON_NUMS] == expected_unluck

def test_max_allowed_days_per_person(input_dates_obj, game_obj):
    dates_list, reqs = input_dates_obj
    max_allowance = game_obj.max_allowed_days_per_person(dates_list, game_obj._person_bank)
    _EXPECTED_LEADER_MAX = 2
    _EXPECTED_LEADER_UNLUCKY = 0
    _EXPECTED_COMMITTEE_MAX = 3
    _EXPECTED_COMMITTEE_UNLUCKY = 0
    _EXPECTED_NONCOMMITTEE_MAX = 2
    _EXPECTED_NONCOMMITTEE_UNLUCKY = 3
    _EXPECTEDS = [
        [_EXPECTED_LEADER_MAX, _EXPECTED_LEADER_UNLUCKY],
        [_EXPECTED_COMMITTEE_MAX, _EXPECTED_COMMITTEE_UNLUCKY],
        [_EXPECTED_NONCOMMITTEE_MAX, _EXPECTED_NONCOMMITTEE_UNLUCKY]]
    for (per_role, expected_set) in itertools.zip_longest(max_allowance.values(), _EXPECTEDS):
        _verify_allowance(game_obj, per_role, expected_set[0], expected_set[1])

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
    game_obj.assign_role(date, person)
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
        
