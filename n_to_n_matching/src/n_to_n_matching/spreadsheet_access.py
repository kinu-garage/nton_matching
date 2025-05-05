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

from collections import OrderedDict
from openpyxl.cell.cell import Cell as pyxl_Cell

from n_to_n_matching.util import Util


class Cell:
    """
    @description: Funtionality-wise this class should be similar to openpyxl.cell.cell.Cell but
        this class does not depend on openpyxl.

        One of the main advantages over a row implementation in the existing libraries is that
        each cell knows what type of info is stored in it, i.e. title of the
        column of the cell that is typically defined in the early number of row(s).
        This comes with downside i.e. when the spreadhseet's structure gets updated later on so that the type of info stored in the cell
        _can_ change. As of 20240827 the implementation does not capture that usecase.
    @todo Move out of GJ realm. This class must be generic.
    """
    def __init__(self):
        self._row_id = -1
        self._col_id = -1
        self._value = None

    @property
    def row_id(self):
        return self._row_id

    @row_id.setter
    def row_id(self, value):
        self._row_id = value

    @property
    def col_id(self):
        return self._col_id

    @col_id.setter
    def col_id(self, value):
        self._col_id = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    def init(self, row_id, col_id, val):
        self.row_id(row_id)
        self.col_id(col_id)
        self.value(val)


class Row:
    """
    @description: Represents a row in a spreadsheet, without relying on existing libraries that provides spreadsheet feature.
    """
    def __init__(self, row_id=-1, logger_obj=None):
        """
        @type cells: [Cell]
        @param row_id: If non -1 value is passed, this value will be added to all the cells:
           - that are newly generated in the object of this class.
           - that are passed to this class IF no row ID is set yet.
        """
        self._logger = Util.get_logger(__name__, logger_obj)
        self._row_id = row_id
        self._cells_in_a_row = OrderedDict()

    @property
    def row_id(self):
        return self._row_id

    @row_id.setter
    def row_id(self, value):
        self._row_id = value

    def set_row_by_cells(self, cells):
        """
        @description: If each cell comes with 'col_id' in, then a cell will be put in the specific index in the ordered dict.
          Otherwise, a cell will be placed at the index in the passed 'cells'.
        @type cells: [Cell]
        """
        for id, cell in enumerate(cells):
            _col_id = cell.col_id
            if not _col_id:
                self._cells_in_a_row[id] = cell
            else:
                self._cells_in_a_row[_col_id] = cell

    def set_row_by_strs(self, title_strs):
        """
        @type title_strs: [str]
        """
        for col_id, title in enumerate(title_strs):
            c = Cell()
            c.col_id = col_id
            c.row_id = self.row_id
            c.value = title
            self._cells_in_a_row[col_id] = c
        self._logger.debug(f"self._cells_in_a_row: {self._cells_in_a_row}")

    def get_col_title(self, col_id):
        return self._cells_in_a_row[col_id].value

    def get_col_id(self, col_title):
        for key, val in self._cells_in_a_row.items():
            self._logger.info(f"k: {key}, v.col_id: {val.col_id}, v.row_id: {val.row_id}, title: {val.value}")
            if val.value == col_title:
                return val.col_id
        return -1


class SpreadsheetCell(pyxl_Cell):
    __slots__ = ('_title_value')

    def __init__(self, cell_obj, title_val=""):
        super().__init__(cell_obj)
        self._title_value = title_val


class SpreadsheetRow():
    def __init__(self, row: pyxl_Cell, is_title_row=False):
        """
        @param is_title_row: Bool to show if the row represents title of the cells below each cell or not.
           This can only be set upon initialization, so no setter is defined.
        """
        self._cells = row
        self._is_title_row = is_title_row

    @property
    def cells(self) -> pyxl_Cell:
        return self._cells

    @cells.setter
    def cells(self, value):
        self._cells = value

    @property
    def is_title_row(self):
        return self._is_title_row

    @property
    def row_id(self):
        return self._cells[0].row  # This impl may look rather adhoc and unstable, but AFAIK this is the official way to get a row ID in openpyxl.
