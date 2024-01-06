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

from enum import Enum

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
        return self._persons

    @persons.setter
    def persons(self, val):
        raise AttributeError("`persons` is an initial raw input and cannot be overwritten.")

    def update_person(self, person):
        self.persons[person.id] = person                

    @property
    def max_allowance(self):
        return self._max_allowance


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
                 school_off=False,
                 req_num_committee=3,
                 req_num_leader=1,
                 req_num_noncommittee=2,
                 assignee_commitee=[],
                 assignee_noncommitee=[]):
        """
        @type assignees: [GuardianPlayer]
        @param assignee_ids_commitee: Can be empty when a class instantiates.
        """
        self._school_off = school_off
        self._req_num_leader = req_num_leader
        self._required_committee = req_num_committee
        self._required_noncommittee = req_num_noncommittee
        self._assignees = assignee_commitee
        self._assignees_noncommitee = assignee_noncommitee

    @property
    def assignees(self):
        return self._assignees

    @assignees.setter
    def assignees(self, val):
        self._assignees = val

    @property
    def assignees_noncommitee(self):
        return self._assignees_noncommitee

    @assignees_noncommitee.setter
    def assignees_noncommitee(self, val):
        self._assignees_noncommitee = val


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
       self._id = id
       self._name = name
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

    
class GjVolunteerAllocationGame(BaseGame):
    DATES = "dates"
    WORKERS = "workers"
    ATTR_MAX_OCCURRENCE_PER_ROLE = "max_occurence"
    ATTR_UNLUCKY_PERSON_NUMS = "num_unlucky_person"

    def __init__(self, dates, workers, clean=False):
        """
        """
        self._dates = dates
        self._workers = PersonBank(workers)
        super().__init__(clean)
        self._check_inputs()

    @classmethod
    def print_tabular(cls, solutions):
        raise NotImplementedError()

    def _check_inputs(self):
        """
        @see Hospital Residents https://daffidwilde.github.io/matching/docs/tutorials/hospital_resident.html
        @description: Check if any rules of the game have been broken.
                Any violations will be flagged as warnings. If the ``clean``
                attribute is in use, then any violations will be removed.
        """
        # This app doesn't require prefs so I'm not sure if calling these
        # is needed but will give it a try for now.
        self._check_inputs_player_prefs_unique(self.DATES)
        self._check_inputs_player_prefs_unique(self.WORKERS)
        self._check_inputs_player_capacity(self.DATES, self.WORKERS)

    def _check_inputs_player_capacity(self, party, other_party):
        """
        @see Hospital Residents https://daffidwilde.github.io/matching/docs/tutorials/hospital_resident.html
        @description Check everyone has a capacity of at least one."""

        for player in vars(self)[party]:
            if player.capacity < 1:
                warnings.warn(PlayerExcludedWarning(player))

                if self.clean:
                    self._remove_player(player, party, other_party)

    def max_per_given_period(self, dates, workers):
        """
        @summary: Return the maximum dates that one worker can be assigned to in a given period.
            e.g. In the case where len(dates) = 4, len(workers) = 7 (3 are commitee, 4 are non-committee),
        @rtype: int, int
        @return: Maximum numbers of 1) "commitee" (or with any special role) worker, 2) non-commitee worker.
        """

    def eval_enough_assignees(self, date):
        """
        @summary Returns eval result if a given `date` has enough numbers of assignees.
            
        @type date: n_to_n_matching.WorkDate
        @rtype: bool, bool
        @return: Return two boolean values of:
            1. True/False whether the number of retval-1 meets the requirement.
            2. True/False whether the number of retval-2 meets the requirement.            
        """
        _enough_committee = date.assignees_commitee == date.req_num_assignee_committee
        _enough_noncommittee = date.assignees_noncommitee == date.req_num_assignee_noncommittee
        return _enough_committee, _enough_noncommittee

    def find_dates_need_attention(self, dates):
        """
        @summary Split the input `dates` into 2 sets, one that needs attention and the others don't.
        @type dates: [WorkDate]
        @rtype: [WorkDate], 
        """
        dates_attention = []
        dates_lgtm = []
        for date in dates:
            _enough_committee, _enough_noncommittee = self.eval_enough_assignees(date)
            if _enough_committee and _enough_noncommittee:
                dates_lgtm.append(date)
            else:
                dates_attention.append(date)
        return dates_attention, dates_lgtm

    def total_slots_required(dates):
        """
        @summary: Returns the number in the requirement. Note this method only handles the static info, NOT reflecting the current state of instances.
        @rtype int, int, int
        """
        needed_leader, needed_committee, needed_general = 0
        for day in dates:
            needed_leader += day.req_num_leader
            needed_committee += day.req_num_committee
            needed_general += day.req_num_noncommittee
        return needed_leader, needed_committee, needed_general

    def total_persons_available(persons):
        """
        @summary: Returns the number in the requirement. Note this method only handles the static info, NOT reflecting the current state of instances.
        @rtype int, int, int
        """
        avaialable_leader, avaialable_committee, avaialable_general = 0
        for p in persons:
            rid = p.role_id
            if rid == PersonRole.LEADER:
                avaialable_leader += 1
            elif rid == PersonRole.COMMITTEE:
                avaialable_committee += 1
            elif rid == PersonRole.GENERAL:
                avaialable_general += 1
            else:
                #TODO print error
                print("Illegal person role-id found. Ignoring.")
        return avaialable_leader, avaialable_committee, avaialable_general
               
    def max_allowed_days_per_person(self, dates):
        """
        @summary:  Returning 2 sets of info for 3 kids of roles (leader, committee, generals):
            - max_*: Maximum number of times each person should be assigned to the correspondent role in the given period.
            - unlucky_*: Number of persons who need to take on the correspondent role once more than `max_*` number.
        @return: Dictionary structure should look like this:
            {
                PersonRole.LEADER: {ATTR_MAX_OCCURRENCE: max_leader, ATTR_UNLUCKY_PERSON_NUMS: unlucky_leaders},
                PersonRole.COMMITTEE: {ATTR_MAX_OCCURRENCE: max_committee, ATTR_UNLUCKY_PERSON_NUMS: unlucky_committees},
                PersonRole.GENERAL: {ATTR_MAX_OCCURRENCE: max_general, ATTR_UNLUCKY_PERSON_NUMS: unlucky_generals},
            }
        """
        # Find the total number of slots need to be filled in all `dates`.
        needed_leader, needed_committee, needed_general = self.total_slots_required(dates)
        available_leader, available_committee, available_general = self.total_persons_available(dates)

        max_leader, unlucky_leaders = divmod(available_leader, needed_leader)
        max_committee, unlucky_committees = divmod(available_committee, needed_committee)
        max_general, unlucky_generals = divmod(available_general, needed_general)
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
        return max_allowance

    def _get_assigned_dates(self, person_id):
        """
        @note TODO The method relies on a member variable (`_dates`), which I don't like. So there's a room for refactoring.
        @rtype int
        """
        assigned = 0
        for date in self._dates:
            def count(person_id, persons, countednum):
                for person in persons:
                    if person.id == person_id:
                        countednum += 1
                return countednum
            
            assigned = count(person_id, date.assignees, assigned)
            assigned = count(person_id, date.assignees_noncommitee, assigned)
        return assigned

    def find_free_workers(self, persons, overbook_allowed_num=1):
        """
        @summary: Returns the set of persons who are not yet assigned required number of the times in the given period.
        @type persons: PersonBank
        @param overbook_allowed_num: Number of times an overbooked person can take.
        @rtype: [GuardianPlayer], [GuardianPlayer], [GuardianPlayer]
        @throw ValueError
        """
        # `max_allowance``: dictionary that `GjVolunteerAllocationGame.max_allowed_days_per_person` returns.
        if not self.max_allowance:
            raise RuntimeError("Field `max_allowance` is empty, which indicates something is wrong...TBD add how to troubleshoot")
        free_workers = []
        fullybookd_workers = []
        overlybooked_workers = []
        for worker in self.persons:
            assigned_dates = self._get_assigned_dates(worker.id)
            this_person_allowance = self.max_allowance[worker.role_id]
            # If a person's assigned dates is smaller than the role's max occurrence, then this person can take more dates.
            if assigned_dates < this_person_allowance[self.ATTR_MAX_OCCURRENCE_PER_ROLE]:
                free_workers.append(worker)
            elif assigned_dates == this_person_allowance[self.ATTR_MAX_OCCURRENCE_PER_ROLE]:
                fullybookd_workers.append(worker)
            elif assigned_dates + overbook_allowed_num == this_person_allowance[self.ATTR_MAX_OCCURRENCE_PER_ROLE]:
                overlybooked_workers.append(worker)
            elif this_person_allowance[self.ATTR_MAX_OCCURRENCE_PER_ROLE] < assigned_dates + overbook_allowed_num:
                raise ValueError("Person ID {} is assigned for '{}' days, which exceeds the limit assigned days. TODO Needs figured out".format(
                    worker.id, assigned_dates))
        if not free_workers:
            raise ValueError("All given persons are already assigned to the max number of dates")
        return free_workers, fullybookd_workers, overlybooked_workers

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
        free_workers, booked_persons = self.find_free_workers(person_bank.persons)
        # Fill in the assignee if a `date` doesn't have enough assignees.
        is_enough_commitee, is_enough_noncommitee = False, False

        # Assign a personnel taken from `free_workers`. Once done, update the `free_workers`.
        #while (not is_enough_commitee) or (not is_enough_noncommitee):
        date = self._assign_day(date, free_workers)

        # Once evaluated all `free_workers` and yet the date is not filled with needed number of persons,
        # use `ATTR_UNLUCKY_PERSON_NUMS` persons.
        _enough_committee, _enough_noncommittee = self.eval_enough_assignees(date)        
        if not (_enough_committee and _enough_noncommittee):
            _overlybooked_workers = []
            date = self._assign_day(date, booked_persons)
            
        return free_workers, booked_persons

    def _assign_day(self, date, persons):
        """
        @param persons: Pool of persons to be assigned if condition meets.
        """
        if not persons:
            raise ValueError("TBD error; There's no pool of persons who are fully booked but can be taking one additional.")
        
        for person in persons:
            _enough_committee, _enough_noncommittee = self.eval_enough_assignees(date)
            if _enough_committee and _enough_noncommittee:
                break
            elif (not _enough_committee) and (person.role_id == PersonPlayer.TYPE_OBLIGATION_COMMITEE):
                date.assignee_commitee.append(person)
            elif (not _enough_noncommittee) and (person.role_id == PersonPlayer.TYPE_OBLIGATION_NONCOMMITEE):
                date.assignee_noncommitee.append(person)
            else:
                print("TBD hmmm not sure what this means, needs looked into.")
                continue
        return date

    def match_per_date(self, dates, workers):
        """
        @type person:
        @param workers: `PersonBank`
        @return 
        @raise ValueError: If the given `dates` already filled with assignees.
        """
        dates_need_attention = []

        # Figure out how many dates each worker can be assigned to for the given `dates`.
        _max_daily_committee_perperson, _max_daily_noncommittee_perperson = self.max_per_given_period(dates, workers)
        _max_daily_all = _max_daily_committee_perperson + _max_daily_noncommittee_perperson

        # BEGIN: Initial screening
        ## See if there's any date where 1 or more assignees are needed.
        dates_need_attention, dates_lgtm = self.find_dates_need_attention(dates)
        if not dates_need_attention:
            # There's no date where an assignee is missing.
            raise ValueError("The input `dates` have all slots filled already.")
        ## Ok, there are some dates that need assignees.
        ## Continuing screening. Determine the maximum #days each person can be assigned to.
        workers.max_allowance = self.max_allowed_days_per_person(dates)

        ## Continuing screening. See if there are workers who have a room to be assigned.
        free_workers, booked_person, overlybooked_workers = [], [], []
