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

from datetime import date

from matching.players import Player

from n_to_n_matching.util import Util


class WorkDate(Player):
    # Attiribute in text (e.g. .yaml) input file 
    ATTR_DATE = "date"
    ATTR_NUM_LEADER = "req_num_leader"
    ATTR_NUM_COMMITTEE = "req_num_commitee"
    ATTR_NUM_GENERAL = "req_num_general"
    ATTR_SCHOOL_OFF = "school_off"
    ATTR_LIST_ASSIGNED_LEADER = "assignees_leader"
    ATTR_LIST_ASSIGNED_COMMITTEE = "assignees_committee"
    ATTR_LIST_ASSIGNED_GENERAL = "assignees_general"

    def __init__(self,
                 datestr,
                 school_off=False,
                 req_num_committee=3,
                 req_num_leader=1,
                 req_num_noncommittee=2,
                 assignee_leader=None,
                 assignee_commitee=None,
                 assignee_noncommitee=None):
        """
        @param datestr: For now this needs to be "yyyy-mm-dd" format.
        @type assignees: [GuardianPlayer]
        @param assignee_ids_commitee: Can be empty when a class instantiates.
        """
        super().__init__(datestr)  # For the rest of __init__, assigning `name` can be skipped because it's done in super class.
        ##self.set_date(datestr)
        self._school_off = school_off
        self._req_num_leader = req_num_leader
        self._required_committee = req_num_committee
        self._required_noncommittee = req_num_noncommittee
        # Initializing list must not happen in the parameter section of
        # the constructor, which causes all instances referencing to the same
        # single instance of a list, which is mutable. See https://stackoverflow.com/questions/2757116/
        self._assignees_leader = assignee_leader if assignee_leader else []
        self._assignees = assignee_commitee if assignee_commitee else []
        self._assignees_noncommittee = assignee_noncommitee if assignee_noncommitee else []

    def set_date(self, datestr):
        Util.validate_date_str(datestr)
        ymd = datestr.split("-")
        year = int(ymd[0])
        month = int(ymd[1])
        day = int(ymd[2])
        self.name = date(year, month, day)

    @property
    def date(self):
        """
        @rtype datetime.date
        """
        return self.name

    @date.setter
    def date(self, val):
        self.set_date(val)

    @property
    def assignees_committee(self):
        return self._assignees

    @assignees_committee.setter
    def assignees_committee(self, val):
        self._assignees = val

    @property
    def assignees_noncommittee(self):
        return self._assignees_noncommittee

    @assignees_noncommittee.setter
    def assignees_noncommittee(self, val):
        self._assignees_noncommittee = val

    @property
    def assignees_leader(self):
        return self._assignees_leader

    @assignees_leader.setter
    def assignees_leader(self, val):
        self._assignees_leader = val

    @property
    def req_num_assignee_committee(self):
        return self._required_committee

    @property
    def req_num_assignee_noncommittee(self):
        return self._required_noncommittee

    @property
    def req_num_leader(self):
        return self._req_num_leader

    @property
    def school_off(self):
        return self._school_off
