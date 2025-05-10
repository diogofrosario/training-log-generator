import streamlit as st

from dataloader import DataLoader
from report import ReportGenerator
from renderer import TemplateRenderer

def run_app():
    st.title("Training Log Generator")

    start_day = st.date_input("Select Start Date")
    output_path = "./Registo_Treino Diogo.docx"

    if file_path := st.file_uploader("Upload CSV File", type="csv"):
        if st.button("Generate Report") and file_path is not None:
            data_loader = DataLoader(file_path, start_day.isoformat(), 6)
            data = data_loader.load_data()

            report_generator = ReportGenerator(data)
            report = report_generator.compile_report()

            renderer = TemplateRenderer('data/log_template.docx')

            renderer.render_report(report, output_path)

            st.write(f"Report saved to {output_path}")

            # add a button to download the report
            st.download_button(label="Download Report", data=output_path, file_name="Registo_Treino Diogo.docx")
            # st.download_button(label="Download Report", data=, file_name="Registo_Treino Diogo.docx", mime=)

if __name__ == "__main__":
    run_app()
