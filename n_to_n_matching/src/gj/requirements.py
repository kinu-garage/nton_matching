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

import datetime
from typing import List

from gj.role import Roles_Definition
from n_to_n_matching.workdate_player import WorkDate

class Consts():
    ATTR_MAX_STINT_OPPORTUNITIES = "max_stint_opportunities"
    ATTR_AVAILABLE_EXTRAS = "num_available_extra"
    ATTR_UNLUCKY_PERSON_NUMS = "num_unlucky_person"    
    

class DateRequirement():
    _MSG_SETTER_NOTALlOWED = "The value is only allowed to be set upon initializing the instance."
    ATTR_SECTION = "Requirement"

    def __init__(self,
                 dates: List[WorkDate],
                 type_duty: Roles_Definition,
                 interval_assigneddates_leader=3,
                 interval_assigneddates_commitee=4,
                 interval_assigneddates_general=5,
                 num_leaders=1,
                 num_committee=2,
                 num_general=2,
                 fiscal_year_start: datetime.date=datetime.date(2025, 4, 1)):
        """
        @param fiscal_year_start: The earliest date in the fiscal year, usually April 1st.
        """
        self._type_duty = type_duty
        self._interval_assigneddates_leader = interval_assigneddates_leader
        self._interval_assigneddates_commitee = interval_assigneddates_commitee
        self._interval_assigneddates_general = interval_assigneddates_general
        self._num_leaders = num_leaders
        self._num_committee = num_committee
        self._num_general = num_general
        self._date_earliest = None
        self._fiscal_year_start = fiscal_year_start
        self._dates = DateRequirement.gen_date_objs(dates, self._num_leaders)

    @staticmethod
    def gen_date_objs(dates_prefs: List[dict], num_leaders: int, num_committee: int, num_general: int) -> List[WorkDate]:
        """
        @param dates_prefs: A list of dictionary, each containing the attributes defined in `WorkDate`.
        @param fiscal_year_start: The earliest date in the fiscal year, usually April 1st.
        @return: A list of `WorkDate` instances.
        @raise ValueError: When any of the required attributes is missing in the input data.
        """
        _dates = [WorkDate(datestr=date[WorkDate.ATTR_DATE],
                           school_off=date.get(WorkDate.ATTR_SCHOOL_OFF, False),
                           req_num_leader=date.get(WorkDate.ATTR_NUM_LEADER, num_leaders),
                           req_num_committee=date.get(WorkDate.ATTR_NUM_COMMITTEE, num_committee),
                           req_num_noncommittee=date.get(WorkDate.ATTR_NUM_GENERAL, num_general),
                           exempt_conditions=date.get(WorkDate.ATTR_EXEMPT_GRADE, None),
                           ) for date in dates_prefs[WorkDate.ATTR_SECTION]]
        return _dates

    @property
    def type_duty(self) -> Roles_Definition:
        return self._type_duty

    @type_duty.setter
    def type_duty(self, value):
        raise ValueError(self._MSG_SETTER_NOTALlOWED)

    @property
    def dates(self) -> List[WorkDate]:
        """
        @note The `WorkDate` instances returned is primarilly a requirement before it gets processed,
          thus may NOT contain the information updated during the application process.
        """
        return self._dates

    @dates.setter
    def dates(self, val: List[WorkDate]):
        self._dates = val

    @property
    def date_earliest(self) -> datetime.date:
        """
        @summary: The earliest date in the fiscal year, usually April 1st.
        """
        return self._date_earliest

    @date_earliest.setter
    def date_earliest(self, date_obj: datetime.date):
        if not isinstance(date_obj, datetime.date):
            raise TypeError(f"Type '{type(date_obj)=}' does not match.")
        self._date_earliest = date_obj

    @property
    def interval_assigneddates_leader(self):
        # TODO Haven't figured this out, but for some reason these getter methods were returning str.
        return int(self._interval_assigneddates_leader)

    @interval_assigneddates_leader.setter
    def interval_assigneddates_leader(self, val):
        raise ValueError(self._MSG_SETTER_NOTALlOWED)

    @property
    def interval_assigneddates_commitee(self):
        return int(self._interval_assigneddates_commitee)

    @interval_assigneddates_commitee.setter
    def interval_assigneddates_commitee(self, val):
        raise ValueError(self._MSG_SETTER_NOTALlOWED)

    @property
    def interval_assigneddates_general(self):
        return int(self._interval_assigneddates_general)

    @interval_assigneddates_general.setter
    def interval_assigneddates_general(self, val):
        raise ValueError(self._MSG_SETTER_NOTALlOWED)

    @property
    def num_leaders(self) -> int:
        return self._num_leaders

    @property
    def num_committee(self) -> int:
        return self._num_committee

    @property
    def num_general(self) -> int:
        return self._num_general

    @property
    def fiscal_year_start(self) -> int:
        return self._fiscal_year_start
