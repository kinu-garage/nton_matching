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

import datetime
import dateutil
import logging
from typing import List
import urllib
import yaml


class Util:
    @staticmethod
    def get_logger(name_logger="", logger_obj: logging.Logger=None) -> logging.Logger:
        if not name_logger:
            name_logger = __name__
        if logger_obj:
            return logger_obj
        logger = logging.getLogger(name_logger)
        _stream_handler = logging.StreamHandler()
        _stream_handler.setLevel(logging.INFO)
        _stream_format = logging.Formatter('%(name)s - %(levelname)s: %(message)s')
        _stream_handler.setFormatter(_stream_format)
        # TODO For some reason, setting the log level in a handler herelogger_obj
        # doesn't seem to take effect. So setting basicConfig.
        logging.basicConfig(level=logging.INFO)
        #logger.addHandler(_stream_handler)
        return logger
    
    @staticmethod
    def read_yaml_to_dict(path_prefix, filename):
        """
        @description: Read in the YAML data from the URL.
        @return: Python's dict object 
        """
        url = "/".join((path_prefix, filename))
        with urllib.request.urlopen(url) as response:
            dictionary = yaml.safe_load(response.read())
        return dictionary

    @staticmethod
    def validate_date_str(date_text):
        try:
            datetime.date.fromisoformat(date_text)
        except ValueError:
            raise ValueError("'{}' is incorrect data format, should be YYYY-MM-DD".format(date_text))

    @staticmethod
    def create_date_from_mmdd(mmdd_string: str, year: int=datetime.date.today().year) -> datetime.date:
        """
        @summary: Creates a `datetime.date` object from a string in "mm/dd" format.
        @param year: The year to use for the date. Defaults to the current year.
        """
        try:
            # Combine the mm/dd string with the provided year
            full_date_string = f"{mmdd_string}/{year}"
            # Parse the full date string into a datetime object
            datetime_object = datetime.datetime.strptime(full_date_string, "%m/%d/%Y")
            # Extract the date component
            return datetime_object.date()
        except ValueError:
            print(f"Error: Invalid date format for '{mmdd_string}'. Please use 'mm/dd'.")
            return None

    @staticmethod
    def create_date_from_str(
        date_string: str,
        year: int=0,
        months_in_subsequent_year: List[int]=[1, 2, 3],
        logger_obj: logging.Logger=None) -> datetime.date:
        """
        @summary: Creates a `datetime.date` object from a string in various format using `dateutil.parser.parse`.
          Some custom logics:
          - If year is not found in `date_string` AND `year` is 0, the current year will be used.
          - If the month in the given str is in the list `months_in_subsequent_year`, the year will be incremented by 1.
        @param months_in_subsequent_year: If None or empty list, year will not be automatically incremented.
        """
        if not logger_obj:
            logger_obj = Util.get_logger(__name__)
        
        try:
            # Parse the full date string into a datetime object
            date_obj = dateutil.parser.parse(date_string).date()
            # Extract the date component
        except ValueError:
            raise ValueError(f"Error: Invalid date format for '{date_string}'. Use 'mm/dd/yy'.")

        if (year != 0) and (date_obj.year != year):
            date_obj = date_obj.replace(year=year)

        if months_in_subsequent_year and (date_obj.month in months_in_subsequent_year):
            _year = date_obj.year + 1
            date_obj = date_obj.replace(year=_year)
        return date_obj