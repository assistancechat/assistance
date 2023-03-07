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


# TODO: Handle conditionals, pull in already filled out components and
# only print parts of the form that have not yet been completed.
def walk_and_build_remaining_form_fields(
    field: dict[str, dict | str], parents=None, form_text=""
):
    if parents is None:
        parents = []

    for key, item in field.items():
        if len(key) == 2 and key.startswith("h"):
            header_level = int(key[1])
            if form_text != "":
                form_text += "\n"

            form_text += "#" * header_level + f" {item}\n\n"

            continue

        if isinstance(item, dict):
            if "conditional" in item:
                continue

            if "optional" in item and item["optional"]:
                continue

            form_text = walk_and_build_remaining_form_fields(
                item, parents=parents + [key], form_text=form_text
            )

            continue

        if key == "text":
            record = ".".join(parents)
            form_text += f"- {record}: {item}\n"

    return form_text
