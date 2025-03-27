#!/usr/bin/env python

# Copyright 2016 Isaac I. Y. Saito.
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
from typing import Dict, List, Tuple

from gj.requirements import DateRequirement
from gj.responsibility import Committeer, Leader, GenGuardian, Responsibility, ToubanExempt
from gj.responsibility import ResponsibilityLevel as RespLvl
from gj.requirements import Consts
from gj.role import Role, Roles_Definition
from n_to_n_matching.person_player import PersonBank, PersonPlayer
from n_to_n_matching.util import Util as NtonUtil
from n_to_n_matching.workdate_player import WorkDate


class GjUtil:
    @staticmethod
    def get_logger(name_logger="", logger_obj: logging.Logger=None) -> logging.Logger:
        """
        @todo Remove this. This is made only as a tentative measure to avoid "not found" error after 'get_logger' is moved to n_to_n_matching.util.Util.
        """
        return NtonUtil.get_logger(name_logger, logger_obj)

    @staticmethod
    def corresponding_responsibility(role: Role, logger=None) -> Responsibility:
        """
        @summary: Matching logic is based on SY2024 setting.
        """
        if not logger:
            logger = GjUtil.get_logger()
        _responsibility = None
        if role:
            a_role_id = role.id
        else:
            a_role_id = 0
        logger.debug(f"{a_role_id=}")
        if ((a_role_id == Roles_Definition.GAKYU_COMMITEE.value) or
            (a_role_id == Roles_Definition.GYOJI_COMMITEE.value) or
            (a_role_id == Roles_Definition.TOUBAN_COMMITEE.value) or
            (a_role_id == Roles_Definition.UNDOKAI_COMMITEE.value) or 
            (a_role_id == Roles_Definition.UNEI_COMMITEE.value)
            ):
            _responsibility = ToubanExempt()
        elif ((a_role_id == Roles_Definition.SAFETY_COMMITEE.value) or
              (a_role_id == Roles_Definition.TOSHO_COMMITEE.value)
              ):
            _responsibility = Committeer()
        elif (
            # Handling of photo clue might be still NOT lucid as of 2024/08. 
            # Ref. https://groups.google.com/a/gjls.org/g/touban-group/c/8ikrmPQ15lk
            (a_role_id == Roles_Definition.PHOTO_CLUE.value) or
            (not a_role_id)):
            _responsibility = GenGuardian()
        else:
            raise ValueError(f"""Obtained role '{a_role_id}' does NOT match any rule.
Make sure the input value conforms to the string expression this tool supports.
It is likely that the input values come all the way down from the input 'master' file (likely in '.xlsx' format).
So if that .xlsx file is an input data for your appliaction, check to see if there's any
                             """)
        return _responsibility

    @staticmethod
    def gen_responsibility(responsibility_level: RespLvl, logger=None) -> Responsibility:
        """
        @summary This method represents a "Director" role for "Builder" pattern https://refactoring.guru/design-patterns/builder
          for either PersonPlayer obj or 
        @rtype: gj.responsibility.Responsibility
        @deprecated: As of 20250305, context is somewhat lost (conforming to a Design Pattern as mentioned above is nice though). Use `corresponding_responsibility` for now.
        """
        responsibility = None
        if (responsibility_level == RespLvl.LEADER):
            responsibility = Leader()
        elif (responsibility_level == RespLvl.COMMITTEE):
            responsibility = Committeer()
        elif (responsibility_level == RespLvl.GENERAL):
            responsibility = GenGuardian()
        #else:  # For now keep 'responsibility' = None.
        return responsibility            

    @staticmethod
    def get_assigned_dates(
        person_id: int, dates: List[WorkDate], logger: logging.Logger=None) -> Tuple[int, int, int, int]:
        """
        @summary: Returns the number that a person of `person_id` is assigned to
          in the period that is given to the tool (by `dates`), regardless the typeof the responsibility.
        @return Four set of integers:
          - assign_count: Sum of all the rest of integers.
          - assigned_leader, assigned_committee, assigned_noncommittee
        """
        if not logger:
            logger = GjUtil.get_logger()
        if (not isinstance(person_id, int)) or (not isinstance(dates[0], WorkDate)):
            raise TypeError(f"One of the args' type is incompatible.\n\tperson_id: '{type(person_id)}' (value: '{person_id}')\n\tdate[0]: '{type(dates[0])}' (value: {dates[0]})")

        assign_count = 0
        def count_assigned(person_id, persons, countednum):
            for person in persons:
                logger.debug("161 person.id: {} person_id: {}".format(person.id, person_id))
                if int(person.id) == int(person_id):
                    logger.debug("162 Matched: person.id: {} person_id: {}".format(person.id, person_id))
                    countednum += 1
            logger.debug("countednum {}".format(countednum))
            return countednum

        assigned_leader = assigned_committee = assigned_noncommittee = 0
        for date in dates:
            assigned_leader += count_assigned(person_id, date.assignees_leader, assign_count)
            assigned_committee += count_assigned(person_id, date.assignees_committee, assign_count)
            assigned_noncommittee += count_assigned(person_id, date.assignees_noncommittee, assign_count)
            #self._log_date_content(date)
        assign_count = assigned_leader + assigned_committee + assigned_noncommittee
        logger.debug("person_id: {}, assign_count: {}, assigned_leader: {} assigned_committee: {} assigned_noncommittee: {}".format(
            person_id, assign_count, assigned_leader, assigned_committee, assigned_noncommittee))
        return assign_count, assigned_leader, assigned_committee, assigned_noncommittee

    @staticmethod
    def total_persons_available(persons: PersonBank, logger=None) -> Tuple[int, int, int]:
        """
        @summary: Returns the number in the requirement. Note this method only handles the static info,
          NOT reflecting the current state of instances.
        @note: Total #leaders is not returned, as that number could be equal to #committee. Application later should
          make a judgement to pull someone of committee persons and assigns the leader role.
        """
        if not logger:
            logger = GjUtil.get_logger()
        avaialable_leader, avaialable_committee, avaialable_general, exempted = 0, 0, 0, 0

        for person_id, person in persons.persons.items():            
            resp_ids = [rid.id for rid in person.responsibilities if rid]
            if RespLvl.COMMITTEE.value in resp_ids:
                # As of 202408 the logic to assign 'leader' is unclear (this needs to be asked for the domain expert).
                # TODO For now all 'committee' member gets 1 leader value, which won't work for sure
                # once https://github.com/kinu-garage/nton_matching/issues/22 is addressed, hence this is temporary.
                avaialable_committee += 1
            elif RespLvl.GENERAL.value in resp_ids:
                avaialable_general += 1
            elif RespLvl.TOUBAN_EXEMPT.value in resp_ids:
                exempted += 1
            else:
                logger.error(f"Illegal person responsibility-id found. responsibilities: {Responsibility.str_responsibilities(person.responsibilities)}, {resp_ids=}. \
Ignoring {person_id=}, Person: {person}.")
        return avaialable_committee, avaialable_general, exempted

    @staticmethod
    def total_slots_required(dates: List[WorkDate]) -> Tuple[int, int, int]:
        """
        @summary: Returns the number per each of 3 responsibility in order to cover all the dates in the arg.
        @type dates: [WorkDate]
        @note This method only handles the static info, NOT reflecting the current state of instances.
        @rtype int, int, int
        """
        needed_leader, needed_committee, needed_general = 0, 0, 0
        for day in dates:
            _reqnum_leader, _reqnum_committee, _reqnum_general = day.get_required_persons()
            needed_leader += _reqnum_leader
            needed_committee += _reqnum_committee
            needed_general += _reqnum_general
        return needed_leader, needed_committee, needed_general

    @staticmethod
    def _log_persons_per_bookings(
            free_workers,
            fullybooked_workers,
            overlybooked_workers,
            msg_prefix= "",
            logger=None):
        if not logger:
            logger = GjUtil.get_logger()
        logger.info(f"{msg_prefix}\n\tfree_workers {free_workers}\n\tfullybooked_workers {fullybooked_workers}\n\toverlybooked_workers {overlybooked_workers}")

    @staticmethod
    def find_free_workers(
        dates: List[WorkDate],
        persons: List[PersonPlayer],
        max_allowance_resplvl: Dict[str, int],
        overbook_allowed_num: int=1,
        logger=None) -> Tuple[List[PersonPlayer], List[PersonPlayer], List[PersonPlayer]]:
        """
        @summary: Returns the set of persons who are not yet assigned the maximum number of the times in the given period.
        @param overbook_allowed_num: Number of times an overbooked person can take.
        @return: 3 lists that contain `PersonPlayer` instances, namely:
           - No assignment.
           - Fully assigned.
           - Assigned more than the allowance.
        @note: Even when any of the return values are empty, the method does NOT warn the caller.
          i.e. It's the caller's responsibility to check the returned values' validity.
        """
        if not logger:
            logger = GjUtil.get_logger()

        # `max_allowance``: dictionary that `GjVolunteerAllocationGame.max_allowed_days_per_person` returns.
        if not max_allowance_resplvl:
            raise RuntimeError("Field `max_allowance` is empty, which indicates something is wrong...TBD add how to troubleshoot")
        free_workers = []
        fullybooked_workers = []
        overlybooked_workers = []
        logger.debug(f"99 persons: {persons}")
        for worker in persons:
            person_id = worker.id            
            is_exempted = (RespLvl.TOUBAN_EXEMPT in worker.responsibilities)
            msg_responsibility = f", i.e. exempted. Skipping this player." if is_exempted else f""

            if is_exempted:
                # For an exempted worker the following process is not needed so skipping to the next iteration.
                continue

            assigned_dates, assigned_leader, assigned_committee, assigned_noncommittee = GjUtil.get_assigned_dates(
                person_id, dates)
            max_days_incl_overbook = assigned_dates + overbook_allowed_num
            # TODO Right now only considering a single responsibility in the next logic.
            # But a single person can take multiple responsibilities. 
            # E.g. For a person with "committee" in the input data, s/he needs to assume both "committee + leader".
            _stint_already_assigned = max_allowance_resplvl[Consts.ATTR_MAX_STINT_OPPORTUNITIES]
            # If a person's assigned dates is smaller than the responsibility's max occurrence, then this person can take more dates.
            if assigned_dates < _stint_already_assigned:
                free_workers.append(worker)
            elif assigned_dates == _stint_already_assigned:
                fullybooked_workers.append(worker)
            elif max_days_incl_overbook == _stint_already_assigned:
                overlybooked_workers.append(worker)
            elif max_days_incl_overbook < _stint_already_assigned:
                raise ValueError(f"Person ID {person_id} is assigned for '{assigned_dates}' days, which exceeds the limit assigned days={max_days_incl_overbook}. TODO Needs figured out")
            else:
                logger.warning(f"_stint_already_assigned = '{_stint_already_assigned}' not falling under any criteria. Skipping for now.")

            logger.debug(f"Worker name: {worker} {person_id=}, #responsibility IDs: '{len(worker.responsibilities)}'{msg_responsibility}, \
assigned_dates: '{assigned_dates}', _stint_already_assigned: '{_stint_already_assigned}'")
        GjUtil._log_persons_per_bookings(free_workers, fullybooked_workers, overlybooked_workers, msg_prefix="151")
        #if not free_workers:
        #    raise ValueError("All given persons are already assigned to the max number of dates")
        return free_workers, fullybooked_workers, overlybooked_workers

    @staticmethod
    def find_free_workers_per_responsibility(
            required_responsibility_id: RespLvl,
            dates: List[WorkDate],
            persons_bank: PersonBank,
            requirements: DateRequirement,            
            overbook_allowed_num=1,
            logger=None):
        """
        @type responsibility: A specific element in `RespLvl`
        """
        if not logger:  # TODO Remove this if block. This shouldn't be needed.
            logger = GjUtil.get_logger()
        
        persons = []
        # TODO This implementation is VERY adhoc. Better solution is preferred.
        ## Problem aimed: In the input data, "Leader" only exists in a requirement of the days
        #    (i.e. in the input data, no person is defined as "Leader"). This would result in
        #    a leader never been assigned with the implementations where a leader can be assigned
        #    only when the person's responsibility level is also a leader.
        # Proposed solution: Only when the required responsibility is "Leader" AND when a person's responsibility in the intput data is X (depends on the person's role),
        #   replace the person's responsibility level with a leader. Per role:
        #   - Tosho, Safety: Committee
        #   - Hoken: General
        #   The replaced responsibility level must be reverted at the end of the loop.
        for pid, pobj in persons_bank.persons.items():
            logger.debug(f"DEBUG 192 {pid=}, {pobj=}, requested resp ID: {required_responsibility_id}")
            for resp_of_a_person in pobj.responsibilities:
                logger.debug(f"194 Required resp ID: {required_responsibility_id} (type of {type(required_responsibility_id)}) given person's responsibility ID: {resp_of_a_person} (type of {type(resp_of_a_person)})")
                _wanted_found = False

                _org_resp_of_a_person = resp_of_a_person
                if required_responsibility_id == RespLvl.LEADER:
                    if (resp_of_a_person.id == RespLvl.COMMITTEE) and ((requirements.type_duty == Roles_Definition.SAFETY_COMMITEE) or 
                                                                       (requirements.type_duty == Roles_Definition.TOSHO_COMMITEE)):
                        resp_of_a_person = Leader()
                    elif resp_of_a_person.id == RespLvl.GENERAL and (
                                                                     (requirements.type_duty == Roles_Definition.HOKEN_COMMITEE)):
                        resp_of_a_person = Leader()
                    #else:
                    #    raise RuntimeError(f"With {required_responsibility_id=} AND this {resp_of_a_person.id=}, {requirements.type_duty=}, \
