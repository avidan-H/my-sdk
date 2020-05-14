from typing import Tuple

from demisto_sdk.commands.common.hook_validations.dashboard import \
    DashboardValidator
from demisto_sdk.commands.common.tools import print_error
from demisto_sdk.commands.format.format_constants import (ERROR_RETURN_CODE,
                                                          SKIP_RETURN_CODE,
                                                          SUCCESS_RETURN_CODE)
from demisto_sdk.commands.format.update_generic_json import BaseUpdateJSON


class DashboardJSONFormat(BaseUpdateJSON):
    """DashboardJSONFormat class is designed to update dashboard JSON file according to Demisto's convention.

       Attributes:
            input (str): the path to the file we are updating at the moment.
            output (str): the desired file name to save the updated version of the YML to.
    """

    def __init__(self, input: str = '', output: str = '', path: str = '', from_version: str = '', no_validate: bool = False):
        super().__init__(input, output, path, from_version, no_validate)

    def update_id(self):
        """Updates the id to be the same as name ."""

        print('Updating ID')
        if 'name' not in self.data:
            print_error(f'Missing "name" field in file {self.source_file} - add this field manually')
            raise Exception(f'Missing "name" field in file {self.source_file} - add this field manually')
        self.data['id'] = self.data['name']

    def run_format(self) -> int:
        try:
            super().update_json()
            self.default_description()
            self.update_id()
            super().save_json_to_destination_file()
            return SUCCESS_RETURN_CODE
        except Exception:
            return ERROR_RETURN_CODE

    def default_description(self):
        if not self.data.get("description", ""):
            self.data["description"] = ""
        if not self.data.get("isPredefined", ""):
            self.data["isPredefined"] = True

    def format_file(self) -> Tuple[int, int]:
        """Manager function for the integration YML updater."""
        format = self.run_format()
        if format:
            return format, SKIP_RETURN_CODE
        else:
            return format, self.initiate_file_validator(DashboardValidator)
