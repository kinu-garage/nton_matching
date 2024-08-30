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
from enum import IntEnum
import logging
from typing import Dict, List

from matching.players import Player

from gj.assigned_date import AssignedDate
from gj.requirements import DateRequirement
from gj.responsibility import Responsibility
from gj.responsibility import ResponsibilityLevel as RespLvl
from gj.role import Role
from n_to_n_matching.util import Util as NtonUtil


class PersonPlayer(Player):
    ATTR_ID = "id"
    ATTR_CHILDREN = "children"
    ATTR_EMAIL = "email"
    ATTR_NAME = "name"
    ATTR_PHONE = "phone"
    ATTR_ROLE_ID = "role_id"
    ATTR_responsibility_id = "responsibility_id"  # Not sure why lower case is used.

    _ERRMSG_SHOULD_NOT_OVERWRITE = "`{}` should only be settable as an initial input and cannot be overwritten."

    def __init__(self,
                 name,
                 id,
                 email_addr,
                 phone_num,
                 responsibilities: List[Responsibility],
                 children_ids=[],
                 roles: List[Role]=[Role()],
                 logger_obj: logging.Logger=None,
                 assigned_dates: List[AssignedDate]=[]):
        """
        @param responsibility_id: Any of `ResponsibilityLevel` enum item.
        @param role_id: -1 is equal to a role ID not being set. Roles are e.g gakyu/library/safety etc.
        """
        super().__init__(name)  # For the rest of __init__, assigning `name` can be skipped because it's done in super class.
        if not isinstance(id, int):
            raise ValueError(f"'id' must be int. Got {type(id)}")
        if not isinstance(responsibilities, list):
            raise ValueError(f"'responsibility_ids' must be list. Got {type(responsibilities)}")
        if not logger_obj:
            logger_obj = self._logger = NtonUtil.get_logger(__name__)
        self._logger = logger_obj
            
        self._id = id
        self.name = name
        self._email_addr = email_addr
        self._phone_num = phone_num
        self._children_ids = children_ids

        self._last_assigned_date_general = None
        self._last_assigned_date_committee = None
        self._last_assigned_date_leader = None

        #if (roles) and not (len(roles) == 1 and Roles_Definition.UNDEFINED in roles):
        self._roles = roles

        self._responsibilities = responsibilities
        self._assigned_dates = assigned_dates

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, val):
        raise AttributeError(self._ERRMSG_SHOULD_NOT_OVERWRITE.format("id"))

    @property
    def assigned_dates(self):
        return self._assigned_dates
    
    @assigned_dates.setter
    def assigned_dates(self, val: List[AssignedDate]):
        """
        @deprecated: Existing values will be overwritten without any warning.
        """
        self._assigned_dates = val

    def assigned_date(self, val: AssignedDate):
        self._assigned_dates.append(val)

    @property
    def roles(self) -> List[Role]:
        return self._roles
    
    @roles.setter
    def roles(self, val: List[Role]):
        """
        @deprecated: Existing values get overwritten, hence not recommended.
        """
        self._roles = val

    def add_role(self, val: Role):
        if not val in self._roles:
            self._roles.append(val)
        else:
            raise ValueError(f"ID '{self.id}' already has '{val}' as a role.")

    @property
    def responsibilities(self) -> List[Responsibility]:
        return self._responsibilities
    
    @responsibilities.setter
    def responsibilities(self, val: Responsibility):
        # TODO Reject if the same responsibility already registered.

        self._responsibilities.append(val)

    @property
    def last_assigned_date(self, responsibility: Responsibility=None) -> AssignedDate:
        """
        @return: 
           - None if not set.
           - If `responsibility` is NOT set, return the most recent date.
           - If `responsibility` is set, return the date with the corresponding `responsibility`.
        """
        _last_date = None
        if not responsibility:
            last_dates = [self._last_assigned_date_general,
                          self._last_assigned_date_committee,
                          self._last_assigned_date_leader]
            try:
                _last_date = max(last_dates)
            except TypeError as e:
                # More than one entry in `last_dates` is not set yet.
                _last_date = None
        else:
            if responsibility.id == RespLvl.COMMITTEE:
                _last_date = self._last_assigned_date_committee
            elif responsibility.id == RespLvl.LEADER:
                _last_date = self._last_assigned_date_leader
            else:
                _last_date = self._last_assigned_date_general
        return _last_date

    @last_assigned_date.setter
    def last_assigned_date(self, d: AssignedDate):
        if not isinstance(d, AssignedDate):
            raise TypeError(f"Input type must be `gj.assigned_date.AssignedDate` but received '{type(d)}'")

        if d.responsibility == RespLvl.COMMITTEE:
            self._last_assigned_date_committee = d
        elif d.responsibility == RespLvl.LEADER:
            self._last_assigned_date_leader = d
        else:
            self._last_assigned_date_general = d

    @staticmethod
    def get_responsibility(responsibility_level: RespLvl, responsibilities: List[Responsibility], logger: logging.Logger) -> Responsibility:
        for resp in responsibilities:
            if resp.id == responsibility_level:
                logger.info(f"'{resp.id=}', type of resp obj= {type(resp)} found in the player's responsibility set.")
                return resp
        raise ValueError(f"Requested responsibility level {responsibility_level} is not found in the passed set of {responsibilities=}.")

    def assign_myself(self, date_assigned: AssignedDate, requirements):
        """
        @summary Set the assigned status on itself
        @todo Rename appropriately esp. there are other methods that have similar names.
        @raise ValueError:
          - Case-a. When the requirement is not met (e.g. too soon for `person` to be assigned since her/his last assignment).
          - Case-b. (TODO needs figured out this case, which is also clarified in the inline comment section of the corresponding line.)
        """
        # Screening
        if not self.responsibilities:
            raise RuntimeError(f"'responsibilities', which should've been set during initialization, is empty.")
        if not requirements:
            self._logger.warning("Requirement was not passed. Using default.")
            requirements = DateRequirement()        
        if not isinstance(date_assigned, AssignedDate):
            raise TypeError(f"Type is incompatible. date: '{type(AssignedDate)}'")

        self.assigned_date(date_assigned)
        self.last_assigned_date = date_assigned
        #self._log_dates("116 Memory addr of date.assignees_leader: {}".format(id(date_assigned.assignees_leader)))


class PersonBank():
    def __init__(self, persons):
        """
        @type persons: [PersonPlayer]
        @param persons: Input list will be converted as a dict.
        """
        self._persons = {}
        for p in persons:
            self._persons[p.id] = p
        self._max_allowance = None

    @property
    def persons(self) -> Dict[int, PersonPlayer]:
        return self._persons

    @persons.setter
    def persons(self, val):
        raise AttributeError("`persons` is an initial raw input and cannot be overwritten.")

    def update_person(self, person):
        self.persons[person.id] = person                

    @property
    def max_allowance(self) -> Dict[str, Dict[str, int]]:
        """
        @return: A dict format returned by `GjVolunteerAllocationGame.max_allowed_days_per_person`
        """
        return self._max_allowance

    @max_allowance.setter
    def max_allowance(self, val: Dict[str, Dict[str, int]]):
        """
        @type: dict format returned by `GjVolunteerAllocationGame.max_allowed_days_per_person`
        """
        self._max_allowance = val