#no combo found. TBD better error message/handling needed.")
                    logger.debug(f"193 Required resp is '{RespLvl.LEADER}'. Person's responsibility is overwritten as {resp_of_a_person}")

                if required_responsibility_id == resp_of_a_person.id:
                    logger.debug(f"195 Requested responsibility ID {resp_of_a_person} found in '{pid=}'")
                    persons.append(pobj)
                    _wanted_found = True

                # Reverting temp resp level set earlier in the for loop. This can always be done regardless.
                resp_of_a_person = _org_resp_of_a_person

                if _wanted_found:
                    break
        
        logger.debug("197 max_allowance={}, responsibility: {}".format(persons_bank.max_allowance, required_responsibility_id))
        _allowance_of_responsibility = persons_bank.max_allowance[required_responsibility_id]
        return GjUtil.find_free_workers(dates,
                                        persons,
                                        _allowance_of_responsibility,
                                        overbook_allowed_num=overbook_allowed_num,
                                        logger=logger)

    @staticmethod
    def find_free_workers_general(
            dates: List[WorkDate], persons_bank: PersonBank, overbook_allowed_num=1, logger=None):
        return GjUtil.find_free_workers_per_responsibility(
            RespLvl.GENERAL, dates, persons_bank, overbook_allowed_num, logger)

    @staticmethod
    def find_free_workers_committee(
            dates: List[WorkDate], persons_bank: PersonBank, overbook_allowed_num=1, logger=None):
        return GjUtil.find_free_workers_per_responsibility(
            RespLvl.COMMITTEE, dates, persons_bank, overbook_allowed_num, logger)

    @staticmethod
    def find_free_workers_leader(
            dates: List[WorkDate], persons_bank: PersonBank, overbook_allowed_num=1, logger=None):
        """
        @summary: Logic is identical to `find_free_workers_committee` as of 20250305.
        """
        return GjUtil.find_free_workers_per_responsibility(
            RespLvl.COMMITTEE, dates, persons_bank, overbook_allowed_num, logger)

    def calc_stint(needed_player: int, available_player: int, logger=None) -> Tuple[int, int, int]:
        """
        @summary: Return a set of a few int:
          - #max stint: Max number that each person should be assigned.
          - #available extra: Surplus of persons iff 'needed_player's < 'available_player's.
          - #unlucky: Iff 'available_player's < 'needed_player's, this number is the persons that have to cover extra #days.
        """
        if not logger:
            logger = GjUtil.get_logger()

        available_extra = 0
        unlucky = 0

        if (not needed_player):
            # Depending on the role, it is possible the num of assignee for particular roles to be 0.
            return 0, available_player, unlucky

        if needed_player <= available_player:
            max_stint = 1
            available_extra = available_player - needed_player	
        elif available_player < needed_player:
            max_stint, unlucky = divmod(needed_player, available_player)

        logger.debug(f"needed_player: {needed_player}, available_player: {available_player}\nmax_stint: {max_stint}, available_extra: {available_extra}, unlucky: {unlucky}")
        return max_stint, available_extra, unlucky

    def max_allowed_days_per_person(dates: List[WorkDate], workers: PersonBank, logger=None) -> PersonBank:
        """
        @summary:  Returning 2 sets of info for 3 kinds of responsibilitys (leader, committee, generals):
            - max_stint_*: Maximum number of times each person should be assigned to the correspondent responsibility in the given period.
            - unlucky_*: Number of persons who need to take on the correspondent responsibility once more than `max_*` number.
        @type dates: [n_to_n_matching.WorkDate]
        @return: Dictionary structure should look like this:
            {
                ResponsibilityLevel.LEADER: {ATTR_MAX_OCCURREcNCE: max_leader, ATTR_UNLUCKY_PERSON_NUMS: unlucky_leaders},
                ResponsibilityLevel.COMMITTEE: {ATTR_MAX_OCCURRENCE: max_committee, ATTR_UNLUCKY_PERSON_NUMS: unlucky_committees},
                ResponsibilityLevel.GENERAL: {ATTR_MAX_OCCURRENCE: max_general, ATTR_UNLUCKY_PERSON_NUMS: unlucky_generals},
            }
        @raise ValueError: If not enough number of persons with a responsibility is given in `workers`.
        """
        def _debug_print_max_per_person(*args):
            logger.debug("Debug:\t")
            for arg in args:
                logger.debug(f'\t{arg=}')

        def _log_available_persons(
                dates, needed_leader, needed_committee, needed_general, available_committee, available_general):
            logger.info(f"""
\t#dates {len(dates)} 
\tneeded_leader {needed_leader} needed_committee {needed_committee} needed_general {needed_general}
\tavailable_committee {available_committee} available_general {available_general}""")

        if not logger:
            logger = GjUtil.get_logger()

        # Find the total number of slots need to be filled in all `dates`.
        needed_leader, needed_committee, needed_general = GjUtil.total_slots_required(dates)
        available_committee, available_general, exempted = GjUtil.total_persons_available(workers)
        if not all([available_committee, available_general]):
            raise ValueError(f"Any one of these must not be 0: {available_committee=}, {available_general=}")
        _log_available_persons(
            dates, needed_leader, needed_committee, needed_general, available_committee, available_general)

        try:
            # Calculating maximum stint per person (i.e. #days a person can take at maximum).
            # TODO 20241018 IDK yet if 'divmod(needed_leader, available_committee)' is the right way to calculate tne #stints.
            max_stint_leader, available_extra_leaders, unlucky_leaders = GjUtil.calc_stint(needed_leader, available_committee)
            max_stint_committee, available_extra_committees, unlucky_committees = GjUtil.calc_stint(needed_committee, available_committee)
            max_stint_general, available_extra_generals, unlucky_generals = GjUtil.calc_stint(needed_general, available_general)
        except ZeroDivisionError as e:
            raise ZeroDivisionError("Theres is at least one arg that is zero. {}".format(
                _debug_print_max_per_person(max_stint_leader, unlucky_leaders, max_stint_committee, unlucky_committees, max_stint_general, unlucky_generals))) from e
        max_allowance = {
            RespLvl.LEADER: {
                # TODO IDK if these pre-calculated numbers of Leader role are useful.
                # Might as well want to calculate in the later process when assigning a leader is needed. IDK.
                Consts.ATTR_MAX_STINT_OPPORTUNITIES: max_stint_leader,
                Consts.ATTR_AVAILABLE_EXTRAS: available_extra_leaders,
                Consts.ATTR_UNLUCKY_PERSON_NUMS: unlucky_leaders},
            RespLvl.COMMITTEE: {
                Consts.ATTR_MAX_STINT_OPPORTUNITIES: max_stint_committee,
                Consts.ATTR_AVAILABLE_EXTRAS: available_extra_committees,
                Consts.ATTR_UNLUCKY_PERSON_NUMS: unlucky_committees},
            RespLvl.GENERAL: {
                Consts.ATTR_MAX_STINT_OPPORTUNITIES: max_stint_general,
                Consts.ATTR_AVAILABLE_EXTRAS: available_extra_generals,
                Consts.ATTR_UNLUCKY_PERSON_NUMS: unlucky_generals},
            }
        logger.info("Inside of max_allowance: {}".format(max_allowance))
        # TODO Verify whether input number of players with each role is sufficient to cover all the required roles.
        workers.max_allowance = max_allowance
        return workers

    @staticmethod
    def str_ids(objs) -> str:
        """
        @type objs: Objects of a class that has `id` as an attribute.
        """
        _resps = []
        for obj in objs:
            _resps.append(str(obj.id))
        _str_resps = ",".join(_resps) if _resps else "No ID found."
        return _str_resps


class MaxAllowance():
    def __init__(self, responsibility_lvl: RespLvl, available_extras_persons: int, unlucky_persons: int):
        self._responsibility_lvl = responsibility_lvl
        self._available_extras_persons = available_extras_persons
        self._unlucky_persons = unlucky_persons

    @property
    def responsibility_lvl(self) -> RespLvl:
        return self._responsibility_lvl

    @responsibility_lvl.setter
    def responsibility_lvl(self, value: RespLvl):
        self._responsibility_lvl = value

    @property
    def available_extras_persons(self) -> int:
        return self._available_extras_persons

    @available_extras_persons.setter
    def available_extras_persons(self, value: int):
        self._available_extras_persons = value

    @property
    def unlucky_persons(self) -> int:
        return self._unlucky_persons

    @unlucky_persons.setter
    def unlucky_persons(self, value: int):
        self._unlucky_persons = value
