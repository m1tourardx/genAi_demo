from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import List, Dict, Type, Optional
import pandas as pd
import os

dir_database = os.path.join(os.getcwd(), 'database')


class HeatInput(BaseModel):
    info = """
            variables:{
            "Water Inlet Temperature":{
                "description": "Temperature of water inlet in heat exchanger.",
                "unit":"°C"
            },
            "Glycol Inlet Temperature":{
                "description": "Temperature of glycol inlet in heat exchanger.",
                "unit":"°C"
            },
            "Out Glycol Temperature":{
                "description": "Temperature of glycol outlet in heat exchanger.",
                "unit":"°C"
            },
            "Out Water Temperature":{
                "description": "Temperature of water outlet in heat exchanger.",
                "unit":"°C"
            }
           """
    variables: List = Field(
        ..., description=f"Here we need to insert a variables to verify.  Check {info} for more information and the name of variables presented in {info}.")
    path: str = Field(default='/Users/mitoura/Desktop/LYB/program/data/',
                      description="Indicates the path to the data, always equal to '/Users/mitoura/Desktop/LYB/program/data/'.")


class HeatQuery(BaseTool):
    name = 'heat_query'
    description = "Use this function to query the data from HX01."
    args_schema: Type[BaseModel] = HeatInput

    def _run(self,
             variables: List[str],
             path: str = os.path.join(dir_database, 'heat_exchanger.csv'),
             run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """
        data_sources: A list of file names or paths to datasets.
        path: Data path, always equal to 'data/'.
        variables: A dictionary where keys are the names of paths and values are lists of variables.
        """

        df = pd.read_csv(path, index_col="Timestamp",
                         parse_dates=["Timestamp"])
        print(variables)
        df_filtered = df[variables]

        return df_filtered.to_string(index=False)

    async def _arun(self,
                    variables: Dict[str, List[str]],
                    path: str = '/Users/mitoura/Desktop/LYB/program/data/',
                    run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("QueryData does not support async.")