#        try:
#            free_workers, booked_persons, overlybooked_workers = self._workers.find_free_workers(max_allowance, workers)
#        except ValueError as e:
#            print("TBD Honestly, I haven't thought of how to handle this situation yet.\n{}".format(str(e)))
        # END: Initial screening

        # Assign personnels per date
        for date in dates_need_attention:
            self.assign_person(date, workers)
            dates_lgtm.append(date)
        return dates_lgtm        

    def solve(self, optimal=""):
        """
        @description: 
        @return matching.BaseMatching
        """
        self._matching = GjVolunteerMatching(
            self.match_per_date(self._dates, self._workers, optimal)
        )
        return self._matching

    @classmethod
    def create_from_dict_dates(cls, dates_prefs, clean=False):
        """
        @summary: Input data converter from text-based (dictionary in .yaml) format to Python format.
        @type dates_prefs: [{ "id", "name", "phone", "email", "children": {"child_id"}, "role_id" }]
        """
        _dates = []
        for d in dates_prefs:
            _school_off = d.get(WorkDate.ATTR_SCHOOL_OFF, False)
            _req_num_leader = d.get(WorkDate.ATTR_NUM_LEADER, 1)
            _req_num_committee = d.get(WorkDate.ATTR_NUM_COMMITTE, 2)
            _req_num_noncommittee = d.get(WorkDate.ATTR_NUM_GENERAL, 3)
            date = WorkDate(date=d[WorkDate.ATTR_DATE],
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
                childrens_ids = p[PersonPlayer.ATTR_CHILDREN],
                role_id=_role_id
            )
            _persons.append(person)
        return _persons

    @classmethod
    def create_from_dictionaries(
            cls, dates_prefs, personnel_prefs, clean=False):
        """
        @summary: Input data converter from text-based (dictionary in .yaml) format to Python format.
        @type dates_prefs: [{ "id", "name", "phone", "email", "children": {"child_id"}, "role_id" }]
        @type personnel_prefs: [{ "id", "name", "phone", "email", "children": {"child_id"}, "role_id" }]
        @param personnel_prefs: List particularly made by .yaml input.
        @rtype: matching.BaseGame
        """
        _dates = GjVolunteerAllocationGame.create_from_dict_dates(dates_prefs, clean=clean)
        _persons = GjVolunteerAllocationGame.create_from_dict_persons(personnel_prefs, clean=clean)
        game = cls(_dates, _persons, clean)
        return game

