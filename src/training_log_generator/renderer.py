from typing import Dict
from docxtpl import DocxTemplate # type: ignore[import]
from datetime import timedelta

class TemplateRenderer:
    def __init__(self, template_path: str):
        self.template_path = template_path

    def render_report(self, report: Dict[str, Dict[str, list]], output_path: str) -> DocxTemplate:
        doc = DocxTemplate(self.template_path)
        context = self.__prepare_context(report)
        doc.render(context)
        doc.save(output_path)
        # return doc

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
        try:
            start_date = list(data.keys())[0]
        except Exception:
            raise Exception("No data found for the selected date range")
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
                float(item["Distance"]) for item in morning_data + afternoon_data
            )

        context["WEEKLY_DISTANCE"] = str(round(total_distance, 2))
        # print(f"Weekly Total Distance: {total_distance}")  # Debug statement
        return context
