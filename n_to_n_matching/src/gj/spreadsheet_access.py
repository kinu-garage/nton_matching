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

from abc import ABC, abstractmethod
import openpyxl as pyxl
from openpyxl.cell.cell import Cell as pyxl_Cell

from gj.responsibility import Responsibility, ResponsibilityLevel
from gj.role import Role, Roles_Definition
from gj.util import GjUtil
from n_to_n_matching.person_player import PersonBank, PersonPlayer
from n_to_n_matching.spreadsheet_access import SpreadsheetCell, SpreadsheetRow


class GjRowEntity:
    COL_TITLE_IDS_202407 = {
        2: "id_in_sheet",           # "No"
        3: "grade_class",           # "学年組"
        5: "person_name",           # "氏名"
        6: "guardian_personname",   # "保護者名"
        7: "phone_emergency",       # "当番用TEL"
        8: "email_emergency",       # "当番用メール"
        9: "sibling_2_class",       # "兄姉２"
        10: "sibling_2_personname",  # "兄姉氏名"
        11: "sibling_3_class",       # "兄姉３"
        12: "sibling_3_personname",  # "兄姉氏名"
        13: "sibling_4_class",       # "兄姉４"
        15: "date_assigned_tosho",   # "図書" NOTE: From  15 (図書) to 20 (退学) aren't verified yet as of 20240829.
        16: "date_assigned_hoken",   # "保健"
        17: "date_assigned_patrol",  # "パトロール"
        18: "comment",               # "備考"
        19: "transfered_on",         # "編入"
        20: "terminate_on",          # "退学"
        24: "exempted_on",           # "免除対象"
        25: "selected_as",           # "選出". As of 20240825 no practical usage of this field is found.
        26: "phone_registered",      # "事務局登録TEL"
        27: "email_registered",      # "クラス登録メール"
    }

    def __init__(self, row: SpreadsheetRow, logger_obj=None):
        if type(row) != SpreadsheetRow:
            raise ValueError(f"'row' object must be the type of SpreadsheetRow. Instead, {type(row)} was passed.")
        self._logger = GjUtil.get_logger(__name__, logger_obj)
        if not row:
            self._logger.warning(f"'row' object is empty. Finishing creating an object without filling with the values.")
            pass
        else:
            self._raw_row = row

        self._is_title_row = True if row.is_title_row else False
        self._gj_row = self.parse_xls_row(row, self.COL_TITLE_IDS_202407)
    
    def parse_xls_row(self, row, col_title_definition=COL_TITLE_IDS_202407):
        """
        @description: Evaluate each cell from the row object, find a cell that matches the column ID, then sets the cell's value.
        @type row: SpreadsheetRow
        @type col_title_definition: dict
        @return: row object filled with the values in the corresponding column index.
        """
        ss_row = []
        for cell in row.cells:
            self._logger.debug(f"cell.column: {cell.column}")
            cell_title = ""
            try:
                cell_title = col_title_definition[cell.column]
            except KeyError as e:
                self._logger.debug(f"Skipping this column. cell.column :{cell.column} is either not used or its definition not present in title definition.")                
            # TODO Roles need special treatment; In the spreadsheet, roles are distributed in multiple columns and value of the cells in each col
            #   are meant to be the date the person is assigned to each role. While this design makes sense from spreadsheet user's usecase,
            #   it doesn't provide convenience for this tool's usecases.
            #   To mitigate, add a special cell to the row object that conveys the type of role.
            ss_cell = SpreadsheetCell(cell, cell_title)
            # TODO Looks like the usage of this ss_row list assumes the order of elements are fixed, however,
            # the current implementation doesn't guarantee the order. Needs a better impl.
            ss_row.append(ss_cell)

    def _get_value_from_gj_row(self, col_id):
        """
        @todo # TODO Identifying the column by specifying column ID is very adhoc. Need more standardized, robust way.
        """
        for cell in self._raw_row.cells:  # type(cell) == openpyxl.cell.cell.Cell
            if cell.column == col_id:
                return cell.value

    @property
    def row_id(self):
        return self._raw_row.row_id

    @property
    def exempted_on(self):
        """
        @todo # TODO Identifying the column by specifying column ID is very adhoc. Need more standardized, robust way.
        """
        return self._get_value_from_gj_row(24)

    @property
    def grade_class(self):
        """
        @todo # TODO Identifying the column by specifying column ID is very adhoc. Need more standardized, robust way.
        """
        return self._get_value_from_gj_row(3)

    @property
    def id_in_sheet(self):
        """
        @todo # TODO Identifying the column by specifying column ID is very adhoc. Need more standardized, robust way.
        """
        return self._get_value_from_gj_row(2)

    @property
    def person_name(self):
        """
        @todo # TODO Identifying the column by specifying column ID is very adhoc. Need more standardized, robust way.
        """
        name = self._get_value_from_gj_row(5)
        if not name:
            raise ValueError("person_name is empty.")
        return name

    @property
    def phone_emergency(self):
        """
        @todo # TODO Identifying the column by specifying column ID is very adhoc. Need more standardized, robust way.
        """
        return self._get_value_from_gj_row(7)

    @property
    def email_emergency(self):
        """
        @todo # TODO Identifying the column by specifying column ID is very adhoc. Need more standardized, robust way.
        """
        return self._get_value_from_gj_row(8)


