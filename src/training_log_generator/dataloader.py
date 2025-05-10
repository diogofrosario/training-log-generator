import pandas as pd
from datetime import timedelta
from typing import Optional


class DataLoader:
    def __init__(self, file_path: str, start_day: str, number_of_days: int):
        self.file_path = file_path
        self.start_day = start_day
        self.number_of_days = number_of_days
        self.data: Optional[pd.DataFrame] = None

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
        df.rename(columns={"Data": "Date", "Distância": "Distance", "Tempo": "Time", "Ritmo médio": "Avg Pace", "Velocidade média": "Avg Pace",}, inplace=True)
        return df

    def __create_date_and_time_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        df[['Date', 'Time_of_Day']] = df['Date'].str.split(' ', expand=True)
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        df['Time_of_Day'] = pd.to_datetime(df['Time_of_Day']).dt.time
        return df

    def __filter_by_date(self, df: pd.DataFrame) -> pd.DataFrame:
        start_datetime = pd.to_datetime(self.start_day)
        date_filter = start_datetime - timedelta(days=self.number_of_days)
        return df[(df["Date"] >= date_filter.date()) & (df["Date"] <= start_datetime.date())]

    @staticmethod
    def __morning_or_afternoon(time: pd.Timestamp) -> str:
        return "morning" if time.hour < 12 else "afternoon"
