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
from collections import defaultdict
import pytz
import pandas as pd
from assistance._paths import CAMPAIGN_DATA, MONOREPO


def run_stats():
    stats_path = MONOREPO / "shared" / "jims" / "campaign-overview.csv"

    progression_timing_data = get_progression_stats()
    counts = defaultdict(lambda: defaultdict(lambda: 0))
    tz = pytz.timezone("Africa/Johannesburg")

    for _email, user_data in progression_timing_data.items():
        for key, timestamp in user_data.items():
            dt = datetime.fromtimestamp(timestamp, tz=tz)

            counts[(dt.year, dt.month, dt.day)][key] += 1

    keys = sorted(counts)

    rows = [(key, dict(counts[key])) for key in keys]

    data = {
        "year": [row[0][0] for row in rows],
        "month": [row[0][1] for row in rows],
        "day": [row[0][2] for row in rows],
    }

    for key in [
        "introduction",
        "next-steps",
        "last-reminder",
        "first-follow-up-after-application-start",
    ]:
        column_data = []

        for row in rows:
            try:
                column_data.append(row[1][key])
            except KeyError:
                column_data.append(0)

        data[key] = column_data

    previous_data = pd.read_csv(stats_path)

    df = pd.DataFrame(data)
    ignore_rows = 2
    df = pd.concat((previous_data[0:6], df[ignore_rows:]))

    df.to_csv(stats_path, index=None)  # type: ignore


def get_progression_stats():
    progression_record = (CAMPAIGN_DATA / "jims-ac" / "progression").glob("*/*")
    progression_timing_data = defaultdict(dict)

    for record in progression_record:
        with open(record) as f:
            time = f.read()

        if time == "":
            time = record.stat().st_mtime
        else:
            time = float(time)

        progression_timing_data[record.parent.name.lower()][record.name] = time

    return progression_timing_data
