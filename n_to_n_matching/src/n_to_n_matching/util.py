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
import logging
import urllib
import yaml


class Util:
    @staticmethod
    def get_logger(name_logger="", logger_obj=None):
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
