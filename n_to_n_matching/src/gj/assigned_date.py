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

import datetime

from gj.responsibility import Responsibility
from gj.role import Role


class AssignedDate():
    """
    @summary: Initial purpose of this class is to provide an easier way to manage the last-assigned-date with the specific responsibility for a person.
    """
    _MSG_ERR_VALCANNOTBESET = "'{}' cannot be set once the object is initialized. Should've been set during initialization."

    def __init__(self,
                 date: datetime.date,
                 role: Role,
                 rank_in_role: int,
                 responsibility: Responsibility,
                 comment: str=""):
        """
        @param comment: Any comment can be stored. Primary motive of this is to store a 'rank', an info stored in the GJLS' master file
           that represents the detailed duty within a responsibility. E.g. in 'tosho' responsibility, there are A/B/C/D ranks as of 2025/08.
        """
        self._date = date
        self._responsibility = responsibility
        self._role = role
        self._comment = comment

    @property
    def date(self) -> datetime.date:
        return self._date

    @date.setter
    def date(self, value: datetime.date):
        raise RuntimeError(self._MSG_ERR_VALCANNOTBESET.format("date"))

    @property
    def responsibility(self) -> Responsibility:
        return self._responsibility

    @responsibility.setter
    def responsibility(self, value: Responsibility):
        raise RuntimeError(self._MSG_ERR_VALCANNOTBESET.format("responsibility"))

    @property
    def role(self) -> Role:
        return self._role

    @role.setter
    def role(self, value: Role):
        raise RuntimeError(self._MSG_ERR_VALCANNOTBESET.format("role"))

    @property
    def comment(self) -> str:
        return self._comment

    @comment.setter
    def comment(self, value: str):
        self._comment = value
