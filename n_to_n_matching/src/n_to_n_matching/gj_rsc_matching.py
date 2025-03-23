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

import logging
from typing import List

from matching import ManyToManyMatching

from n_to_n_matching.util import Util
from n_to_n_matching.workdate_player import WorkDate


class GjVolunteerMatching(ManyToManyMatching):
    """
    @todo Consider optimizing and move code back to upstream as much
    """
    _KEY_DATE = "date"
    _KEY_PERSON_ID = "person_id"
    _KEY_responsibility_id = "responsibility_id"

    def __init__(self, dates_lgtm, dates_failed, person_bank=None, max_allowance=None):
        """
        @type dates_lgtm: dict
        @param dates_lgtm: needs the following keys:
           - "date"
           - "guardian_id"
           - "responsibility_id"
        @type dates_failed: dict
        @type person_bank: PersonBank
        @type max_allowance: dict  (What `GjVolunteerAllocationGame.max_allowed_days_per_person` returns.)
        """
        super().__init__(
            GjVolunteerMatching.dates_list_to_dict(dates_lgtm))
        # Validate the dict: Error if the `dictionary` doesn't have expected keys.

        # Custom attributes
        self._person_bank = person_bank
        ## Keeping _dates_list as a member variable is redundant as 
        ## the same info converted to a Python's dict is stored in the
        ## parent class. However, by the conversion to dict, convenience of
        ## data access is lost. So for now, just as a convenience this list
        ## version of an instance that contains `WorkDate` instances is also retained.
        ## TODO In future this should better be refactored to remove redundancy.
        self._dates_lgtm = dates_lgtm
        self._dates_failed = dates_failed
        self._max_allowance = max_allowance

    def add_item(self, new_match):
        self._dataframe.append(new_match)

    @property
    def dates_lgtm(self):
        return self._dates_lgtm

    @dates_lgtm.setter
    def dates_lgtm(self, val):
        raise ValueError("This data must only be set upon initializing this class.")

    @property
    def dates_failed(self):
        return self._dates_failed

    @dates_failed.setter
    def dates_failed(self, val):
        raise ValueError("This data must only be set upon initializing this class.")

    @property
    def person_bank(self):
        return self._person_bank

    @person_bank.setter
    def person_bank(self, val):
        self._person_bank = val

    @property
    def max_allowance(self):
        return self._max_allowance

    @max_allowance.setter
    def max_allowance(self, val):
        self._max_allowance = val

    @staticmethod
    def dates_list_to_dict(list_dates: List[WorkDate]):
        """
        @rtype: dict
        @return: Example format:
           {
             "str": {
                WorkDate.ATTR_DATE: str,
                WorkDate.ATTR_LIST_ASSIGNED_LEADER: [PersonPlayer],
                WorkDate.ATTR_LIST_ASSIGNED_COMMITTEE: [PersonPlayer],
                WorkDate.ATTR_LIST_ASSIGNED_GENERAL: [PersonPlayer],
                WorkDate.ATTR_NUM_LEADER: int,
                WorkDate.ATTR_NUM_COMMITTEE: int,
                WorkDate.ATTR_NUM_GENERAL: int,
                WorkDate.ATTR_SCHOOL_OFF: bool,
              }
           }
        """
        dict_dates = {}
        if not list_dates:
            raise ValueError("Arg `list_dates` must not be empty")
        for date in list_dates:
            date_dict = {
                WorkDate.ATTR_DATE: date.name,  # `WorkDate(name)` represents the date in `str` format.
                WorkDate.ATTR_LIST_ASSIGNED_LEADER: date.assignees_leader,
                WorkDate.ATTR_LIST_ASSIGNED_COMMITTEE: date.assignees_committee,
                WorkDate.ATTR_LIST_ASSIGNED_GENERAL: date.assignees_noncommittee,
                WorkDate.ATTR_NUM_LEADER: date.req_num_leader,
                WorkDate.ATTR_NUM_COMMITTEE: date.req_num_assignee_committee,
                WorkDate.ATTR_NUM_GENERAL: date.req_num_assignee_noncommittee,
                WorkDate.ATTR_SCHOOL_OFF: date.school_off
            }
            dict_dates[date.name] = date_dict
        return dict_dates
