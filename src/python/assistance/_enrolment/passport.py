# Copyright (C) 2023 Assistance.Chat contributors

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import datetime
from typing import TypedDict

from passporteye import read_mrz


class PassportDetails(TypedDict):
    first_name: str
    middle_names: str
    family_name: str
    date_of_birth: str
    nationality: str
    passport_number: str
    passport_expiry_date: str


def get_fields_from_passport(passport_path: str) -> PassportDetails:
    """Extracts data from a passport image.

    Args:
        passport_path (str): The path to the passport image.

    Returns:
        dict: A dictionary of the extracted data.
    """
    passport_results = read_mrz(passport_path, extra_cmdline_params="legacy")

    results_as_dict: dict[str, str] = passport_results.to_dict()

    names = results_as_dict["names"]
    split_names = names.split(" ")
    first_name = split_names[0].capitalize()

    if len(split_names) > 1:
        middle_names = " ".join([item.capitalize() for item in split_names[1:]])
    else:
        middle_names = ""

    family_name = results_as_dict["surname"].capitalize()
    date_of_birth = _convert_date_to_iso_format(results_as_dict["date_of_birth"])

    nationality = results_as_dict["nationality"]
    passport_number = results_as_dict["number"]
    passport_expiry_date = _convert_date_to_iso_format(
        results_as_dict["expiration_date"]
    )

    results: PassportDetails = {
        "first_name": first_name,
        "middle_names": middle_names,
        "family_name": family_name,
        "date_of_birth": date_of_birth,
        "nationality": nationality,
        "passport_number": passport_number,
        "passport_expiry_date": passport_expiry_date,
    }

    return results


def _convert_date_to_iso_format(date: str) -> str:
    """Converts a date from the passport format to ISO format.

    Args:
        date (str): The date in the passport format.

    Returns:
        str: The date in ISO format.
    """
    return datetime.strptime(date, "%y%m%d").strftime("%Y-%m-%d")
