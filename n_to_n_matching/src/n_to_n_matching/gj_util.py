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

from n_to_n_matching.workdate_player import WorkDate


class GjUtil:
    @staticmethod
    def _get_logger():
        return logging.getLogger(__name__)

    @staticmethod
    def get_assigned_dates(person_id, dates, logger=None):
        """
        @summary Returns the number that a person of `person_id` is assigned to
          in the period that is given to the tool, regardless the type
          of the role.
        @type dates: [WorkDate]
        @type logger: logging.Logger
        @rtype int, int, int, int
        @return assign_count, assigned_leader, assigned_committee, assigned_noncommittee
        """
        if not logger:
            logger = GjUtil._get_logger()
        if (not isinstance(person_id, int)) or (not isinstance(dates[0], WorkDate)):
            raise TypeError(f"One of the args' type is incompatible. person_id: '{type(person_id)}', date[0]: '{type(dates[0])}'")

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
