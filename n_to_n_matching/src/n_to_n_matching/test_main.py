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

from n_to_n_matching.match_game import GjVolunteerAllocationGame
from n_to_n_matching.person_player import PersonRole
from n_to_n_matching.workdate_player import WorkDate


def fixture_persons_1():
    return [
        {
            "id": 1,
            "name": "guardian-name1",
            "phone": "000-000-0000",
            "email": "1@dot.com.dummy",
            "children": {
              "child_id": 1111,
              "child_id": 1112},
            "role_id": PersonRole.LEADER.value
        },
        {
            "id": 2,
            "name": "guardian-name2",
            "phone": "000-000-0000",
            "email": "2@dot.com.dummy",
            "children": {
              "child_id": 1113},
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 3,
            "name": "guardian-name3",
            "phone": "000-000-0000",
            "email": "3@dot.com.dummy",
            "children": {
                "child_id": 1114,
                "child_id": 1115,
                "child_id": 1116},
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 4,
            "name": "guardian-name4",
            "phone": "000-000-0000",
            "email": "4@dot.com.dummy",
            "children": {
              "child_id": 1117},
            "role_id": PersonRole.LEADER.value
        },
        {
            "id": 5,
            "name": "guardian-name5",
            "phone": "000-000-0000",
            "email": "5@dot.com.dummy",
            "children": {
                "child_id": 1118,
                "child_id": 1119,
                "child_id": 1120,
                "child_id": 1121},
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 6,
            "name": "guardian-name6",
            "phone": "000-000-0000",
            "email": "6@dot.com.dummy",
            "children": {
                "child_id": 116},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 7,
            "name": "guardian-name7",
            "phone": "000-000-0000",
            "email": "7@dot.com.dummy",
            "children": {
                "child_id": 1171,
                "child_id": 1172},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 8,
            "name": "guardian-name8",
            "phone": "000-000-0000",
            "email": "8@dot.com.dummy",
            "children": {
                "child_id": 1181,
                "child_id": 1182,
                "child_id": 1183},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 9,
            "name": "guardian-name9",
            "phone": "000-000-0000",
            "email": "9@dot.com.dummy",
            "children": {
                "child_id": 1191,
                "child_id": 1192},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 10,
            "name": "guardian-name10",
            "phone": "000-000-0000",
            "email": "10@dot.com.dummy",
            "children": {
                "child_id": 11101,
                "child_id": 11102,
                "child_id": 11103,
                "child_id": 11104},
            "role_id": PersonRole.GENERAL.value
        },
    ]

def fixture_persons_2():
    persons = fixture_persons_1()
    persons.extend([{
            "id": 11,
            "name": "guardian-name11",
            "phone": "000-000-0000",
            "email": "11@dot.com.dummy",
            "children": {
              "child_id": 1111101,
              "child_id": 1111102,
              "child_id": 1111103,},
            "role_id": PersonRole.LEADER.value
        },
        {
            "id": 12,
            "name": "guardian-name12",
            "phone": "000-000-0000",
            "email": "12@dot.com.dummy",
            "children": {
                "child_id": 1111201,},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 13,
            "name": "guardian-name13",
            "phone": "000-000-0000",
            "email": "13@dot.com.dummy",
            "children": {
              "child_id": 1111301,
              "child_id": 1111302,
              "child_id": 1111303,
              },
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 14,
            "name": "guardian-name14",
            "phone": "000-000-0000",
            "email": "14@dot.com.dummy",
            "children": {
                "child_id": 1111401,
                "child_id": 1111402,
                },
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 15,
            "name": "guardian-name15",
            "phone": "000-000-0000",
            "email": "15@dot.com.dummy",
            "children": {
                "child_id": 1111501,
                "child_id": 1111502,
                "child_id": 1111503,
                "child_id": 1111504,
                },
            "role_id": PersonRole.GENERAL.value
        },
    ])
    return persons

def fixture_dates_0():
    return [
        { WorkDate.ATTR_DATE: "2024-04-01", },
        {
            WorkDate.ATTR_DATE: "2024-04-08",
            WorkDate.ATTR_NUM_LEADER: 1,
            WorkDate.ATTR_NUM_COMMITTEE: 3,
            WorkDate.ATTR_NUM_GENERAL: 4,
        },
        { WorkDate.ATTR_DATE: "2024-04-15", },
        { WorkDate.ATTR_DATE: "2024-04-22", },
    ]

def fixture_dates_1():
    dates = fixture_dates_0()
    dates.extend([
        { WorkDate.ATTR_DATE: "2024-04-29", },
        { WorkDate.ATTR_DATE: "2024-05-06", },
        { WorkDate.ATTR_DATE: "2024-05-13", },
        { WorkDate.ATTR_DATE: "2024-05-20", },
    ])
    return dates

def test_1():
    #dates_input = Util.read_yaml_to_dict(base_url, "dates.yml")
    dates_input = fixture_dates_1()
    #guardian_input = Util.read_yaml_to_dict(base_url, "guardian.yml")
    guardian_input = fixture_persons_2()

    num_dates = len(dates_input)
    num_guardians = len(guardian_input)
    solution = GjVolunteerAllocationGame.create_from_dictionaries(
        dates_input, guardian_input).solve()
    #for date, guardians in solution.items():
    #    print(f"{date}\n\tLeader: {guardians[WorkDate.ATTR_LIST_ASSIGNED_LEADER]}\n\t{guardians}")
    GjVolunteerAllocationGame.print_tabular_stdout(solution)
