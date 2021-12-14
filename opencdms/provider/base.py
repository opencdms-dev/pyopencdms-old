# =================================================================
#
# Authors: Ian Edwards
#
# Copyright (c) 2020, OpenCDMS Project
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# =================================================================
from abc import ABC, abstractmethod
import logging
from typing import Dict, Any, Union

LOGGER = logging.getLogger(__name__)


class CDMSProvider(ABC):
    """Generic CDMS Provider Abstract Base Class"""
    @abstractmethod
    def list(
        self,
        model_name: str,
        query: Dict[str, Dict[str, Any]],
        limit, offset
    ):
        """
        Takes a model name for a specific provider and a query parameter
        which looks like this:

        {
            "column_name": {
                "operator": "one of <, >, <=, >=, =,
                 contains, starts_with, ends_with"
            }
        }

        """
        raise NotImplementedError

    @abstractmethod
    def create(self, model_name: str, data: Dict) -> Any:
        raise NotImplementedError

    @abstractmethod
    def get(self, model_name: str, unique_id: Dict[str, Union[str, int]]):
        raise NotImplementedError

    @abstractmethod
    def update(
        self,
        model_name: str,
        unique_id: Dict[str, Union[str, int]],
        data: Dict
    ) -> Any:
        raise NotImplementedError

    @abstractmethod
    def delete(self, model_name: str, unique_id: Dict[str, Union[str, int]]):
        raise NotImplementedError