def __main__():
    #dates_input = Util.read_yaml_to_dict(base_url, "dates.yml")
    dates_input = [
        { "date": "2024-04-01", },
        {
            "date": "2024-04-08",
            "num_leader": 1,
            "num_commitee": 2,
            "num_general": 3,
        },
        { "date": "2024-04-15", },
        { "date": "2024-04-22", }
    ]
    #guardian_input = Util.read_yaml_to_dict(base_url, "guardian.yml")
    guardian_input = [
        {
            "id": 1,
            "name": "guardian-name1",
            "phone": "000-000-0000",
            "email": "1@dot.com.dummy",
            "children": {
              "child_id": 1111,
              "child_id": 1112},
            "role_id": 1
        },
        {
            "id": 2,
            "name": "guardian-name2",
            "phone": "000-000-0000",
            "email": "2@dot.com.dummy",
            "children": {
              "child_id": 1113},
            "role_id": 2
        },
        {
            "id": 3,
            "name": "guardian-name3",
            "phone": "000-000-0000",
            "email": "3@dot.com.dummy",
            "children": {
                "child_id": 1114,
                "child_id": 1115,
                "child_id": 1116},
            "role_id": 2
        },
        {
            "id": 4,
            "name": "guardian-name4",
            "phone": "000-000-0000",
            "email": "4@dot.com.dummy",
            "children": {
              "child_id": 1117},
            "role_id": 1
        },
        {
            "id": 5,
            "name": "guardian-name5",
            "phone": "000-000-0000",
            "email": "5@dot.com.dummy",
            "children": {
                "child_id": 1118,
                "child_id": 1119,
                "child_id": 1120,
                "child_id": 1121},
            "role_id": 2
        },
    ]

    num_dates = len(dates_input)
    num_guardians = len(guardian_input)
    game = GjVolunteerAllocationGame.create_from_dictionaries(
        dates_input, guardian_input)
    solution = game.solve()
    for date, guardians in solution.items():
        print(f"{date} ({date.capacity}): {guardians}")
    GjVolunteerAllocationGame.print_tabular(solution)

