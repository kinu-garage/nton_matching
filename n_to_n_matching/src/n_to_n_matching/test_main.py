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

from typing import List

from gj.grade_class import GjGradeGroup
from gj.printing import GjDocx
from gj.requirements import DateRequirement
from gj.responsibility import ResponsibilityLevel
from gj.role import Role, Roles_Definition, Roles_ID
from gj.spreadsheet_access import GjRowEntity
from gj.spreadsheet_access import GjToubanAccess2024 as GTA
from n_to_n_matching.match_game import GjVolunteerAllocationGame
from n_to_n_matching.person_player import PersonPlayer
from n_to_n_matching.workdate_player import WorkDate


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
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.TOSHO_COMMITEE),
        },
        {
            "id": 2,
            "name": "guardian-name2",
            "phone": "000-000-0000",
            "email": "2@dot.com.dummy",
            "children": {
              "child_id": "000003"},
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.TOSHO_COMMITEE),
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
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.GAKYU_COMMITEE),
        },
        {
            "id": 4,
            "name": "guardian-name4",
            "phone": "000-000-0000",
            "email": "4@dot.com.dummy",
            "children": {
              "child_id": "000007"},
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.SAFETY_COMMITEE),
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
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.UNDOKAI_COMMITEE),
        },
        {
            "id": 6,
            "name": "guardian-name6",
            "phone": "000-000-0000",
            "email": "6@dot.com.dummy",
            "children": {
                "child_id": "000012"},
        },
        {
            "id": 7,
            "name": "guardian-name7",
            "phone": "000-000-0000",
            "email": "7@dot.com.dummy",
            "children": {
                "child_id": "000013",
                "child_id": "000014"},
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
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.UNEI_COMMITEE),
        },
        {
            "id": 12,
            "name": "guardian-name12",
            "phone": "000-000-0000",
            "email": "12@dot.com.dummy",
            "children": {
                "child_id": "000025",},
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
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.GYOJI_COMMITEE),
        },
        {
            "id": 14,
            "name": "guardian-name14",
            "phone": "000-000-0000",
            "email": "14@dot.com.dummy",
            "children": {
                "child_id": "000029",
                "child_id": "000030",},
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
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.TOSHO_COMMITEE),
        },
        {
            "id": 17,
            "name": "guardian-name17",
            "phone": "000-000-0000",
            "email": "17@dot.com.dummy",
            "children": {
              "child_id": "000036",
              "child_id": "000037",},
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.PHOTO_CLUE),
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
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.UNDOKAI_COMMITEE),
        },
        {
            "id": 19,
            "name": "guardian-name19",
            "phone": "000-000-0000",
            "email": "19@dot.com.dummy",
            "children": {
              "child_id": "000040",
              "child_id": "000041",},
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.GAKYU_COMMITEE),
        },
        {
            "id": 20,
            "name": "guardian-name20",
            "phone": "000-000-0000",
            "email": "20@dot.com.dummy",
            "children": {
              "child_id": "000042",
              "child_id": "000043",},
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.UNDOKAI_COMMITEE),
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
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.TOUBAN_COMMITEE),
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
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.UNDOKAI_COMMITEE),
        },
        {
            "id": 23,
            "name": "guardian-name23",
            "phone": "000-000-0000",
            "email": "23@dot.com.dummy",
            "children": {
              "child_id": "000050",},
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.SAFETY_COMMITEE),
        },
        {
            "id": 24,
            "name": "guardian-name24",
            "phone": "000-000-0000",
            "email": "24@dot.com.dummy",
            "children": {
              "child_id": "000051",
              "child_id": "000052",},
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.SAFETY_COMMITEE),
        },
        {
            "id": 25,
            "name": "guardian-name25",
            "phone": "000-000-0000",
            "email": "25@dot.com.dummy",
            "children": {
              "child_id": "000053",
              "child_id": "000054",},
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.GYOJI_COMMITEE),
        },
        {
            "id": 26,
            "name": "guardian-name26",
            "phone": "000-000-0000",
            "email": "26@dot.com.dummy",
            "children": {
              "child_id": "000055",
              "child_id": "000056",},
        },
        {
            "id": 27,
            "name": "guardian-name27",
            "phone": "000-000-0000",
            "email": "27@dot.com.dummy",
            "children": {
              "child_id": "000057",
              "child_id": "000058",},
        },
        {
            "id": 28,
            "name": "guardian-name28",
            "phone": "000-000-0000",
            "email": "28@dot.com.dummy",
            "children": {
              "child_id": "000059",},
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.GYOJI_COMMITEE),
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
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.UNEI_COMMITEE),
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
        },
        {
            "id": 33,
            "name": "guardian-name33",
            "phone": "000-000-0000",
            "email": "33@dot.com.dummy",
            "children": {
              "child_id": "000072",},
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.GYOJI_COMMITEE),
        },
        {
            "id": 34,
            "name": "guardian-name34",
            "phone": "000-000-0000",
            "email": "34@dot.com.dummy",
            "children": {
              "child_id": "000073",
              "child_id": "000074",},
            PersonPlayer.ATTR_ROLE_ID: Role(Roles_Definition.GAKYU_COMMITEE),
        },
        {
            "id": 35,
            "name": "guardian-name35",
            "phone": "000-000-0000",
            "email": "35@dot.com.dummy",
            "children": {
              "child_id": "000075",},
        },
    ])
    return persons