class GjToubanAccess:
    """
    @todo: Spreadsheet format is tied to .xls as of 2024/08 but no guarantee to stick with it in the future (so better keep that in mind when making design decisions).
    """
    SUFFIX_MASTERSHEET = "マスター"
    MASTERSHEET_2024 = "2024当番マスター"
    # ID of the column in a spreadsheet that shows the responsibilitys that the exemption rule is to eb applied for certain assignment.
    COL_ROW_EXEMPT = "X"
    NAME_TOSHOIIN = "図書委員"
    LIST_AVAILABLE_TARGET = [NAME_TOSHOIIN]

    def __init__(self, logger_obj=None):
        self._logger = GjUtil.get_logger(__name__, logger_obj)
        self._touban_master_sheet = None

    @staticmethod
    def get_a_sheet_by_name(workbook, sheet_name):
        """
        @type workbook: openpyxl.workbook.workbook.Workbook
        @param sheet_name: The full name of the sheet to obtain.
        @rtype: Worksheet
        """
        for sheet in workbook:
            if sheet.title == sheet_name:
                return sheet
        raise LookupError(f"Requested sheet '{sheet_name}' not found in the given workbook obj.")

    def get_a_spread_sheet(self, path_xls, sheet_name=MASTERSHEET_2024):
        # 'data_only=True' is needed in order to read a value from each cell, not the macro formula.
        # See https://stackoverflow.com/a/35624928/577001
        wb = pyxl.load_workbook(path_xls, data_only=True)
        sheet = self.get_a_sheet_by_name(wb, sheet_name)
        if not sheet:
            raise ValueError("In the workbook '{}', no sheet found that has the name '{}'".format(
                wb.title, sheet_name))
        return sheet

    @staticmethod
    def get_a_sheet(workbook, suffix_master_file):
        """
        @deprecated: Picking up a sheet just by a suffix of the sheet name may not be robust.
        @type workbook: openpyxl.workbook.workbook.Workbook
        @rtype: Worksheet
        """
        for sheet in workbook:
            if sheet.title.endswith(suffix_master_file):
                return sheet

    def get_touban_master_sheet(self, path_xls, sheet_name=MASTERSHEET_2024):
        if not path_xls:
            raise ValueError("Either/Both args 'path_xls' and/or 'sheet_struct' is empty.")
        sheet = self.get_a_spread_sheet(path_xls, sheet_name)
        return sheet

    def get_candidates(self, sheet, key_target):
        """
        @param key_target: E.g. NAME_TOSHOIIN
        @rtype: 1) [[cell]], 2) [int]
        """
        if key_target not in self.LIST_AVAILABLE_TARGET:
            raise ValueError("The passed key_target='{}' is not present in the available targets '{}'.".format(
                key_target, self.LIST_AVAILABLE_TARGET))
        
        rows_matched = []
        # ID of the rows that meet the search criteria
        row_ids = []
        for cell in sheet[self.COL_ROW_EXEMPT]:
            if cell.value == key_target:
                row_ids.append(cell.row)  # 'row' is not intuitive way to get row number but it works.
        self._logger.info(f"row_ids: {row_ids}")    
        # Haven't found openpyxl API way of knowing the row number,
        # so maually figuring here...
        for row_id in row_ids:
            row = sheet[row_id]
            # Verify the row ID matches with what we want.
            if row[0].row == row_id:  # Again, 'row' returning row ID is unintuitive, but this is the way..
                rows_matched.append(sheet[row_id])
        self._logger.debug(f"Rows matched: {rows_matched}")
        return rows_matched, row_ids

    def gj_xls_to_personobj(self, path_to_xls, title_row=3):
        """
        @description Convert GJLS' .xls specific format to the format this package can handle.

            Assumption for the spreadsheet format:
            - Titles of cells are defined in a single row.
            - Rows before the title row does not contain any info that needs to be taken into consideration for creating person info.

        @type path_to_xls: str
        @param title_row: The row where the values represent the type of the info that the cells under each column carries.
          As of 20240827, this title row must be a single row (i.e. Cases where titles are written in multiple rows are not yet supported).
        @rtype: dict
        @return: n_to_n_matching.person_player.PersonBank
        """
        persons = []
        # Read .xls file into a Python objects
        rows_xls_obj = self.get_touban_master_sheet(path_to_xls)
        # Each row should obtain the ID number from a cell in each row in the spreadsheet,
        # but how reliably maintained the ID in the spreadsheet is unknown. So here
        # maintaining ID as well. This is just a backup.
        _row_count = 1
        # Parse each row object, create 'PersonPlayer' object per each person.
        for row_pyxl in rows_xls_obj:
            # If the row is title, set title flag.
            is_title_row = True if row_pyxl[0].row == title_row else False
            # If the row is earlier thatn title row, do not look for person info.
            if row_pyxl[0].row <= title_row:
                continue
            row = GjRowEntity(SpreadsheetRow(row_pyxl, is_title_row), self._logger)
            # Identify GJ role(s), and deduce the responsibility from the role(s).
            a_role = Role(row.exempted_on)
            _responsibility = None
            try:
                # TODO Assign role in addition to responsibility, for Tosho, Patrol.
                #_responsibility_id = self.match_responsibility(a_role)
                _responsibility = GjUtil.corresponding_responsibility(a_role)
            except ValueError as e:
                self._logger.error(f"Column #{row.row_id}. Skipping as an unknown error occurred. {str(e)}")
                continue

            if row.id_in_sheet:
               _family_id_in_sheet = int(row.id_in_sheet)
            else:
                _family_id_in_sheet = _row_count
            self._logger.debug(f"_family_id_in_sheet: {_family_id_in_sheet}")

            try:
                _student_fullname = row.person_name
            except ValueError as e:
                self._logger.debug(f"Student name empty. Likely empty row. Skipping.")
                continue
  
            # TODO Not fully sure if 'exempted_on' is the correct selection.
            #responsibility = GjUtil.gen_responsibility(row.exempted_on)

            person = PersonPlayer(
                id =_family_id_in_sheet,
                name =_student_fullname,
                email_addr = row.email_emergency,
                phone_num = row.phone_emergency,
                grade_class = row.grade_class,
                roles=[a_role],
                # 2024/08 'children_ids' attribute was originally created without the knowledge of how students/guardians are 
                # grouped into a family info. Now that it's more known, 'children_ids' doesn't seem to be needed, hence
                # setting 'None' here
                children_ids = None,
                responsibilities=[_responsibility],
            )
            self._logger.debug(f"person ID: {person.id}, name: {person.name}")
            persons.append(person)
            _row_count += 1
        self._logger.debug(f"Persons: {persons}, size of persons: {len(persons)}")
        return PersonBank(persons)

    @abstractmethod
    def match_responsibility(self, a_role_id: Roles_Definition=""):
        """
        @deprecated: Potentially this method may no longer needed, replaced by GjUtil.corresponding_responsibility().
        """
        raise NotImplementedError()


