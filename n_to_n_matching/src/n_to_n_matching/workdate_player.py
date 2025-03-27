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
from typing import List, Tuple

from matching.players import Player

from gj.grade_class import GjGrade
from gj.responsibility import Responsibility
from gj.responsibility import ResponsibilityLevel as RespLvl
from n_to_n_matching.person_player import PersonPlayer
from n_to_n_matching.util import Util


class WorkDate(Player):
    """
    @summary: Describes the requirement for a single day.
    """
    # Attiribute in text (e.g. .yaml) input file 
    ATTR_SECTION = "Dates"  # Key in the input file.
    ATTR_DATE = "date"
    ATTR_NUM_LEADER = "req_num_leader"
    ATTR_NUM_COMMITTEE = "req_num_commitee"
    ATTR_NUM_GENERAL = "req_num_general"
    ATTR_SCHOOL_OFF = "school_off"
    ATTR_LIST_ASSIGNED_LEADER = "assignees_leader"
    ATTR_LIST_ASSIGNED_COMMITTEE = "assignees_committee"
    ATTR_LIST_ASSIGNED_GENERAL = "assignees_general"
    ATTR_DUTY_TYPE = "duty_type"
    ATTR_EXEMPT_GRADE = "exempted_grade"

    REQ_INTERVAL_ASSIGNEDDATES_LEADER = "req_interval_assigneddates_leader"
    REQ_INTERVAL_ASSIGNEDDATES_COMMITTE = "req_interval_assigneddates_commitee"
    REQ_INTERVAL_ASSIGNEDDATES_GENERAL = "req_interval_assigneddates_general"
    DEFAULT_PERDAY_LEADER = 1
    DEFAULT_PERDAY_COMMITTEE = 2
    DEFAULT_PERDAY_GENERAL = 1
    
    def __init__(self,
                 datestr,
                 school_off=False,
                 req_num_committee=2,
                 req_num_leader=1,
                 req_num_noncommittee=1,
                 assignee_leader: List[PersonPlayer]=None,
                 assignee_commitee: List[PersonPlayer]=None,
                 assignee_noncommitee: List[PersonPlayer]=None,
                 exempt_conditions: List[GjGrade]=None):
        """
        @param datestr: For now this needs to be "yyyy-mm-dd" format.
        @type assignees: [PersonPlayer] TBD this no longer exists?
        """
        super().__init__(datestr)
        # type: datetime.date
        # For date information, this `_date_obj` instance (accessible via `date()`) should be prioritized, instead of `super.name`.
        self._date_obj = None
        self._date = self.name

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
        self._exempt_conditions = exempt_conditions

    def set_date(self, datestr):
        """
        @param datestr: Format of "yyyy-mm-dd" is required.
        @raise ValueError: When `datestr` format is not appropriate.
        """
        Util.validate_date_str(datestr)
        ymd = datestr.split("-")
        year = int(ymd[0])
        month = int(ymd[1])
        day = int(ymd[2])
        self._date_obj = date(year, month, day)

    @property
    def date(self):
        """
        @rtype datetime.date
        """
        return self._date_obj

    @date.setter
    def _date(self, val):
        """
        @
        """
        self.set_date(val)

    @property
    def assignees_committee(self):
        return self._assignees

    def assignee_committee(self, val: PersonPlayer):
        self._assignees.append(val)

    @property
    def assignees_noncommittee(self):
        return self._assignees_noncommittee

    def assignee_noncommittee(self, val: PersonPlayer):
        self._assignees_noncommittee.append(val)

    @property
    def assignees_leader(self: List[PersonPlayer]):
        return self._assignees_leader

    def assignee_leader(self, val: PersonPlayer):
        self._assignees_leader.append(val)

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

    def get_required_persons(self) -> Tuple[int, int, int]:
        needed_leader, needed_committee, needed_general = 0, 0, 0
        needed_leader += self.req_num_leader
        needed_committee += self.req_num_assignee_committee
        needed_general += self.req_num_assignee_noncommittee
        return needed_leader, needed_committee, needed_general

    def get_current_assignednum(self):
        """
        @rtype: int
        """
        return len(self.assignees_leader) + len(self.assignees_committee) + len(self.assignees_noncommittee)

    def eval_enough_assignees(self) -> Tuple[bool, bool, bool]:
        """
        @deprecated: Recommended to use PersonPlayer._eval_enough_assignees instead.
        @summary Returns eval result if a given `date` has enough numbers of assignees.
            
        @type date: n_to_n_matching.WorkDate
        @rtype: bool, bool, bool
        @return: Return 3 boolean values of:
            1. True/False whether the number of retval-1 meets the requirement.
            2. True/False whether the number of retval-2 meets the requirement.            
        """
        _enough_leaders = len(self.assignees_leader) == self.req_num_leader
        _enough_committee = len(self.assignees_committee) == self.req_num_assignee_committee
        _enough_noncommittee = len(self.assignees_noncommittee) == self.req_num_assignee_noncommittee
        return _enough_leaders, _enough_committee, _enough_noncommittee

    def assign_responsibility(self, responsibility: Responsibility, player: PersonPlayer):
        if responsibility == RespLvl.LEADER.value:
            self.assignee_leader(player)
        elif responsibility == RespLvl.COMMITTEE.value:
            self.assignee_committee(player)
        elif responsibility == RespLvl.GENERAL.value:
            self.assignee_noncommittee(player)
        else:
            raise ValueError(f"Rresponsibility: {responsibility=} not recognized")

    def eval_enough_assignees(self, responsibility: Responsibility) -> bool:
        if responsibility == RespLvl.LEADER.value:
            return len(self.assignees_leader) == self.req_num_leader
        elif responsibility == RespLvl.COMMITTEE.value:
            return len(self.assignees_committee) == self.req_num_assignee_committee
        elif responsibility == RespLvl.GENERAL.value:
            return len(self.assignees_noncommittee) == self.req_num_assignee_noncommittee
        else:
            raise ValueError(f"Rresponsibility: {responsibility=} not recognized")

    def eval_enough_assignees_all(self) -> Tuple[bool, bool, bool]:
        _len_leaders = self.eval_enough_assignees(RespLvl.LEADER)
        _len_committees = self.eval_enough_assignees(RespLvl.COMMITTEE)
        _len_general = self.eval_enough_assignees(RespLvl.GENERAL)
        return _len_leaders, _len_committees, _len_general
        
    def total_assignees_num(self) -> int:
        return len(self.assignees_leader) + len(self.assignees_committee) + len(self.assignees_noncommittee)

    @property
    def exempt_conditions(self) -> List[GjGrade]:
        return self._exempt_conditions