def requirement_set_0(duty_type=Roles_Definition.TOSHO_COMMITEE):
    return {
            WorkDate.ATTR_DUTY_TYPE: duty_type,
            WorkDate.REQ_INTERVAL_ASSIGNEDDATES_LEADER: 3*7,
            WorkDate.REQ_INTERVAL_ASSIGNEDDATES_COMMITTE: 3*7,
            WorkDate.REQ_INTERVAL_ASSIGNEDDATES_GENERAL: 5*7,
            WorkDate.ATTR_NUM_LEADER: 1,
            WorkDate.ATTR_NUM_COMMITTEE: 2,
            WorkDate.ATTR_NUM_GENERAL: 1,
        }

def fixture_dates_0():
    return {
        WorkDate.ATTR_SECTION: [
            { WorkDate.ATTR_DATE: "2024-04-13", },
            {
                WorkDate.ATTR_DATE: "2024-04-20",
                WorkDate.ATTR_NUM_LEADER: 1,
                WorkDate.ATTR_NUM_COMMITTEE: 2,
                WorkDate.ATTR_NUM_GENERAL: 2,
            },
            { WorkDate.ATTR_DATE: "2024-04-27", },
            { WorkDate.ATTR_DATE: "2024-05-04", },
        ]}

def fixture_dates_1():
    dates = fixture_dates_0()
    dates[WorkDate.ATTR_SECTION].extend([
        { 
            WorkDate.ATTR_DATE: "2024-05-11", 
            WorkDate.ATTR_EXEMPT_GRADE: GjGradeGroup.ELEM_SHOU,  # Entire elementary/Sho-gakko is exempted this day due to parent-teacher meeting.
         },
        {
            WorkDate.ATTR_DATE: "2024-05-18", 
            WorkDate.ATTR_EXEMPT_GRADE: GjGradeGroup.MIDD_HIGH_CHUKOU
         },
        { WorkDate.ATTR_DATE: "2024-05-25", 
          WorkDate.ATTR_NUM_GENERAL: 5,
         },
        { WorkDate.ATTR_DATE: "2024-06-01", },
    ])
    return dates

def fixture_dates_20250322():
    return {
        WorkDate.ATTR_SECTION: [
            { WorkDate.ATTR_DATE: "2025-04-12", },
            { WorkDate.ATTR_DATE: "2025-04-19", },
            { WorkDate.ATTR_DATE: "2025-04-26", },
            { WorkDate.ATTR_DATE: "2025-05-03", },
            { WorkDate.ATTR_DATE: "2025-05-10", },
            { WorkDate.ATTR_DATE: "2025-05-17", },
            { WorkDate.ATTR_DATE: "2025-05-24", },
            { WorkDate.ATTR_DATE: "2025-05-31", },
            { WorkDate.ATTR_DATE: "2025-06-07", },
            { WorkDate.ATTR_DATE: "2025-06-14", },
        ]}

