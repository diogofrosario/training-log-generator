import tkinter as tk
from tkinter import filedialog
from datetime import datetime, timedelta

from training_log_generator.dataloader import DataLoader
from training_log_generator.report import ReportGenerator
from training_log_generator.renderer import TemplateRenderer


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

        data_loader = DataLoader(file_path, start_day, 6)
        df = data_loader.load_data()

        report_generator = ReportGenerator(df)
        report = report_generator.compile_report()

        template_renderer = TemplateRenderer('data/log_template.docx')
        output_path = f'./Registo_Treino {name}.docx'
        template_renderer.render_report(report, output_path)

        self.root.destroy()
        print(f"Report generated at {output_path}")
 

if __name__ == "__main__":
    app = GUIApplication()
