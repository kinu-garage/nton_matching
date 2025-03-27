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

from enum import Enum


class Roles_Definition(Enum):
    """
    @description: The enumerated string values are meant to correspond to the string that are used
      in the cell in the input spreadsheet (called "免除対象" as of 2024/10) that
      'gj.speadsheet_access.GjRowEntity.exempted_on()' accesses.
    """
    GAKYU_COMMITEE = "学級委員"
    GYOJI_COMMITEE = "行事委員"
    HOKEN_COMMITEE = "保健委員"
    PHOTO_CLUE = "カメラ担当"
    SAFETY_COMMITEE = "安全対策委員"
    TOSHO_COMMITEE = "図書委員"
    UNEI_COMMITEE = "運営関係者"
    UNDOKAI_COMMITEE = "運動会委員"
    TOUBAN_COMMITEE = "当番作成委員"        
    UNDEFINED = "-1"


class Roles_ID(Enum):
    """
    @summry `ID` is not accurate. Re-defining roles with alphabet, primarilly for commandlien input.
    @todo Maintaining `Roles_ID` and `Roles_Definition` separately is very redundant for no good reasons.
    """
    ANZEN = "anzen"
    HOKEN = "hoken"
    TOSHO = "tosho"
    
    def __str__(self):
        return self.value


class Role():
    def __init__(self, id: Roles_Definition=Roles_Definition.UNDEFINED):
        self._role_id = id

    def __repr__(self):
        return self._role_id

    def __str__(self):
        return str(self._role_id)

    @property
    def id(self) -> Roles_Definition:
        return self._role_id

    @id.setter
    def id(self, val: Roles_Definition):
        raise NotImplementedError("Role ID should not be settable after initialization.")