def fixture_dates_20250503():
    return {
        WorkDate.ATTR_SECTION: [
            { WorkDate.ATTR_DATE: "2025-06-07", },
            { WorkDate.ATTR_DATE: "2025-08-02", },
            { WorkDate.ATTR_DATE: "2025-08-09", },
            { WorkDate.ATTR_DATE: "2025-08-16", },
            { WorkDate.ATTR_DATE: "2025-08-23", },
            { WorkDate.ATTR_DATE: "2025-08-30", },

        ]}

def fixture_dates_20250503_v2(duty_type=Roles_Definition.TOSHO_COMMITEE):
    return {
        DateRequirement.ATTR_SECTION: [
            { WorkDate.ATTR_DUTY_TYPE: duty_type, },
            { WorkDate.REQ_INTERVAL_ASSIGNEDDATES_LEADER: 3*7, },
            { WorkDate.REQ_INTERVAL_ASSIGNEDDATES_COMMITTE: 3*7, },
            { WorkDate.REQ_INTERVAL_ASSIGNEDDATES_GENERAL: 5*7, },
            { WorkDate.ATTR_NUM_LEADER: 1, },
            { WorkDate.ATTR_NUM_COMMITTEE: 2, },
            { WorkDate.ATTR_NUM_GENERAL: 1, },
        ],
        WorkDate.ATTR_SECTION: [
            { WorkDate.ATTR_DATE: "2025-06-07", },
            { WorkDate.ATTR_DATE: "2025-08-02", },
            { WorkDate.ATTR_DATE: "2025-08-09", },
            { WorkDate.ATTR_DATE: "2025-08-16", },
            { WorkDate.ATTR_DATE: "2025-08-23", },
            { WorkDate.ATTR_DATE: "2025-08-30", },

        ]            
        }

def _fixture_dates_per_role(duty_type, dates):
    reqs = requirement_set_0(duty_type)
    dal = {DateRequirement.ATTR_SECTION: reqs}
    dal[WorkDate.ATTR_SECTION] = dates[WorkDate.ATTR_SECTION]
    return dal

def test_1(guardian_input):
    #dates_input = Util.read_yaml_to_dict(base_url, "dates.yml")
    dates_input = fixture_dates_1()

    solution = GjVolunteerAllocationGame.create_from_dictionaries(
        dates_input, guardian_input).solve()
    #for date, guardians in solution.items():
    #    print(f"{date}\n\tLeader: {guardians[WorkDate.ATTR_LIST_ASSIGNED_LEADER]}\n\t{guardians}")
    GjVolunteerAllocationGame.print_tabular_stdout(solution)

def test_2():
    #guardian_input = Util.read_yaml_to_dict(base_url, "guardian.yml")
    guardian_input = fixture_persons_3()

    test_1(guardian_input)

_MSG_AFTER_TABLE_HOKEN_20250503 = """
＜保健当番の方へ＞　※当番にアサインされ、この当番表を受け取ったらすぐに以下に一通り目を通してください。※
★集合場所：保健室（315教室）　集合時間：午前8時45分（～午後3時頃終了予定）　※昼食は各自ご持参ください。
※保健室の場所は、正面玄関を入って突き当りのカフェテリアを右に曲がって右側角の315教室（10月5日にDojoで配信された教室配置図を参考に）
★添付のプリントを読み、一日の流れや仕事内容などを把握しておいて下さい。
★当日、応援の手が必要になった場合は、事務局もしくは図書当番リーダーに声をかけ、応援を要請してください。
★当番の日に都合が悪い場合（一時帰国、退学予定も含む）は、上記の電話番号または登校日等を利用し各自で交替の方を見つけ、速やかに 
　①当番作成委員 ②もとの当番日のリーダー ③交替日のリーダーに必ず連絡して下さい。
★リーダーの方が当番日を変更される場合は、①当番作成委員 ②もとの当番日の前の週のリーダー ③交替日の前の週のリーダー
　の3名に連絡してください。　
　　※当番の交替は、できるだけ当番表の中の方から見つけて下さい。どうしても見つからない場合は、当番表にない方でもよいものとします。
★リーダーの方へ：①同じ日の当番の方に１週間前にテキストでリマインドの連絡をして下さい。
　　　　　　　　　②交替者なく休まれた方がいらした場合は、当番作成委員までご連絡下さい。
　　　　　　　　　③当番終了後、当番表を確認し、次週保健当番のリーダーの方に確認の連絡をして下さい。
★交替者なく休まれた方には、やり直し1回に加え、更にペナルティー1回の合計2回当番をお願いする事になりますので、ご注意下さい。
★当番作成委員は、交替者を当番担当者に代わって見つけることは致しませんので、予めご了承願います。
★交通渋滞等で、当日遅れる場合は、必ず事務局に連絡を入れて下さい。

連絡先一覧
2025年度 当番表作成委員 (保健・図書　連絡・配信係）XXXXX  　touban-hoken_tosho@gjls.org
　ジョージア日本語学校"""

