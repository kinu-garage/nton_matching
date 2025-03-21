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

from abc import ABC, abstractmethod
from enum import IntEnum
from typing import List


class ResponsibilityLevel(IntEnum):
    """
    @summary: Reponsibility here is solely about "Touban" i.e. not applicable generically for any other kinds of "responsibility".
    """
    UNDEFINED = -1
    LEADER = 1  # 202408 Deprecated. There may not be many cases where someone in the input data is designated as a 'leader'.
    COMMITTEE = 2
    GENERAL = 3
    CHILD = 4
    TOUBAN_EXEMPT = 5


class Responsibility(ABC):
    def __init__(self, id: int=ResponsibilityLevel.GENERAL):
        self._id = id

    def __repr__(self):
        return self._id

    def __str__(self):
        return str(self._id)

    @abstractmethod
    def required_interval(self, requirements):
        raise NotImplementedError()

    @property
    def id(self) -> ResponsibilityLevel:
        return self._id

    #@id.setter
    #def id(self, val: ResponsibilityLevel):
    #    raise NotImplementedError("responsibility ID should not be settable after initialization.")

    @staticmethod 
    def str_responsibilities(responsibilities) -> str:
        """
        @type responsibilities: List[Responsibility]
        """
        _resps = []
        for r in responsibilities:
            _resps.append(str(r.id))
        _str_resps = ",".join(_resps) if _resps else "No responsibilities found."
        return _str_resps


class Leader(Responsibility):
    def __init__(self):
        super().__init__(ResponsibilityLevel.LEADER)
        # TODO Isn't a Leader also a Committeer?

    def required_interval(self, requirements):
        return requirements.interval_assigneddates_leader


class Committeer(Responsibility):
    def __init__(self):
        super().__init__(ResponsibilityLevel.COMMITTEE)

    def required_interval(self, requirements):
        return requirements.interval_assigneddates_commitee


class GenGuardian(Responsibility):
    def __init__(self):
        super().__init__(ResponsibilityLevel.GENERAL)

    def required_interval(self, requirements):
        return requirements.interval_assigneddates_general


class ToubanExempt(Responsibility):
    def __init__(self):
        super().__init__(ResponsibilityLevel.TOUBAN_EXEMPT)
        self._MSG_TITLE = "ToubanExempt"

    def _raise_error_exempt(self):
        raise RuntimeError(f"{self._MSG_TITLE} cannot be assigned any responsibility as it's exempted by definition.")

    def required_interval(self, requirements):
        self._raise_error_exempt()
