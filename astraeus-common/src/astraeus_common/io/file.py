import json
from typing import Callable, List

import structlog


class File:
    file_path: str

    def __init__(self, file_path: str):
        self.file_path = file_path
        self._log = structlog.get_logger()

    def read_json_file(self) -> List[dict]:
        """
        Read a JSON file and return a list of dictionaries.

        :return: A list of dictionaries containing the data from the JSON file.
        """
        data = []
        try:
            with open(self.file_path) as json_file:
                self._log.info(f'Reading json file {self.file_path}')
                count = 0
                for row in json_file:
                    count += 1
                    if count % 100 == 0:
                        self._log.info(f'Reading line {count}')
                    data.append(json.loads(row))
        except Exception as err:
            self._log.error(f"Error while reading json file: {err}")

        return data

    def read_json_file_and_exec(self, function: Callable) -> None:
        """
        Read a JSON file and execute a given function for every batch of rows.

        :param function: The function to be executed for every batch of rows.
        :type function: Callable
        """
        try:
            with open(self.file_path) as json_file:
                self._log.info(f'Reading json file {self.file_path}')
                row_list = list()
                for no_row, row in enumerate(json_file):
                    row_list.append(json.loads(row))
                    if no_row % 100 == 0:
                        function(row_list)
                        row_list = []

        except Exception as err:
            self._log.error(f"Error while reading json file: {err}")