_MSG_AFTER_TABLE_SAFETY_20250503 = """
＜パトロール当番の方へ＞　※当番にアサインされ、この当番表を受け取ったらすぐに以下に一通り目を通してください。※
★集合場所：補習校正面玄関前　集合時間：午前8時15分（～午後3時30分頃終了予定）　※昼食は各自ご持参ください。
★添付のプリントを読み、ご自分の担当の当番欄（アルファベット表示）を確認し、一日の流れや仕事内容などを把握しておいて下さい。
★当番の日に都合が悪い場合（一時帰国、退学予定も含む）は、上記の電話番号または登校日等を利用し各自で交替の方を見つけ、速やかに 
　①当番作成委員 ②もとの当番日のリーダー ③交替日のリーダーに必ず連絡して下さい。
★リーダーの方が当番日を変更される場合は、①危機管理担当運営委員（Kocho@gjls.org）②当番表作成委員 ③もとの当番日の前の週のリーダー
　④交替日の前の週のリーダー　の4名に連絡してください。　
　※当番の交替は、できるだけ当番表の中の方から見つけて下さい。どうしても見つからない場合は、当番表にない方でもよいものとします。
★リーダーの方へ：①同じ日の当番の方々に１週間前にテキストでリマインドの連絡をして下さい。
　　　　　　　　　②交替者なく休まれた方がいらした場合は、当番表作成委員までご連絡下さい。
　　　　　　　　　③当番終了後、当番表を確認し、次週パトロール当番のリーダーの方に確認の連絡をして下さい。
★交替者なく休まれた方には、やり直し1回に加え、更にペナルティー1回の合計2回当番をお願いする事になりますので、ご注意下さい。
★当番表作成委員は、交替者を当番担当者に代わって見つけることは致しませんので、予めご了承願います。
★交通渋滞等で、当日遅れる場合は、必ず事務局に連絡を入れて下さい。
★駐車場の管理などもあり危険なため、パトロール当番は子供をつれての当番は禁止です。
★コロナに関連するお問い合わせ、パトロールの実務内容に関するお問い合わせは、危機管理担当運営委員（ Kocho@gjls.org）または運営委員に
　直接ご連絡下さい。当番表作成委員は割り当てた当番を変更する範囲でしかお問い合わせにお答えできませんのでご了承ください。

連絡先一覧
　2025年度 当番表作成委員 （パトロール連絡・配信係）　XXXX
　ジョージア日本語学校"""