class GjToubanAccess2024(GjToubanAccess):
    def match_responsibility(self, a_role_id: Roles_Definition="") -> Responsibility:
        """
        @description: (Overriding abstract method)
        @raise ValueError
        """
        _responsibility_id = -1
        if ((a_role_id == Roles_Definition.GAKYU_COMMITEE) or
            (a_role_id == Roles_Definition.GYOJI_COMMITEE) or
            (a_role_id == Roles_Definition.TOUBAN_COMMITEE) or
            (a_role_id == Roles_Definition.UNDOKAI_COMMITEE) or 
            (a_role_id == Roles_Definition.UNEI_COMMITEE)
            ):
            _responsibility_id = ResponsibilityLevel.TOUBAN_EXEMPT.value
        elif ((a_role_id == Roles_Definition.TOSHO_COMMITEE) or
              (a_role_id == Roles_Definition.SAFETY_COMMITEE)
              ):
            _responsibility_id = ResponsibilityLevel.COMMITTEE.value
        elif (
            # Handling of photo clue might be still NOT lucid as of 2024/08. 
            # Ref. https://groups.google.com/a/gjls.org/g/touban-group/c/8ikrmPQ15lk
            (a_role_id == Roles_Definition.PHOTO_CLUE) or
            (not a_role_id)):
            _responsibility_id = ResponsibilityLevel.GENERAL.value
        else:
            raise ValueError(f"""Obtained role '{a_role_id}' does NOT match any rule.
Make sure the input value conforms to the string expression this tool supports.
It is likely that the input values come all the way down from the input 'master' file (likely in '.xlsx' format).
So if that .xlsx file is an input data for your appliaction, check to see if there's any
                             """)
        return _responsibility_id
