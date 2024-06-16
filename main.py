import tkinter as tk
from tkinter import filedialog
import argparse
from datetime import datetime, timedelta
from typing import Dict

import pandas as pd

from docxtpl import DocxTemplate
import jinja2

from utils import prepare_data, fill_template, prepare_context

import warnings

warnings.filterwarnings("ignore")


def open_file():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("CSV files", "*.csv"), ("all files", "*.*")))
    return filename


def compile_report(df: pd.DataFrame) -> Dict[str, Dict[str, list]]:
    # Initialize an empty dictionary to store the runs information for each day and period (morning/afternoon)
    report = {}

    # Group the DataFrame by Date and am_pm (morning/afternoon)
    grouped = df.groupby(["Date", "am_pm"])

    # Iterate over each group and extract relevant information
    for (date, am_pm), group_df in grouped:
        if date not in report:
            report[date] = {"morning": [], "afternoon": []}

        # Extracting information for each run
        for _, row in group_df.iterrows():
            run_info = {
                "Time": row["Time"],
                "Distance": row["Distance"],
                "Pace": row["Avg Pace"]
            }
            report[date][am_pm].append(run_info)

    return report


def _generate_weekly_report(df: pd.DataFrame) -> Dict[str, Dict[str, list]]:
    # Compile the report
    report = compile_report(df)
    print(report)

    # Initialize variables to calculate total distance
    total_distance = 0

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Print the report
    for date, runs in report.items():
        print(f"Date: {date}")
        for period, run_info in runs.items():
            if run_info:  # Check if there are any runs in this period
                print(f"{period.capitalize()} runs:")
                for run in run_info:
                    print(f"   Time: {run['Time']}, Distance: {run['Distance']}, Pace: {run['Pace']}")
                    total_distance += run['Distance']
            else:
                print(f"No {period} runs.")
        print()

    # Print total distance for the week
    print(f"Total distance for the week: {total_distance} kms.")
    return report


def last_sunday() -> str:
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


def run_analysis() -> None:
    # Get the values from the entry widgets
    number_of_days = int(entry1.get())
    start_day = entry2.get()
    file_path = open_file()

    print(file_path)

    # Call the prepare_data function with the retrieved values
    df = prepare_data(file_path, number_of_days, start_day)

    # Generate and display the report
    
    report = _generate_weekly_report(df)
    
    # Paths to the template and the output file
    template_path = './log_template.docx'
    output_path = './filled_log.docx'

    # Fill the template
    # fill_template(report, template_path, output_path)
    
    doc = DocxTemplate(template_path)
    context = prepare_context(report)
    doc.render(context)
    doc.save(output_path)

    root.destroy()  # Close the GUI window after generating the report
    return


if __name__ == "__main__":
    root = tk.Tk()

    label1 = tk.Label(root, text="Number of days:")
    label1.pack()
    entry1 = tk.Entry(root)
    entry1.pack()
    entry1.insert(0, "6")

    label2 = tk.Label(root, text="Start day:")
    label2.pack()
    entry2 = tk.Entry(root)
    entry2.pack()
    entry2.insert(0, last_sunday())

    button2 = tk.Button(root, text="Open CSV File and Generate Report", command=run_analysis)
    button2.pack()

    root.mainloop()
