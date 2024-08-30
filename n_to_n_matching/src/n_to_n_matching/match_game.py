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

import copy
import logging
import random
from typing import Dict, List, Tuple

from matching import BaseGame
from matching.exceptions import PlayerExcludedWarning

from gj.responsibility import Responsibility, ResponsibilityLevel
from gj.requirements import DateRequirement
from gj.role import Role, Roles_Definition
from gj.util import GjUtil
from n_to_n_matching.gj_rsc_matching import GjVolunteerMatching
from n_to_n_matching.person_player import (AssignedDate,
                                           PersonBank,
                                           PersonPlayer)
from n_to_n_matching.workdate_player import WorkDate


class GjVolunteerAllocationGame(BaseGame):
    DATES = "dates"
    WORKERS = "workers"

    def __init__(self, dates, persons, requirements: DateRequirement=None, clean=False, logger_obj=None):
        """
        @type persons: PersonBank
        @param persons: Will be converted to `PersonBank` class instance.
        @type requirements: DateRequirement
        """
        super().__init__(clean)
        self._dates = dates
        self._person_bank = persons
        self._reqs = requirements
        self._check_inputs()

        if not logger_obj:
            logger_obj = GjUtil.get_logger()
        self._logger = GjUtil.get_logger(__name__, logger_obj)

    @classmethod
    def print_tabular_stdout(cls, solution):
        """
        @type solution: n_to_n_matching.gj_rsc_matching.GjVolunteerMatching
        """
        _heading = "Result"
        _heading_dates_lgtm = "Dates filled"
        _heading_dates_failed = "Dates not-filled"
        print(f"{_heading:*^40}")  # TODO Using `print`..?
        print(f"Max allowance: {solution.max_allowance}")

        for person_id, person_obj in solution.person_bank.persons.items():
            num_assigned_dates, num_assigned_leader, num_assigned_committee, num_assigned_noncommittee = GjUtil.get_assigned_dates(
                person_id, solution.dates_lgtm)
            print(f"P-ID {person_id}, responsibility: {Responsibility.str_responsibilities(person_obj.responsibilities)}, #assigned date: {num_assigned_dates}")
        print(f"{_heading_dates_lgtm:O^40}")
        for date, date_detail in solution.items():
            print(f"{date}\n\tLeader: {date_detail[WorkDate.ATTR_LIST_ASSIGNED_LEADER]}\n\t",
                  f"Commitee assignee: {date_detail[WorkDate.ATTR_LIST_ASSIGNED_COMMITTEE]}\n\t",
                  f"General assignee: {date_detail[WorkDate.ATTR_LIST_ASSIGNED_GENERAL]}")
        print(f"{_heading_dates_failed:x^40}")
        for date in solution.dates_failed:
            print(f"{date.date}\n\tLeader: {date.assignees_leader}\n\t",
                  f"Commitee assignee: {date.assignees_committee}\n\t",
                  f"General assignee: {date.assignees_noncommittee}")

    def _check_inputs(self):
        """
        @see Hospital Residents https://daffidwilde.github.io/matching/docs/tutorials/hospital_resident.html
        @description: Check if any rules of the game have been broken.
                Any violations will be flagged as warnings. If the ``clean``
                attribute is in use, then any violations will be removed.
        """
        # This app doesn't require prefs so I'm not sure if calling these
        # is needed but will give it a try for now.
        # 20240207 Ok for now commenting these out.
        #self._check_inputs_player_prefs_unique(self.DATES)
        #self._check_inputs_player_prefs_unique(self.WORKERS)
        #self._check_inputs_player_capacity(self.DATES, self.WORKERS)
        pass

    def _check_inputs_player_capacity(self, party, other_party):
        """
        @see Hospital Residents https://daffidwilde.github.io/matching/docs/tutorials/hospital_resident.html
        @description Check everyone has a capacity of at least one."""

        for player in vars(self)[party]:
            if player.capacity < 1:
                warnings.warn(PlayerExcludedWarning(player))

                if self.clean:
                    self._remove_player(player, party, other_party)

    def _log_dates(self, msg_prefix= "", dates=None):
        if not dates:
            dates = self._dates
        for d in dates:
            self._log_date_content(d, msg_prefix="f{msg_prefix}: ")

    def find_dates_need_attention(self, dates):
        """
        @summary Split the input `dates` into 2 sets, one that needs attention and the others don't.
        @type dates: [WorkDate]
        @rtype: [WorkDate], 
        """
        dates_attention = []
        dates_lgtm = []
        for date in dates:
            _enough_leaders, _enough_committee, _enough_noncommittee = date.eval_enough_assignees_all()
            if all([_enough_leaders, _enough_committee, _enough_noncommittee]):
                dates_lgtm.append(date)
            else:
                dates_attention.append(date)
        for date_attention in dates_attention:
            self._log_date_content(date_attention, "date_attention")
        for date_lgtm in dates_lgtm:
            self._log_date_content(date_lgtm, "date_lgtm")
        self._logger.info(f"{dates_attention =}\n{dates_lgtm =}")
        return dates_attention, dates_lgtm

    def assign_responsibility(
        self,
        date_wd: WorkDate,
        person: PersonPlayer,
        responsibility: Responsibility,
        req_space_days: int,
        requirements: DateRequirement=None):
        """
        @type responsibility: A specific element in `RespLvl`
        @todo Rename appropriately esp. there are other methods that have similar names.
        @raise ValueError:
          - Case-a. When the requirement is not met (e.g. too soon for `person` to be assigned since her/his last assignment).
          - Case-b. (TODO needs figured out this case, which is also clarified in the inline comment section of the corresponding line.)
        """
        # BEGIN: Init screening
        if not requirements:
            self._logger.warning("Requirement was not passed. Using default.")
            requirements = DateRequirement()        
        if (not isinstance(person, PersonPlayer)) or (not isinstance(date_wd, WorkDate)):
            raise TypeError(f"One of the args' type is incompatible. person: '{type(person)}', date_wd: '{type(WorkDate)}'")
        # If the previous assigned date is closer than what's in the requirement, this person cannot be assigned.
        # END: Init screening

        # If `person.last_assigned_date` is None, it's set to the same date as `date_wd`
        # (so the `days_interval` will be 0).
        _last_assigned_date = person.last_assigned_date if person.last_assigned_date else None
        days_interval = (date_wd.date - _last_assigned_date.date).days if _last_assigned_date else 9999  # Setting arbitrarily impossibly large interval
        self._logger.warning(f"**Assigning responsibility** {person.id=}: {person.last_assigned_date=}, {date_wd.date=}, {responsibility=}, {req_space_days=}, {days_interval=}")
        if days_interval <= req_space_days:
            raise ValueError(f"""
                             Can't assign the person (ID={self.responsibility_id}) on {date_assigned} as this person must wait for {req_space_days} days
                              since the last assignment on {_last_assigned_date}.""")

        _enough_leaders, _enough_committee, _enough_noncommittee = date_wd.eval_enough_assignees_all()
        if all([_enough_leaders, _enough_committee, _enough_noncommittee]):
            return  # TODO Think of better return value to communicate the result
        elif (not _enough_leaders) and (responsibility == ResponsibilityLevel.LEADER.value):
            date_wd.assignee_leader(person)
        elif (not _enough_committee) and (responsibility == ResponsibilityLevel.COMMITTEE.value):
            date_wd.assignee_committee(person)
        elif (not _enough_noncommittee) and (responsibility == ResponsibilityLevel.GENERAL.value):
            date_wd.assignee_noncommittee(person)
        else:
            raise ValueError(f"Not assigning '{person}' ID={person.id} as the needs didn't match the responsibilities.  \
Responsibilities: {Responsibility.str_responsibilities(person.responsibilities)}, roles: {person.roles}. {_enough_leaders=}, {_enough_committee=}, {_enough_noncommittee=}")

        date_assigned = AssignedDate(date_wd.date, responsibility)
        person.assign_myself(date_assigned, requirements)

        self._log_dates("116 Memory addr of date.assignees_leader: {}".format(id(date_wd.assignees_leader)))

    def _assign_day_per_responsibility(self,
            date: WorkDate,
            person_bank: PersonBank,
            requirements: DateRequirement,
            responsibility_id,
            req_space_days: int,
            overbook: bool=False) -> WorkDate:
        """
        @summary: 
          Internally in this method, the list of available persons get randomized,
          in order to help distributing the assigned dates of each person.
        @type responsibility_id: A specific element in `RespLvl`
        @param overbook: If True, this method tries to add a booking to the person who has already been fully booked.
        """
        if not person_bank.persons:
            raise ValueError("There's no pool of persons in the arg.")

        # TODO 20250305 Should call `find_free_workers` per each resplvl
        _free_ppl, _fullybooked_ppl, overbooked_ppl = GjUtil.find_free_workers_per_responsibility(
            responsibility_id,
            # TODO The method being called here takes a collection of dates objs,
            # while a singular date is passed to this method. I guess this "smells"...
            self._dates,
            person_bank,
            logger=self._logger)
        _persons = _free_ppl
        if overbook:
            self._logger.warning(f"Overbooking is triggered.:=^20")
            _persons = copy.deepcopy(_fullybooked_ppl)

        _persons_randomized = sorted(_persons, key=lambda x: random.random())
        for person in _persons_randomized:
            try:
                # TODO 20250305 Should call `assign_responsibility` per each resplvl
                self.assign_responsibility(date, person, responsibility_id, req_space_days, requirements)
            except ValueError as e:
                self._logger.warning(f"Error received: {str(e)}. Skipping {person.id =}, continuing.")
                continue
        return date

    def _assign_day(self,
            date: WorkDate,
            person_bank: PersonBank,
            requirements: DateRequirement,
            overbook: bool=False) -> WorkDate:
        """
        @summry: Assigning a person on a single day, for which ALL the responsibilities required.
          TBD Clarify if the all required slots per responsibility for the day are filled by this or not.
        """
        req_responsibilities = []
                
        if requirements.type_duty == Roles_Definition.TOSHO_COMMITEE:
            req_responsibilities = [ResponsibilityLevel.GENERAL, ResponsibilityLevel.COMMITTEE, ResponsibilityLevel.LEADER]
        elif requirements.type_duty == Roles_Definition.SAFETY_COMMITEE:
            req_responsibilities = [ResponsibilityLevel.GENERAL, ResponsibilityLevel.LEADER]
        else:
            raise ValueError(f"{requirements.type_duty=} were not identified. Returning.")

        for resp in req_responsibilities:
            # Maybe a bit unintuitive but passing a value via enum subclass is a valid way to access
            # a value of a member of an enum class https://realpython.com/python-enum/#accessing-enumeration-members
            req_space_days = -1
            if (resp == ResponsibilityLevel.LEADER.value):
                req_space_days = requirements.interval_assigneddates_leader
            elif (resp == ResponsibilityLevel.COMMITTEE.value):
                req_space_days = requirements.interval_assigneddates_commitee
            elif (resp == ResponsibilityLevel.GENERAL.value):
                req_space_days = requirements.interval_assigneddates_general
            else:
                raise RuntimeError(f"{resp =} is out of scope of handling.")

            self._logger.info(f"{date=}, responsibility={resp}, {req_space_days=}, {overbook=}")
            date = self._assign_day_per_responsibility(date, person_bank, requirements, resp, req_space_days, overbook)
        return date

    def assign_person(self, 
                      date: WorkDate,
                      person_bank: PersonBank,
                      requirements: DateRequirement=None,
                      overbook=True):
        """
        @summary: Assign a person taken from the `person_bank` obj. The status of assignment is kept tracked in
          `person_bank` obj. 

          Types of some stuff (TBD)
          - `free_workers`: the same instance as the input arg but with potentially one element popped out.
          - `booked_persons`: the same instance as the input arg but with potentially one element appended.
          - `overlybooked_workers`: f

          Also, `date` is NOT returned explicitly, but potentially its `assignee_ids_{commitee, noncommitee}` field is updated.
        @param overbook: Naming may not be appropriate so want a better one. When True, TBD
        """
        self._logger.info(f"Began assigning {date.date =}")
        if not requirements:
            self._logger.warning("Requirement was not passed. Using default.")
            requirements = DateRequirement()

        # Assign a personnel taken from `free_workers`. Once done, update the `free_workers`.
        date = self._assign_day(date, person_bank, requirements)

        # Once evaluated all `free_workers` and yet the date is not filled with needed number of persons,
        # use `ATTR_UNLUCKY_PERSON_NUMS` persons.
        _enough_leaders, _enough_committee, _enough_noncommittee = date.eval_enough_assignees_all()
        if not all([_enough_leaders, _enough_committee, _enough_noncommittee]):
            date = self._assign_day(date, person_bank, requirements, overbook=True)

    def _log_date_content(self, date, msg_prefix=""):
        self._logger.info(f"{msg_prefix} Date={date.date} assignees stored. Leader: {date.assignees_leader}, Committee: {date.assignees_committee}, Non-commitee: {date.assignees_noncommittee}")

    def match(self, dates, person_bank, requirements=None, optimal=""):
        """
        @type dates: [n_to_n_matching.WorkDate]
        @type person_bank: n_to_n_matching.PersonBank
        @type reqs: DateRequirement
        @param optimal: Unused for now, kept just to make it consistent with `matching` pkg.
        @return 
        @raise ValueError: If the given `dates` already filled with assignees.
        """
        self._logger.info(f"{requirements.interval_assigneddates_leader = }, {requirements.interval_assigneddates_commitee = }, {requirements.interval_assigneddates_general = }")
        if not requirements:
            self._logger.warning("Requirement was not passed. Using default.")
            requirements = DateRequirement()

        dates_need_attention = []

        # Figure out how many dates each worker can be assigned to for the given `dates`.
        # ? 20240207 These vars are not used
        #_max_daily_committee_perperson, _max_daily_noncommittee_perperson = self.max_per_given_period(dates, workers)
        #_max_daily_all = _max_daily_committee_perperson + _max_daily_noncommittee_perperson

        # BEGIN: Initial screening
        ## See if there's any date where 1 or more assignees are needed.
        dates_need_attention, dates_lgtm = self.find_dates_need_attention(dates)
        if not dates_need_attention:
            # There's no date where an assignee is missing.
            raise ValueError("The input `dates` have all slots filled already, which typically means you're good.")
        ## Ok, there are some dates that need assignees.
        ## Determine the maximum #days each person can be assigned to.
        person_bank = GjUtil.max_allowed_days_per_person(dates, person_bank)
        # END: Initial screening

        # Assign personnels per date
        for date in dates_need_attention:
            self._log_date_content(date, msg_prefix="BEFORE assigning:")
            _assignednum_before = date.get_current_assignednum()
            self.assign_person(date, person_bank, requirements)
            _assignednum_after = date.get_current_assignednum()
            if (_assignednum_before < _assignednum_after):
                dates_lgtm.append(date)
            #dates_need_attention.remove(date)
            self._log_date_content(date, msg_prefix="AFTER assigning a day:")
            self._logger.info(f"AFTER assigning a day: All dates_need_attention={dates_need_attention}\n\tdates_lgtm={dates_lgtm}")
        rest_dates_need_attention = list(set(dates_need_attention).difference(dates_lgtm))
        return dates_lgtm, rest_dates_need_attention

    def solve(self, optimal=""):
        """
        @description: 
        @return `GjVolunteerMatching`
        """
        if not self._logger:
            # Not ideal workaround of __init__ being bypassed...
            logger_obj = GjUtil.get_logger()
            self._logger = GjUtil.get_logger(__name__, logger_obj)

        dates_lgtm, dates_failed = self.match(self._dates, self._person_bank, self._reqs, optimal)
        self._matching = GjVolunteerMatching(
            dates_lgtm,
            dates_failed,
            self._person_bank,
            self._person_bank.max_allowance
        )
        return self._matching

    @classmethod
    def create_from_dict_dates(
        cls, dates_prefs, clean=False, logger_obj: logging.Logger=None) -> Tuple[List[WorkDate], DateRequirement]:
        """
        @summary: Input data converter from text-based (dictionary in .yaml) format to Python format.
          Only required attribute in each element in `dates_prefs` is `date` (i.e. other attributes are optional).
        @type dates_prefs: [{}]
        @param dates_prefs: e.g. 
            [
                { "date": "2024-04-06", 
                  "school_off": True, },
                { "date": "2024-04-13",
                  "num_leader": 1,
                  "num_commitee": 2,
                  "num_general": 3, },
                { "date": "2024-04-20", },
                { "date": "2024-04-27", }
            ]
        @raise ValueError
        """
        if not logger_obj:
            logger_obj = GjUtil.get_logger()
        if WorkDate.ATTR_SECTION not in dates_prefs:
            raise ValueError(f"A required section '{WorkDate.ATTR_SECTION}' in the input file is missing.")

        logger_obj.info(f"{dates_prefs = }")
        # If date requirement is included in the input.
        if DateRequirement.ATTR_SECTION in dates_prefs:
            dates_dict = dates_prefs[DateRequirement.ATTR_SECTION]
            requirement = DateRequirement(
                dates_dict.get(WorkDate.ATTR_DUTY_TYPE, Roles_Definition.TOSHO_COMMITEE),
                dates_dict.get(WorkDate.REQ_INTERVAL_ASSIGNEDDATES_LEADER, -1),
                dates_dict.get(WorkDate.REQ_INTERVAL_ASSIGNEDDATES_COMMITTE, -1),
                dates_dict.get(WorkDate.REQ_INTERVAL_ASSIGNEDDATES_GENERAL, -1),
            )
        else:
            logger_obj.warning(f"Requirement is missing. Moving on with default value.")
            requirement = DateRequirement()

        _dates = [WorkDate(datestr=d[WorkDate.ATTR_DATE],
                           school_off=d.get(WorkDate.ATTR_SCHOOL_OFF, False),
                           req_num_leader=d.get(WorkDate.ATTR_NUM_LEADER, 1),
                           req_num_committee=d.get(WorkDate.ATTR_NUM_COMMITTEE, 2),
                           req_num_noncommittee=d.get(WorkDate.ATTR_NUM_GENERAL, 3)
                           ) for d in dates_prefs[WorkDate.ATTR_SECTION]]
        # Find the earliest date in the given dates in order for that date to be the beginning of the given period.
        _date_earliest = min(date.date for date in _dates)
        requirement.date_earliest = _date_earliest

        return _dates, requirement

    @classmethod
    def create_from_dict_persons(cls, person_prefs, clean=False) -> List[PersonPlayer]:
        """
        @summary: Input data converter from text-based (dictionary in .yaml) format to Python format.
        @type personnel_prefs: [{ "id", "name", "phone", "email", "children": {"child_id"}, "responsibility_id" }]
        @rtype: [PersonPlayer]
        """
        _persons = []
        for p in person_prefs:
            #a_role = Role(Roles_Definition.TOSHO_COMMITEE)  # TODO This assign ALL entries as Tosho, which is not realistic. Doing so just as a quick test for now.
            try:
                a_role = p[PersonPlayer.ATTR_ROLE_ID]
            except KeyError as e:
                a_role = None
            #_responsibility_id = p.get(PersonPlayer.ATTR_responsibility_id, ResponsibilityLevel.GENERAL)
            _responsibility = GjUtil.corresponding_responsibility(a_role)
            person = PersonPlayer(
                id=p[PersonPlayer.ATTR_ID],
                name=p[PersonPlayer.ATTR_NAME],
                email_addr = p[PersonPlayer.ATTR_EMAIL],
                phone_num = p[PersonPlayer.ATTR_PHONE],
                roles=[a_role],  # TODO 20241022 This 'role_id' may not be yet added in the input data. Added here just to pass a test.
                children_ids = p[PersonPlayer.ATTR_CHILDREN],
                responsibilities=[_responsibility]
            )
            _persons.append(person)
        return _persons

    @classmethod
    def create_from_dictionaries(
            cls, dates_prefs, personnel_prefs, clean=False):
        """
        @summary: Input data converter from text-based (dictionary in .yaml) format to Python format.
          Or to see it from a different angle, this is a constructor https://realpython.com/instance-class-and-static-methods-demystified/#delicious-pizza-factories-with-classmethod
        @type dates_prefs: [{ "id", "name", "phone", "email", "children": {"child_id"}, "responsibility_id" }]
        @type personnel_prefs: [{ "id", "name", "phone", "email", "children": {"child_id"}, "responsibility_id" }]
        @param personnel_prefs: List particularly made by .yaml input.
        @rtype: matching.BaseGame
        """
        _dates, _reqs = GjVolunteerAllocationGame.create_from_dict_dates(dates_prefs, clean=clean)
        _persons = GjVolunteerAllocationGame.create_from_dict_persons(personnel_prefs, clean=clean)
        game = cls(_dates, PersonBank(_persons), _reqs, clean)
        return game

    @classmethod
    def create_from_dictionaries_2(
            cls, dates_prefs, persons_obj, clean=False):
        """
        @summary: Input data converter from text-based (dictionary in .yaml) format to Python format.
          Or to see it from a different angle, this is a constructor https://realpython.com/instance-class-and-static-methods-demystified/#delicious-pizza-factories-with-classmethod
        @type dates_prefs: [{ "id", "name", "phone", "email", "children": {"child_id"}, "responsibility_id" }]
        @type persons_obj: PersonBank
        @param personnel_prefs: List particularly made by .yaml input.
        @rtype: GjVolunteerAllocationGame (child class of `matching.BaseGame`)
        """
        _dates, _reqs = GjVolunteerAllocationGame.create_from_dict_dates(dates_prefs, clean=clean)
        game = cls(_dates, persons_obj, _reqs, clean)
        return game

    def check_stability(self):
        """
        @override
        """
        pass

    def check_validity(self):
        """
        @override
        """
        pass
