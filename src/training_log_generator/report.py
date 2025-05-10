import pandas as pd
from typing import Dict

class ReportGenerator:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def compile_report(self) -> Dict[str, Dict[str, list]]:
        report = {}
        grouped = self.data.groupby(["Date", "am_pm"])

        for (date, am_pm), group_df in grouped:
            if date not in report:
                report[date] = {"morning": [], "afternoon": []}

            for _, row in group_df.iterrows():
                # print(row)
                run_info = {"Time": row["Time"], "Distance": row["Distance"], "Pace": row["Avg Pace"]}
                report[date][am_pm].append(run_info)

        return report
