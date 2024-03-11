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
from n_to_n_matching.workdate_player import DateRequirement, WorkDate


def fixture_persons_1():
    return [
        {
            "id": 1,
            "name": "guardian-name1",
            "phone": "000-000-0000",
            "email": "1@dot.com.dummy",
            "children": {
              "child_id": "000001",
              "child_id": "000002"},
            "role_id": PersonRole.LEADER.value
        },
        {
            "id": 2,
            "name": "guardian-name2",
            "phone": "000-000-0000",
            "email": "2@dot.com.dummy",
            "children": {
              "child_id": "000003"},
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 3,
            "name": "guardian-name3",
            "phone": "000-000-0000",
            "email": "3@dot.com.dummy",
            "children": {
                "child_id": "000004",
                "child_id": "000005",
                "child_id": "000006"},
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 4,
            "name": "guardian-name4",
            "phone": "000-000-0000",
            "email": "4@dot.com.dummy",
            "children": {
              "child_id": "000007"},
            "role_id": PersonRole.LEADER.value
        },
        {
            "id": 5,
            "name": "guardian-name5",
            "phone": "000-000-0000",
            "email": "5@dot.com.dummy",
            "children": {
                "child_id": "00008",
                "child_id": "00009",
                "child_id": "000010",
                "child_id": "000011"},
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 6,
            "name": "guardian-name6",
            "phone": "000-000-0000",
            "email": "6@dot.com.dummy",
            "children": {
                "child_id": "000012"},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 7,
            "name": "guardian-name7",
            "phone": "000-000-0000",
            "email": "7@dot.com.dummy",
            "children": {
                "child_id": "000013",
                "child_id": "000014"},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 8,
            "name": "guardian-name8",
            "phone": "000-000-0000",
            "email": "8@dot.com.dummy",
            "children": {
                "child_id": "000015",
                "child_id": "000016",
                "child_id": "000017",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 9,
            "name": "guardian-name9",
            "phone": "000-000-0000",
            "email": "9@dot.com.dummy",
            "children": {
                "child_id": "000018",
                "child_id": "000019",
                "child_id": "000020",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 10,
            "name": "guardian-name10",
            "phone": "000-000-0000",
            "email": "10@dot.com.dummy",
            "children": {
                "child_id": "000021",
                "child_id": "000022",
                "child_id": "000023",
                "child_id": "000024"},
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
              "child_id": "000022",
              "child_id": "000023",
              "child_id": "000024",},
            "role_id": PersonRole.LEADER.value
        },
        {
            "id": 12,
            "name": "guardian-name12",
            "phone": "000-000-0000",
            "email": "12@dot.com.dummy",
            "children": {
                "child_id": "000025",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 13,
            "name": "guardian-name13",
            "phone": "000-000-0000",
            "email": "13@dot.com.dummy",
            "children": {
              "child_id": "000026",
              "child_id": "000027",
              "child_id": "000028",},
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 14,
            "name": "guardian-name14",
            "phone": "000-000-0000",
            "email": "14@dot.com.dummy",
            "children": {
                "child_id": "000029",
                "child_id": "000030",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 15,
            "name": "guardian-name15",
            "phone": "000-000-0000",
            "email": "15@dot.com.dummy",
            "children": {
                "child_id": "000031",
                "child_id": "000032",
                "child_id": "000033",
                "child_id": "000034",},
            "role_id": PersonRole.GENERAL.value
        },
    ])
    return persons

def fixture_persons_3():
    persons = fixture_persons_2()
    persons.extend([
        {
            "id": 16,
            "name": "guardian-name16",
            "phone": "000-000-0000",
            "email": "16@dot.com.dummy",
            "children": {
              "child_id": "000035",
            },
            "role_id": PersonRole.LEADER.value
        },
        {
            "id": 17,
            "name": "guardian-name17",
            "phone": "000-000-0000",
            "email": "17@dot.com.dummy",
            "children": {
              "child_id": "000036",
              "child_id": "000037",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 18,
            "name": "guardian-name18",
            "phone": "000-000-0000",
            "email": "18@dot.com.dummy",
            "children": {
              "child_id": "000038",
              "child_id": "000039",
              "child_id": "000040",},
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 19,
            "name": "guardian-name19",
            "phone": "000-000-0000",
            "email": "19@dot.com.dummy",
            "children": {
              "child_id": "000040",
              "child_id": "000041",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 20,
            "name": "guardian-name20",
            "phone": "000-000-0000",
            "email": "20@dot.com.dummy",
            "children": {
              "child_id": "000042",
              "child_id": "000043",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 21,
            "name": "guardian-name21",
            "phone": "000-000-0000",
            "email": "21@dot.com.dummy",
            "children": {
              "child_id": "000044",
              "child_id": "000045",
              "child_id": "000046",
            },
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 22,
            "name": "guardian-name22",
            "phone": "000-000-0000",
            "email": "22@dot.com.dummy",
            "children": {
              "child_id": "000047",
              "child_id": "000048",
              "child_id": "000049",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 23,
            "name": "guardian-name23",
            "phone": "000-000-0000",
            "email": "23@dot.com.dummy",
            "children": {
              "child_id": "000050",},
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 24,
            "name": "guardian-name24",
            "phone": "000-000-0000",
            "email": "24@dot.com.dummy",
            "children": {
              "child_id": "000051",
              "child_id": "000052",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 25,
            "name": "guardian-name25",
            "phone": "000-000-0000",
            "email": "25@dot.com.dummy",
            "children": {
              "child_id": "000053",
              "child_id": "000054",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 26,
            "name": "guardian-name26",
            "phone": "000-000-0000",
            "email": "26@dot.com.dummy",
            "children": {
              "child_id": "000055",
              "child_id": "000056",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 27,
            "name": "guardian-name27",
            "phone": "000-000-0000",
            "email": "27@dot.com.dummy",
            "children": {
              "child_id": "000057",
              "child_id": "000058",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 28,
            "name": "guardian-name28",
            "phone": "000-000-0000",
            "email": "28@dot.com.dummy",
            "children": {
              "child_id": "000059",},
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 29,
            "name": "guardian-name29",
            "phone": "000-000-0000",
            "email": "29@dot.com.dummy",
            "children": {
              "child_id": "000060",
              "child_id": "000061",
              "child_id": "000062",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 30,
            "name": "guardian-name30",
            "phone": "000-000-0000",
            "email": "30@dot.com.dummy",
            "children": {
              "child_id": "000063",
              "child_id": "000064",
              "child_id": "000065",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 31,
            "name": "guardian-name31",
            "phone": "000-000-0000",
            "email": "31@dot.com.dummy",
            "children": {
              "child_id": "000066",
              "child_id": "000067",
              "child_id": "000068",
            },
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 32,
            "name": "guardian-name32",
            "phone": "000-000-0000",
            "email": "32@dot.com.dummy",
            "children": {
              "child_id": "000069",
              "child_id": "000070",
              "child_id": "000071",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 33,
            "name": "guardian-name33",
            "phone": "000-000-0000",
            "email": "33@dot.com.dummy",
            "children": {
              "child_id": "000072",},
            "role_id": PersonRole.COMMITTEE.value
        },
        {
            "id": 34,
            "name": "guardian-name34",
            "phone": "000-000-0000",
            "email": "34@dot.com.dummy",
            "children": {
              "child_id": "000073",
              "child_id": "000074",},
            "role_id": PersonRole.GENERAL.value
        },
        {
            "id": 35,
            "name": "guardian-name35",
            "phone": "000-000-0000",
            "email": "35@dot.com.dummy",
            "children": {
              "child_id": "000075",},
            "role_id": PersonRole.GENERAL.value
        },
    ])
    return persons

def fixture_dates_0():
    return {
        DateRequirement.ATTR_SECTION: {
            WorkDate.REQ_INTERVAL_ASSIGNEDDATES_LEADER: 3*7,
            WorkDate.REQ_INTERVAL_ASSIGNEDDATES_COMMITTE: 3*7,
            WorkDate.REQ_INTERVAL_ASSIGNEDDATES_GENERAL: 5*7,
        },
        WorkDate.ATTR_SECTION: [
            { WorkDate.ATTR_DATE: "2024-04-13", },
            {
                WorkDate.ATTR_DATE: "2024-04-20",
                WorkDate.ATTR_NUM_LEADER: 1,
                WorkDate.ATTR_NUM_COMMITTEE: 3,
                WorkDate.ATTR_NUM_GENERAL: 4,
            },
            { WorkDate.ATTR_DATE: "2024-04-27", },
            { WorkDate.ATTR_DATE: "2024-05-04", },
        ]}

def fixture_dates_1():
    dates = fixture_dates_0()
    dates[WorkDate.ATTR_SECTION].extend([
        { WorkDate.ATTR_DATE: "2024-05-11", },
        { WorkDate.ATTR_DATE: "2024-05-18", },
        { WorkDate.ATTR_DATE: "2024-05-25", 
          WorkDate.ATTR_NUM_GENERAL: 5,
         },
        { WorkDate.ATTR_DATE: "2024-06-01", },
        { WorkDate.ATTR_DATE: "2024-06-08", },
        { WorkDate.ATTR_DATE: "2024-06-15", },
    ])
    return dates

def test_1():
    #dates_input = Util.read_yaml_to_dict(base_url, "dates.yml")
    dates_input = fixture_dates_1()
    #guardian_input = Util.read_yaml_to_dict(base_url, "guardian.yml")
    guardian_input = fixture_persons_3()

    solution = GjVolunteerAllocationGame.create_from_dictionaries(
        dates_input, guardian_input).solve()
    #for date, guardians in solution.items():
    #    print(f"{date}\n\tLeader: {guardians[WorkDate.ATTR_LIST_ASSIGNED_LEADER]}\n\t{guardians}")
    GjVolunteerAllocationGame.print_tabular_stdout(solution)