_MSG_AFTER_TABLE_TOSHO_20250503 = """
＜図書当番の方へ＞　※当番にアサインされ、この当番表を受け取ったらすぐに以下に一通り目を通してください。※
★集合場所：図書室（300教室）　集合時間：午前8時45分　（～午後3時頃終了予定）　※昼食は各自ご持参ください。
※図書室の場所は、正面玄関を入って突き当りのカフェテリアを左に曲がって奥の方、300教室です（10月5日にDojoで配信された教室配置図を参考にしてください）
★当日、保健当番で応援の手が必要になった場合は、図書当番D,Eの方は、保健当番のお手伝いをお願いすることもあります。
★当番の日に都合が悪い場合(一時帰国、退学予定も含む)は上記の電話番号や登校日等を利用し各自交替の方を見つけ、速やかに下記の方までお知らせください。 
　　当番A・B・C： A・B・Cの中から交替者を見つけ、もとの当番日のリーダー、交替日のリーダー、当番表作成委員および図書委員長(tosho@gjls.org)へ連絡
　　当番D ： Dの中から交替者を見つけ、もとの当番日のリーダー、交替日のリーダー、および当番表作成委員へ連絡
　※当番の交替は、できるだけ当番表の中の方から見つけて下さい。どうしても見つからない場合は、当番表にない方でもよいものとします。
★リーダーの方へ：①同じ日の当番の方に１週間前にテキストでリマインドの連絡をして下さい。
　　　　　　　　　②交替者なく休まれた方がいらした場合は、当番作成委員までご連絡下さい。
　　　　　　　　　③当番終了後、当番表を確認し、次週図書当番のリーダーの方に確認の連絡をして下さい。
★交替者なく休まれた方には、やり直し1回に加え、更にペナルティー1回の合計2回当番をお願いする事になりますので、ご注意下さい。
★当番作成委員は、交替者を当番担当者に代わって見つけることは致しませんので、予めご了承願います。
★交通渋滞等で、当日遅れる場合は、必ず事務局に連絡を入れて下さい。

★運動会・球技大会の日の図書当番は、雨天で運動会・球技大会が中止をなった時のみ、活動があります。
連絡先一覧
2025年度 当番表作成委員 (保健・図書　連絡・配信係）XXXX   　touban-hoken_tosho@gjls.org
　ジョージア日本語学校"""

def test_3(path_touban_master_sheet, sheet_name, output_path="/cws/src/130s/nton_matching", role: Roles_ID=Roles_ID.TOSHO):
    touban_accessor = GTA()  # TODO What is this?
    guardian_input = touban_accessor.gj_xls_to_personobj(
        path_touban_master_sheet, sheet_name=sheet_name, row_spec=GjRowEntity.COL_TITLE_IDS_20250503)
    dates = fixture_dates_20250503_v2()
    _ROLE_CHOSEN = "(担当当番名)"
    if role == Roles_ID.TOSHO.value:
        dates_input = _fixture_dates_per_role(duty_type=Roles_Definition.TOSHO_COMMITEE, dates=dates)
        _paragraph_after_table = _MSG_AFTER_TABLE_TOSHO_20250503
        _ROLE_CHOSEN = Roles_Definition.TOSHO_COMMITEE.value
    elif role == Roles_ID.HOKEN.value:
        dates_input = _fixture_dates_per_role(duty_type=Roles_Definition.HOKEN_COMMITEE, dates=dates)
        _paragraph_after_table = _MSG_AFTER_TABLE_HOKEN_20250503
        _ROLE_CHOSEN = Roles_Definition.HOKEN_COMMITEE.value
    elif role == Roles_ID.ANZEN.value:
        dates_input = _fixture_dates_per_role(duty_type=Roles_Definition.SAFETY_COMMITEE, dates=dates)
        dates_input[DateRequirement.ATTR_SECTION][WorkDate.ATTR_NUM_GENERAL] = 3
        _paragraph_after_table = _MSG_AFTER_TABLE_SAFETY_20250503
        _ROLE_CHOSEN = Roles_Definition.SAFETY_COMMITEE.value

    print(f"064 {role=}")
    solution = GjVolunteerAllocationGame.create_from_dictionaries_2(
        dates_input, guardian_input, role=role).solve()    
    GjVolunteerAllocationGame.print_tabular_stdout(solution)

    docx_gen = GjDocx(output_path)
    docx_gen.print_distributable(
        solution=solution,
        requirements=solution.reqs,
        heading1=f"202508-09当番予定表: {_ROLE_CHOSEN}",
        paragraph_after_table=_paragraph_after_table,
        path_input_file=path_touban_master_sheet)
