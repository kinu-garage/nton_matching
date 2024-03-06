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
from enum import Enum

from matching.players import Player


class PersonRole(Enum):
    LEADER = 1
    COMMITTEE = 2
    GENERAL = 3
    CHILD = 4


class PersonPlayer(Player):
    ATTR_ID = "id"
    ATTR_EMAIL = "email"
    ATTR_NAME = "name"
    ATTR_PHONE = "phone"
    ATTR_CHILDREN = "children"
    ATTR_ROLE_ID = "role_id"
    TYPE_OBLIGATION_LEADER = "leader"
    TYPE_OBLIGATION_COMMITEE = "commitee"
    TYPE_OBLIGATION_NONCOMMITEE = "non-commitee"

    def __init__(self,
                 name,
                 id,
                 email_addr,
                 phone_num,
                 role_id=PersonRole.GENERAL,
                 children_ids=[]):
       """
       @param role_id: Any of `GuardianRole` enum item.
       """
       super().__init__(name)  # For the rest of __init__, assigning `name` can be skipped because it's done in super class.
       self._id = id
       self.name = name
       self._email_addr = email_addr
       self._phone_num = phone_num
       self._role_id = role_id
       self._children_ids = children_ids
       self._last_assigned_date = None

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, val):
        raise AttributeError("`id` should only be settable as an initial input and cannot be overwritten.")

    @property
    def role_id(self):
        return self._role_id
    
    @role_id.setter
    def role_id(self, val):
        raise AttributeError("`role_id` should only be settable as an initial input and cannot be overwritten.")

    @property
    def last_assigned_date(self):
        """
        @rtype: datetime.date
        @return: None if not set.
        """
        return self._last_assigned_date

    @last_assigned_date.setter
    def last_assigned_date(self, d):
        """
        @type d: datetime.date
        """
        if not isinstance(d, date):
            raise TypeError(f"Input type must be 'datetime.date' but received '{type(d)}'")
        self._last_assigned_date = d


class PersonBank():
    def __init__(self, persons):
        """
        @type persons: [GuardianPlayer]
        @param persons: Input list will be converted as a dict.
        """
        persons_dict = {}
        for p in persons:
            persons_dict[p.id] = p
        self._persons = persons_dict
        self._max_allowance = None

    @property
    def persons(self):
        """
        @rtype dict
        """
        return self._persons

    @persons.setter
    def persons(self, val):
        raise AttributeError("`persons` is an initial raw input and cannot be overwritten.")

    def update_person(self, person):
        self.persons[person.id] = person                

    @property
    def max_allowance(self):
        """
        @return: A dict format returned by `max_allowed_days_per_person`
        """
        return self._max_allowance

    @max_allowance.setter
    def max_allowance(self, val):
        self._max_allowance = val
