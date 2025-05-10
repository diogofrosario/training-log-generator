import pandas as pd
from datetime import datetime, timedelta

import tkinter as tk
from tkinter import filedialog
from typing import Dict

from docxtpl import DocxTemplate

NUMBER_OF_DAYS = 6

class DataLoader:
    def __init__(self, file_path: str, start_day: str, number_of_days: int):
        self.file_path = file_path
        self.start_day = start_day
        self.number_of_days = number_of_days
        self.data = None

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(self.file_path)
        self.data = self.__preprocess(df)
        return self.data

    def __preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            df = self.__create_date_and_time_columns(df)
            df = self.__filter_by_date(df)
        except KeyError:
            df = self.__rename_columns_for_portuguese(df)
            df = self.__create_date_and_time_columns(df)
            df = self.__filter_by_date(df)
        df["am_pm"] = df["Time_of_Day"].apply(self.__morning_or_afternoon)
        return df

    def __rename_columns_for_portuguese(self, df: pd.DataFrame) -> pd.DataFrame:
        df.rename(columns={"Data": "Date", "Distância": "Distance", "Tempo": "Time", "Ritmo médio": "Avg Pace"}, inplace=True)
        return df

    def __create_date_and_time_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df["Date"] = pd.to_datetime(df["Date"])
        df["Time_of_Day"] = df["Date"].dt.time
        df["Date"] = df["Date"].dt.date
        return df

    def __filter_by_date(self, df: pd.DataFrame) -> pd.DataFrame:
        start_datetime = pd.to_datetime(self.start_day)
        date_filter = start_datetime - pd.Timedelta(days=self.number_of_days)
        return df[(df["Date"] >= date_filter.date()) & (df["Date"] <= start_datetime.date())]

    @staticmethod
    def __morning_or_afternoon(time: pd.Timestamp) -> str:
        return "morning" if time.hour < 12 else "afternoon"

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
                run_info = {"Time": row["Time"], "Distance": row["Distance"], "Pace": row["Avg Pace"]}
                report[date][am_pm].append(run_info)

        return report

class TemplateRenderer:
    def __init__(self, template_path: str):
        self.template_path = template_path

    def render_report(self, report: Dict[str, Dict[str, list]], output_path: str) -> None:
        doc = DocxTemplate(self.template_path)
        context = self.__prepare_context(report)
        doc.render(context)
        doc.save(output_path)

    def __prepare_context(self, data: Dict[str, Dict[str, list]]) -> Dict[str, str]:
        context = {}
        days_of_week = [
            "MONDAY",
            "TUESDAY",
            "WEDNESDAY",
            "THURSDAY",
            "FRIDAY",
            "SATURDAY",
            "SUNDAY",
        ]
        start_date = list(data.keys())[0]
        total_distance = 0.0

        for i, day in enumerate(days_of_week):
            current_date = start_date + timedelta(days=i)
            date_str = current_date.strftime("%Y-%m-%d")

            morning_data = data.get(current_date, {}).get("morning", [])
            afternoon_data = data.get(current_date, {}).get("afternoon", [])

            # when there are more than one run in a morning or afternoon (workouts with warm up, main workout, cool down)
            # the order of the activities would should in the incorrect order so we reverse the list to show the correct order
            if len(morning_data) > 1:
                morning_data = morning_data[::-1]

            if len(afternoon_data) > 1:
                afternoon_data = afternoon_data[::-1]

            morning_time = (
                ", ".join([item["Time"] for item in morning_data]) if morning_data else ""
            )
            morning_dist = (
                ", ".join([str(item["Distance"]) for item in morning_data])
                if morning_data
                else ""
            )
            morning_pace = (
                ", ".join([item["Pace"] for item in morning_data]) if morning_data else ""
            )

            afternoon_time = (
                ", ".join([item["Time"] for item in afternoon_data])
                if afternoon_data
                else ""
            )
            afternoon_dist = (
                ", ".join([str(item["Distance"]) for item in afternoon_data])
                if afternoon_data
                else ""
            )
            afternoon_pace = (
                ", ".join([item["Pace"] for item in afternoon_data])
                if afternoon_data
                else ""
            )

            context[f"DATE_{day}"] = date_str
            context[f"TIME_{day}_MORN"] = morning_time
            context[f"DIST_{day}_MORN"] = morning_dist
            context[f"PACE_{day}_MORN"] = morning_pace
            context[f"TIME_{day}_AFTER"] = afternoon_time
            context[f"DIST_{day}_AFTER"] = afternoon_dist
            context[f"PACE_{day}_AFTER"] = afternoon_pace

            print(
                f"{day}: Date: {date_str}, Morning: {morning_time}, {morning_dist}, {morning_pace}, Afternoon: {afternoon_time}, {afternoon_dist}, {afternoon_pace}"
            )  # Debug statement

            total_distance += sum(
                item["Distance"] for item in morning_data + afternoon_data
            )

        context["WEEKLY_DISTANCE"] = str(round(total_distance, 2))
        # print(f"Weekly Total Distance: {total_distance}")  # Debug statement
        return context
    
class GUIApplication:
    def __init__(self):
        self.root = tk.Tk()
        self.name_entry = None
        self.start_day_entry = None
        self.__setup_gui()

    def __setup_gui(self):
        label1 = tk.Label(self.root, text="Name:")
        label1.pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()
        self.name_entry.insert(0, "Diogo")

        label2 = tk.Label(self.root, text="Start day:")
        label2.pack()
        self.start_day_entry = tk.Entry(self.root)
        self.start_day_entry.pack()
        self.start_day_entry.insert(0, self.__get_last_sunday())

        button2 = tk.Button(self.root, text="Open CSV File and Generate Report", command=self.run_analysis)
        button2.pack()

        self.root.mainloop()

    @staticmethod
    def __get_last_sunday() -> str:
       # Get the current date
        current_date = datetime.today()

        # Check if today is Sunday
        if current_date.weekday() == 6:  # Sunday is represented by 6
            return current_date.strftime("%Y/%m/%d")

        # Find the number of days to subtract to reach the last Sunday
        days_to_subtract = (7 + current_date.weekday()) % 6

        # Subtract the days to get the date of the last Sunday
        last_sunday_date = current_date - timedelta(days=days_to_subtract)

        return last_sunday_date.strftime("%Y/%m/%d")

    def run_analysis(self):
        name = self.name_entry.get()
        start_day = self.start_day_entry.get()
        file_path = filedialog.askopenfilename(initialdir="/", title="Select file", filetypes=[("CSV files", "*.csv"), ("all files", "*.*")])

        data_loader = DataLoader(file_path, start_day, NUMBER_OF_DAYS)
        df = data_loader.load_data()

        report_generator = ReportGenerator(df)
        report = report_generator.compile_report()

        template_renderer = TemplateRenderer('data/log_template.docx')
        output_path = f'./Registo_Treino {name}.docx'
        template_renderer.render_report(report, output_path)

        self.root.destroy()
        
if __name__ == "__main__":
    app = GUIApplication()