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

from n_to_n_matching.workdate_player import WorkDate

class Consts():
    ATTR_MAX_STINT_OPPORTUNITIES = "max_stint_opportunities"
    ATTR_AVAILABLE_EXTRAS = "num_available_extra"
    ATTR_UNLUCKY_PERSON_NUMS = "num_unlucky_person"    
    

class DateRequirement():
    _MSG_SETTER_NOTALlOWED = "The value is only allowed to be set upon initializing the instance."
    ATTR_SECTION = "Requirement"

    def __init__(self,
                 type_duty,
                 dates: List[WorkDate],
                 interval_assigneddates_leader=3,
                 interval_assigneddates_commitee=4,
                 interval_assigneddates_general=5):
        """
        @type type_match: `Roles_Definition` intenum.
        """
        self._type_duty = type_duty
        self._dates = dates
        self._interval_assigneddates_leader = interval_assigneddates_leader
        self._interval_assigneddates_commitee = interval_assigneddates_commitee
        self._interval_assigneddates_general = interval_assigneddates_general

    @property
    def type_duty(self):
        """
        @rtype type_match: `Roles_Definition` intenum.
        """
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
