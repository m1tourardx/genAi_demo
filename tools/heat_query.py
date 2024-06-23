from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import List, Dict, Type, Optional
import pandas as pd
import os

dir_database = os.path.join(os.getcwd(), 'database')


class HeatInput(BaseModel):

    variables: List = Field(
        ..., description="""
    Here we need to select a variables to verify.
    To Water Inlet Temperature, the variable is “Water Inlet Temperature” in °C. 
    To Glycol Inlet Temperature, the variable is “Glycol Inlet Temperature” in °C. 
    To Out Glycol Temperature, the variable is “Out Glycol Temperature” in °C. 
    To Out Water Temperature, the variable is “Out Water Temperature” in °C. 
""")

class HeatQuery(BaseTool):
    name = 'heat_query'
    description = "Use this function to query the data from HX01."
    args_schema: Type[BaseModel] = HeatInput

    def _run(self,
             variables: List[str],
             path: str = os.path.join(dir_database, 'heat_exchanger.csv'),
             run_manager: Optional[CallbackManagerForToolRun] = None) -> str:

        df = pd.read_csv(path, index_col="Timestamp",
                         parse_dates=["Timestamp"])
        df_filtered = df[variables]
        summary = {}

        for variable in variables:
            max_value = df_filtered[variable].max()
            max_dates = df_filtered[df_filtered[variable] == max_value].index

            min_value = df_filtered[variable].min()
            min_dates = df_filtered[df_filtered[variable] == min_value].index

            mean_value = df_filtered[variable].mean()
            mean_dates = df_filtered[df_filtered[variable] == mean_value].index

            last_value = df_filtered[variable].iloc[-1]
            last_date = df_filtered.index[-1]

            summary[variable] = {
                "max_value": max_value,
                "max_dates": max_dates,
                "min_value": min_value,
                "min_dates": min_dates,
                "mean_value": mean_value,
                "mean_dates": mean_dates,
                "last_value": last_value,
                "last_date": last_date
            }

        summary_text = ""
        for variable, stats in summary.items():
            summary_text += (
                f"Variable: {variable}\n"
                f"Maximum Value: {stats['max_value']} (Dates: {', '.join(map(str, stats['max_dates']))})\n"
                f"Minimum Value: {stats['min_value']} (Dates: {', '.join(map(str, stats['min_dates']))})\n"
                f"Mean Value: {stats['mean_value']} (Dates: {', '.join(map(str, stats['mean_dates']))})\n"
                f"Last Value: {stats['last_value']} (Date: {stats['last_date']})\n\n"
            )

        return summary_text

    async def _arun(self,
                    variables: Dict[str, List[str]],
                    run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("QueryData does not support async.")
