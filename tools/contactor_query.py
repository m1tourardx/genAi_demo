from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import List, Dict, Type, Optional
import pandas as pd
import os
from .date_time import convert_to_datetime
from datetime import datetime, timedelta

dir_database = os.path.join(os.getcwd(), 'database')


class ContactorInput(BaseModel):
    ts_start: str = Field(..., description="Identify the start time for data acquisition. Return informations in this format: %Y-%m-%dT%H:%M:%S.")
    ts_end: str = Field(..., description="Identify the end time for data acquisition. Return informations in this format: %Y-%m-%dT%H:%M:%S.")
    variables: List = Field(..., description="""
    Here we need to select a variables to verify.
    To Natural Gas Dew Point, the variable is “Dew Point” in °C. 
    To Contactor tower pressure, the variable is “Contactor Pressure” in bar. 
    To Contactor Tower temperature, the variable is “Contactor Temperature” in °C. 
    To Glycol moisture in contactor tower input, the variable is “Glycol Moisture” in % v/v.
    To Natural Gas mosture in contactor tower output, the variable is "Natural Gas Moisture" in lbm/MMscf.
    To Glycol Level, the variable is "Glycol Level" in %.
    """)


class ContactorQuery(BaseTool):
    name = 'contactor_query'
    description = "Use this function to query the data from contactor tower."
    args_schema: Type[BaseModel] = ContactorInput

    def _run(self,
             ts_start: str,
             variables: List[str],
             ts_end: str = 'now',
             path: str = os.path.join(dir_database, 'contactor_tower.csv'),
             run_manager: Optional[CallbackManagerForToolRun] = None) -> str:

        ts_start = convert_to_datetime(ts_start)
        ts_end = convert_to_datetime(ts_end)

        if ts_start == ts_end:
            ts_start = ts_end - timedelta(days=3)


        dir_database = os.path.join(os.getcwd(), 'database')
        def update_timestamps_in_datasets(directory):
            files = [f for f in os.listdir(directory) if f.endswith('.csv')]
            reference_date = datetime.today().date()
            
            updated_datasets = {}

            for file in files:
                df = pd.read_csv(os.path.join(directory, file), parse_dates=["Timestamp"])
                
                last_timestamp = pd.to_datetime(df['Timestamp'].iloc[-1]).date()
                days_diff = (reference_date - last_timestamp).days

                df['Timestamp'] = pd.to_datetime(df['Timestamp']) + timedelta(days=days_diff)
                df.set_index('Timestamp', inplace=True)
                
                updated_datasets[file] = df
                
            return updated_datasets

        updated_datasets = update_timestamps_in_datasets(dir_database)
        doc01 = updated_datasets.get('contactor_tower.csv')

        df = doc01
        df = df[(df.index >= ts_start) & (df.index <= ts_end)]
        
        if df.empty:
            return "No data available for the given date range."
        
        df_filtered = df[variables]
        summary = {}

        for variable in variables:
            max_value = df_filtered[variable].max()
            max_dates = df_filtered[df_filtered[variable] == max_value].index

            min_value = df_filtered[variable].min()
            min_dates = df_filtered[df_filtered[variable] == min_value].index

            mean_value = df_filtered[variable].mean()

            last_value = df_filtered[variable].iloc[-1]
            last_date = df_filtered.index[-1]

            summary[variable] = {
                "max_value": max_value,
                "max_dates": max_dates,
                "min_value": min_value,
                "min_dates": min_dates,
                "mean_value": mean_value,
                "last_value": last_value,
                "last_date": last_date
            }

        summary_text = ""
        for variable, stats in summary.items():
            summary_text += (
                f"Variable: {variable}\n"
                f"Maximum Value: {stats['max_value']} (Dates: {', '.join(map(str, stats['max_dates']))})\n"
                f"Minimum Value: {stats['min_value']} (Dates: {', '.join(map(str, stats['min_dates']))})\n"
                f"Mean Value: {stats['mean_value']})\n"
                f"Last Value: {stats['last_value']} (Date: {stats['last_date']})\n\n"
            )

        return summary_text

    async def _arun(self,
                    variables: Dict[str, List[str]],
                    path: str = '/Users/mitoura/Desktop/LYB/program/data/',
                    run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("QueryData does not support async.")
