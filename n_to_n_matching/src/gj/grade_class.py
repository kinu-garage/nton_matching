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

from enum import Enum
import logging
from typing import List, Type

from n_to_n_matching.util import Util as NtonUtil


class GjGrade(Enum):
    KINDER_YOCHIEN_YURI = "幼 ゆり"
    KINDER_YOCHIEN_MOMO = "幼 もも"
    ELEM_SHOU_1_1 = "小1－1"
    ELEM_SHOU_1_2 = "小1－2"
    ELEM_SHOU_1_3 = "小1－3"
    ELEM_SHOU_2_1 = "小2－1"
    ELEM_SHOU_2_2 = "小2－2"
    ELEM_SHOU_2_3 = "小2－3"
    ELEM_SHOU_3_1 = "小3－1"
    ELEM_SHOU_3_2 = "小3－2"
    ELEM_SHOU_3_3 = "小3－3"
    ELEM_SHOU_4_1 = "小4－1"
    ELEM_SHOU_4_2 = "小4－2"
    ELEM_SHOU_4_3 = "小4－3"
    ELEM_SHOU_5_1 = "小5－1"
    ELEM_SHOU_5_2 = "小5－2"
    ELEM_SHOU_5_3 = "小5－3"
    ELEM_SHOU_6_1 = "小6－1"
    ELEM_SHOU_6_2 = "小6－2"
    ELEM_SHOU_6_3 = "小6－3"
    MIDD_CHUU_1_1 = "中1－1"
    MIDD_CHUU_1_2 = "中1－2"
    MIDD_CHUU_2_1 = "中2－1"
    MIDD_CHUU_2_2 = "中2－2"
    MIDD_CHUU_3_1 = "中3－1"
    HIGH_KOU_1_1 = "高1－1"
    HIGH_KOU_2_1 = "高2－1"

    def __str__(self):
        return self.value


class GjGradeGroup(Enum):
    KINDER_YOCHIEN = [GjGrade.KINDER_YOCHIEN_MOMO, GjGrade.KINDER_YOCHIEN_YURI]
    ELEM_SHOU_1STG = [GjGrade.ELEM_SHOU_1_1, GjGrade.ELEM_SHOU_1_2, GjGrade.ELEM_SHOU_1_3]
    ELEM_SHOU_2STG = [GjGrade.ELEM_SHOU_2_1, GjGrade.ELEM_SHOU_2_2, GjGrade.ELEM_SHOU_2_3]
    ELEM_SHOU_3STG = [GjGrade.ELEM_SHOU_3_1, GjGrade.ELEM_SHOU_3_2, GjGrade.ELEM_SHOU_3_3]
    ELEM_SHOU_4STG = [GjGrade.ELEM_SHOU_4_1, GjGrade.ELEM_SHOU_4_2, GjGrade.ELEM_SHOU_4_3]
    ELEM_SHOU_5STG = [GjGrade.ELEM_SHOU_5_1, GjGrade.ELEM_SHOU_5_2, GjGrade.ELEM_SHOU_5_3]
    ELEM_SHOU_6STG = [GjGrade.ELEM_SHOU_6_1, GjGrade.ELEM_SHOU_6_2, GjGrade.ELEM_SHOU_6_3]
    ELEM_SHOU_LOWER = [ELEM_SHOU_1STG, ELEM_SHOU_2STG, ELEM_SHOU_3STG]
    ELEM_SHOU_UPPER = [ELEM_SHOU_4STG, ELEM_SHOU_5STG, ELEM_SHOU_6STG]
    ELEM_SHOU = [ELEM_SHOU_LOWER, ELEM_SHOU_UPPER]
    MIDD_CHUU = [GjGrade.MIDD_CHUU_1_2, GjGrade.MIDD_CHUU_1_2, GjGrade.MIDD_CHUU_2_1, GjGrade.MIDD_CHUU_2_2, GjGrade.MIDD_CHUU_3_1]
    HIGH_KOU = [GjGrade.HIGH_KOU_1_1, GjGrade.HIGH_KOU_2_1]
    MIDD_HIGH_CHUKOU = [MIDD_CHUU, HIGH_KOU]


class GradeUtil():
    @staticmethod
    def find_grade(grade: str, logger=None) -> GjGrade:
        if not logger:
            logger = NtonUtil.get_logger()
        
        for gr in GjGrade:
            logger.debug(f"Given grade: {grade}")
            if grade == gr.value:
                return gr
        return None

    @staticmethod
    def included_grade(in_grade: GjGrade, group, logger=None) -> bool:
        """
        @summary Judge if the given `in_grade` is included in the given `group`.
        @param group: The type can be either `GjGradeGroup`, `GjGrade`, or `str`.
        """
        if not logger:
            logger = NtonUtil.get_logger()
        
        _included = False
        logger.info(f"87\t{type(in_grade)=}, {in_grade=}.\n\t{type(group)=}, {group=}")
        if isinstance(group, GjGradeGroup):
            subgroup = group.value
            _included = GradeUtil.included_grade(in_grade, subgroup)
        elif isinstance(group, List):  # This if clause is checking `List[GjGradeGroup]`,
                                     # but just checking `List` avoiding Python's complaints.
            if (in_grade in group):
                logger.debug("88")
                _included = True
            else:
                logger.debug("89")
                for subgroup in group:
                    logger.debug("87")
                    _included = GradeUtil.included_grade(in_grade, subgroup)
                    if _included:
                        logger.debug("86")
                        break
        elif isinstance(group, GjGrade):
            subgroups: List[GjGrade] = group.value
            logger.debug("85")
            if in_grade == subgroups:
                logger.debug("84")
                _included = True
            return _included
        elif isinstance(group, str):
            logger.debug("83")
            if in_grade.value == group:
                logger.debug("82")
                _included = True
            return _included

        logger.debug("81")
        return _included

