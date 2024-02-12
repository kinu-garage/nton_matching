#!/usr/bin/env python

# Copyright 2024 Isaac Saito.
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
import logging

from matching import BaseGame, ManyToManyMatching
from matching.exceptions import (
    MatchingError,
    PlayerExcludedWarning,
)
from matching.players import Player

from n_to_n_matching.util import Util


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


class GjVolunteerMatching(ManyToManyMatching):
    """
    @todo Consider optimizing and move code back to upstream as much
    """
    _KEY_DATE = "date"
    _KEY_PERSON_ID = "person_id"
    _KEY_ROLE_ID = "role_id"
    def __init__(self, dictionary):
        """
        @type dictionary: dict
        @param dictionary: needs the following keys:
           - "date"
           - "guardian_id"
           - "role_id"
        """        
        super().__init__(dictionary)
        # Validate the dict: Error if the `dictionary` doesn't have expected keys.

    def add_item(self, new_match):
        self._dataframe.append(new_match)


class WorkDate():
    # Attiribute in text (e.g. .yaml) input file 
    ATTR_DATE = "date"
    ATTR_NUM_LEADER = "num_leader"
    ATTR_NUM_COMMITTE = "num_commitee"
    ATTR_NUM_GENERAL = "num_general"
    ATTR_SCHOOL_OFF = "school_off"

    def __init__(self,
                 datestr,
                 school_off=False,
                 req_num_committee=3,
                 req_num_leader=1,
                 req_num_noncommittee=2,
                 assignee_leader=[],
                 assignee_commitee=[],
                 assignee_noncommitee=[]):
        """
        @param datestr: For now this needs to be "yyyy-mm-dd" format.
        @type assignees: [GuardianPlayer]
        @param assignee_ids_commitee: Can be empty when a class instantiates.
        """
        self.set_date(datestr)
        self._school_off = school_off
        self._req_num_leader = req_num_leader
        self._required_committee = req_num_committee
        self._required_noncommittee = req_num_noncommittee
        self._assignees_leader = assignee_leader
        self._assignees = assignee_commitee
        self._assignees_noncommittee = assignee_noncommitee

    def set_date(self, datestr):
        Util.validate_date_str(datestr)
        ymd = datestr.split("-")
        year = int(ymd[0])
        month = int(ymd[1])
        day = int(ymd[2])
        self._date = date(year, month, day)

    @property
    def date(self):
        """
        @rtype datetime.date
        """
        return self._date

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

    
class GjVolunteerAllocationGame(BaseGame):
    DATES = "dates"
    WORKERS = "workers"
    ATTR_MAX_OCCURRENCE_PER_ROLE = "max_occurence"
    ATTR_UNLUCKY_PERSON_NUMS = "num_unlucky_person"

    def __init__(self, dates, workers, clean=False, logger_obj=None):
        """
        """
        super().__init__(clean)
        self._dates = dates
        self._workers = PersonBank(workers)
        self._check_inputs()
        self._logger = self._set_logger(logger_obj)

    @classmethod
    def print_tabular(cls, solutions):
        raise NotImplementedError()

    def _set_logger(self, logger_obj):
        if logger_obj:
            return logger_obj
        logger = logging.getLogger(__name__)
        _stream_handler = logging.StreamHandler()
        _stream_handler.setLevel(logging.INFO)
        _stream_format = logging.Formatter('%(name)s - %(levelname)s: %(message)s')
        _stream_handler.setFormatter(_stream_format)
        # TODO For some reason, setting the log level in a handler here
        # doesn't seem to take effect. So setting basicConfig.
        logging.basicConfig(level=logging.INFO)
        #logger.addHandler(_stream_handler)
        return logger

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

    def eval_enough_assignees(self, date):
        """
        @summary Returns eval result if a given `date` has enough numbers of assignees.
            
        @type date: n_to_n_matching.WorkDate
        @rtype: bool, bool, bool
        @return: Return 3 boolean values of:
            1. True/False whether the number of retval-1 meets the requirement.
            2. True/False whether the number of retval-2 meets the requirement.            
        """
        _enough_leaders = len(date.assignees_leader) == date.req_num_leader
        _enough_committee = len(date.assignees_committee) == date.req_num_assignee_committee
        _enough_noncommittee = len(date.assignees_noncommittee) == date.req_num_assignee_noncommittee
        return _enough_leaders, _enough_committee, _enough_noncommittee

    def find_dates_need_attention(self, dates):
        """
        @summary Split the input `dates` into 2 sets, one that needs attention and the others don't.
        @type dates: [WorkDate]
        @rtype: [WorkDate], 
        """
        dates_attention = []
        dates_lgtm = []
        for date in dates:
            _enough_leaders, _enough_committee, _enough_noncommittee = self.eval_enough_assignees(date)
            if all([_enough_leaders, _enough_committee, _enough_noncommittee]):
                dates_lgtm.append(date)
            else:
                dates_attention.append(date)
        for date_attention in dates_attention:
            self._log_date_content(date_attention, "find_dates_need_attention: date_attention")
        for date_lgtm in dates_lgtm:
            self._log_date_content(date_lgtm, "find_dates_need_attention: date_lgtm")
        return dates_attention, dates_lgtm

    def total_slots_required(self, dates):
        """
        @summary: Returns the number per each of 3 role in order to cover all the dates in the arg.
        @note This method only handles the static info, NOT reflecting the current state of instances.
        @rtype int, int, int
        """
        needed_leader, needed_committee, needed_general = 0, 0, 0
        for day in dates:
            needed_leader += day.req_num_leader
            needed_committee += day.req_num_assignee_committee
            needed_general += day.req_num_assignee_noncommittee
        return needed_leader, needed_committee, needed_general

    def total_persons_available(self, persons):
        """
        @summary: Returns the number in the requirement. Note this method only handles the static info, NOT reflecting the current state of instances.
        @type persons: `PersonBank`
        @rtype int, int, int
        """
        avaialable_leader, avaialable_committee, avaialable_general = 0, 0, 0
        for key, value in persons.persons.items():
            rid = value.role_id
            if rid == PersonRole.LEADER.value:
                avaialable_leader += 1
            elif rid == PersonRole.COMMITTEE.value:
                avaialable_committee += 1
            elif rid == PersonRole.GENERAL.value:
                avaialable_general += 1
            else:
                #TODO print error
                print("Illegal person role-id found. PID: {}, Person obj: {}, role_id: {}. Ignoring.".format(key, value, rid))
        return avaialable_leader, avaialable_committee, avaialable_general

    def _log_available_persons(self, dates, needed_leader, needed_committee, needed_general,
                               available_leader, available_committee, available_general):
        self._logger.info("#dates {}\n\tneeded_leader {} needed_committee {} needed_general {}\n\tavailable_leader {} available_committee {} available_general {}".format(
            len(dates), needed_leader, needed_committee, needed_general, available_leader, available_committee, available_general))

    def max_allowed_days_per_person(self, dates, workers):
        """
        @summary:  Returning 2 sets of info for 3 kids of roles (leader, committee, generals):
            - max_*: Maximum number of times each person should be assigned to the correspondent role in the given period.
            - unlucky_*: Number of persons who need to take on the correspondent role once more than `max_*` number.
        @type workers: `PersonBank`
        @return: Dictionary structure should look like this:
            {
                PersonRole.LEADER: {ATTR_MAX_OCCURRENCE: max_leader, ATTR_UNLUCKY_PERSON_NUMS: unlucky_leaders},
                PersonRole.COMMITTEE: {ATTR_MAX_OCCURRENCE: max_committee, ATTR_UNLUCKY_PERSON_NUMS: unlucky_committees},
                PersonRole.GENERAL: {ATTR_MAX_OCCURRENCE: max_general, ATTR_UNLUCKY_PERSON_NUMS: unlucky_generals},
            }
        @raise ValueError: If not enough number of persons with a role is given in `workers`.
        """
        def _debug_print_max_per_person(*args):
            print("Debug:\t")
            for arg in args:
                print(f'\t{arg=}')

        # Find the total number of slots need to be filled in all `dates`.
        needed_leader, needed_committee, needed_general = self.total_slots_required(dates)
        available_leader, available_committee, available_general = self.total_persons_available(workers)
        if not all([available_leader, available_committee, available_general]):
            raise ValueError("Any one of these must not be 0: available_leader={}, available_committee={}, available_general={}".format(
                available_leader, available_committee, available_general))
        self._log_available_persons(dates, needed_leader, needed_committee, needed_general, available_leader, available_committee, available_general)

        try:
            max_leader, unlucky_leaders = divmod(needed_leader, available_leader)
            max_committee, unlucky_committees = divmod(needed_committee, available_committee)
            max_general, unlucky_generals = divmod(needed_general, available_general)
        except ZeroDivisionError as e:
            raise ZeroDivisionError("Theres is at least one arg that is zero. {}".format(
                _debug_print_max_per_person(max_leader, unlucky_leaders, max_committee, unlucky_committees, max_general, unlucky_generals))) from e
        max_allowance = {
            PersonRole.LEADER: {
                self.ATTR_MAX_OCCURRENCE_PER_ROLE: max_leader,
                self.ATTR_UNLUCKY_PERSON_NUMS: unlucky_leaders},
            PersonRole.COMMITTEE: {
                self.ATTR_MAX_OCCURRENCE_PER_ROLE: max_committee,
                self.ATTR_UNLUCKY_PERSON_NUMS: unlucky_committees},
            PersonRole.GENERAL: {
                self.ATTR_MAX_OCCURRENCE_PER_ROLE: max_general,
                self.ATTR_UNLUCKY_PERSON_NUMS: unlucky_generals},
            }
        self._logger.info("max_allowance: {}".format(max_allowance))
        return max_allowance

    def _get_assigned_dates(self, person_id):
        """
        @summary Returns the number that a person of `person_id` is assigned to
          in the period that is given to the tool, regardless the type
          of the role.
        @note TODO The method relies on a member variable (`_dates`), which I don't like. So there's a room for refactoring.
        @rtype int
        """
        assigned = 0

        def count(person_id, persons, countednum):
            for person in persons:
                if person.id == person_id:
                    countednum += 1
            return countednum

        for date in self._dates:
            assigned_l = count(person_id, date.assignees_leader, assigned)
            assigned_c = count(person_id, date.assignees_committee, assigned)
            assigned_nc = count(person_id, date.assignees_noncommittee, assigned)
            self._log_date_content(date)
        assigned = assigned_l + assigned_c + assigned_nc
        self._logger.info("person_id: {} assigned_l: {} assigned_c: {} assigned_nc: {}".format(
            person_id, assigned_l, assigned_c, assigned_nc))
        return assigned

    def find_free_workers(self, persons, overbook_allowed_num=1):
        """
        @summary: Returns the set of persons who are not yet assigned required number of the times in the given period.
        @type persons: PersonBank
        @param overbook_allowed_num: Number of times an overbooked person can take.
        @rtype: [GuardianPlayer], [GuardianPlayer], [GuardianPlayer]
        @return: Even when any of the return values is empty, the method does NOT warn the caller. 
          i.e. It's the caller's responsibility to check the returned values' validity.
        """
        # `max_allowance``: dictionary that `GjVolunteerAllocationGame.max_allowed_days_per_person` returns.
        if not persons.max_allowance:
            raise RuntimeError("Field `max_allowance` is empty, which indicates something is wrong...TBD add how to troubleshoot")
        free_workers = []
        fullybooked_workers = []
        overlybooked_workers = []
        for person_id, worker in persons.persons.items():
            assigned_dates = self._get_assigned_dates(person_id)
            max_days_incl_overbook = assigned_dates + overbook_allowed_num
            # Maybe a bit unintuitive but passing a value via enum subclass is a valid way to access
            # a value of a member of an enum class https://realpython.com/python-enum/#accessing-enumeration-members
            this_person_allowance = persons.max_allowance[PersonRole(worker.role_id)]
            _occurrence_per_role = this_person_allowance[self.ATTR_MAX_OCCURRENCE_PER_ROLE]
            # If a person's assigned dates is smaller than the role's max occurrence, then this person can take more dates.
            if assigned_dates < _occurrence_per_role:
                free_workers.append(worker)
            elif assigned_dates == _occurrence_per_role:
                fullybooked_workers.append(worker)
            elif max_days_incl_overbook == _occurrence_per_role:
                overlybooked_workers.append(worker)
            elif max_days_incl_overbook < this_person_allowance[self.ATTR_MAX_OCCURRENCE_PER_ROLE]:
                raise ValueError("Person ID {} is assigned for '{}' days, which exceeds the limit assigned days={}. TODO Needs figured out".format(
                    person_id, assigned_dates, max_days_incl_overbook))
            else:
                self._logger.warning("_occurrence_per_role = '{}' not falling under any criteria. Skipping for now.".format(
                    _occurrence_per_role))
            self._logger.info("PersonRole(worker.role_id): '{}', assigned_dates: '{}', _occurrence_per_role: '{}'".format(
                PersonRole(worker.role_id), assigned_dates, _occurrence_per_role))
        self._logger.info("free_workers {}\nfullybookd_workers {}\noverlybooked_workers {}".format(
            free_workers, fullybooked_workers, overlybooked_workers))
        #if not free_workers:
        #    raise ValueError("All given persons are already assigned to the max number of dates")
        return free_workers, fullybooked_workers, overlybooked_workers

    def _assign_day(self, date, person_bank, overbook=False):
        """
        @type person_bank: [PersonBank]
        @param persons: Pool of persons to be assigned if condition meets.
        """
        if not person_bank.persons:
            raise ValueError("There's no pool of persons in the arg.")

        _persons = person_bank.persons.values()
        if overbook:
            _free_ppl, fullybooked_ppl, overbooked_ppl = self.find_free_workers(person_bank)
            _persons = fullybooked_ppl
        for person in _persons:
            _enough_leaders, _enough_committee, _enough_noncommittee = self.eval_enough_assignees(date)
            if all([_enough_leaders, _enough_committee, _enough_noncommittee]):
                break
            elif (not _enough_leaders) and (person.role_id == PersonRole.LEADER.value):
                date.assignees_leader.append(person)
            elif (not _enough_committee) and (person.role_id == PersonRole.COMMITTEE.value):
                date.assignees_committee.append(person)
            elif (not _enough_noncommittee) and (person.role_id == PersonRole.GENERAL.value):
                date.assignees_noncommittee.append(person)
            else:
                self._logger.warning("TBD hmmm not sure what this means, needs looked into. _enough_leaders: {}, _enough_committee: {}, _enough_noncommittee: {}".format(
                    _enough_leaders, _enough_committee, _enough_noncommittee))
                continue
        return date

    def assign_person(self, date, person_bank, overbook=True):
        """
        @type free_workers: [PersonPlayer]
        @type booked_persons: [PersonPlayer]
        @param overbook: Naming may not be appropriate so want a better one. When True, 
        @rtype: WorkDate, [PersonPlayer]
        @return:
          - `free_workers`: the same instance as the input arg but with potentially one element popped out.
          - `booked_persons`: the same instance as the input arg but with potentially one element appended.
          - `overlybooked_workers`: f

          Also, `date` is NOT returned explicitly, but potentially its `assignee_ids_{commitee, noncommitee}` field is updated.
        """
        # Fill in the assignee if a `date` doesn't have enough assignees.
        is_enough_commitee, is_enough_noncommitee = False, False

        # Assign a personnel taken from `free_workers`. Once done, update the `free_workers`.
        #while (not is_enough_commitee) or (not is_enough_noncommitee):
        date = self._assign_day(date, person_bank)

        # Once evaluated all `free_workers` and yet the date is not filled with needed number of persons,
        # use `ATTR_UNLUCKY_PERSON_NUMS` persons.
        _enough_leaders, _enough_committee, _enough_noncommittee = self.eval_enough_assignees(date)        
        if not all([_enough_leaders, _enough_committee, _enough_noncommittee]):
            date = self._assign_day(date, person_bank, overbook=True)

    def _log_date_content(self, date, msg_prefix=""):
        self._logger.info("{} Date={} assignees stored. Leader: {}, Committee: {}, Non-commitee: {}".format(
            msg_prefix, date.date, date.assignees_leader, date.assignees_committee, date.assignees_noncommittee))

    def match(self, dates, workers, optimal=""):
        """
        @type dates: [n_to_n_matching.WorkDate]
        @type workers: n_to_n_matching.PersonBank
        @param optimal: Unused for now, kept just to make it consistent with `matching` pkg.
        @return 
        @raise ValueError: If the given `dates` already filled with assignees.
        """
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
            raise ValueError("The input `dates` have all slots filled already.")
        ## Ok, there are some dates that need assignees.
        ## Continuing screening. Determine the maximum #days each person can be assigned to.
        workers.max_allowance = self.max_allowed_days_per_person(dates, workers)
        # END: Initial screening

        # Assign personnels per date
        for date in dates_need_attention:
            self._log_date_content(date, msg_prefix="BEFORE assigning:")
            self.assign_person(date, workers)
            dates_lgtm.append(date)
            #dates_need_attention.remove(date)
            # Temp test
            date.assignees_leader = []
            self._log_date_content(date, msg_prefix="AFTER assigning a day:")
            self._logger.info("AFTER assigning a day: All dates_need_attention={}\n\tdates_lgtm={}".format(dates_need_attention, dates_lgtm))
        return dates_lgtm        

    def solve(self, optimal=""):
        """
        @description: 
        @return matching.BaseMatching
        """
        self._matching = GjVolunteerMatching(
            self.match(self._dates, self._workers, optimal)
        )
        return self._matching

    @classmethod
    def create_from_dict_dates(cls, dates_prefs, clean=False):
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
        """
        _dates = []
        for d in dates_prefs:
            _school_off = d.get(WorkDate.ATTR_SCHOOL_OFF, False)
            _req_num_leader = d.get(WorkDate.ATTR_NUM_LEADER, 1)
            _req_num_committee = d.get(WorkDate.ATTR_NUM_COMMITTE, 2)
            _req_num_noncommittee = d.get(WorkDate.ATTR_NUM_GENERAL, 3)
            date = WorkDate(datestr=d[WorkDate.ATTR_DATE],
                            school_off=_school_off,
                            req_num_leader=_req_num_leader,
                            req_num_committee=_req_num_committee,
                            req_num_noncommittee=_req_num_noncommittee)
            _dates.append(date)
        return _dates

    @classmethod
    def create_from_dict_persons(cls, person_prefs, clean=False):
        """
        @summary: Input data converter from text-based (dictionary in .yaml) format to Python format.
        @type personnel_prefs: [{ "id", "name", "phone", "email", "children": {"child_id"}, "role_id" }]
        """
        _persons = []
        for p in person_prefs:
            _role_id = p.get(PersonPlayer.ATTR_ROLE_ID, PersonRole.GENERAL)
            person = PersonPlayer(
                id=p[PersonPlayer.ATTR_ID],
                name=p[PersonPlayer.ATTR_NAME],
                email_addr = p[PersonPlayer.ATTR_EMAIL],
                phone_num = p[PersonPlayer.ATTR_PHONE],
                children_ids = p[PersonPlayer.ATTR_CHILDREN],
                role_id=_role_id
            )
            _persons.append(person)
        return _persons

    @classmethod
    def create_from_dictionaries(
            cls, dates_prefs, personnel_prefs, clean=False):
        """
        @summary: Input data converter from text-based (dictionary in .yaml) format to Python format.
          Or to see it from a different angle, this is a constructor https://realpython.com/instance-class-and-static-methods-demystified/#delicious-pizza-factories-with-classmethod
        @type dates_prefs: [{ "id", "name", "phone", "email", "children": {"child_id"}, "role_id" }]
        @type personnel_prefs: [{ "id", "name", "phone", "email", "children": {"child_id"}, "role_id" }]
        @param personnel_prefs: List particularly made by .yaml input.
        @rtype: matching.BaseGame
        """
        _dates = GjVolunteerAllocationGame.create_from_dict_dates(dates_prefs, clean=clean)
        _persons = GjVolunteerAllocationGame.create_from_dict_persons(personnel_prefs, clean=clean)
        game = cls(_dates, _persons, clean)
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
