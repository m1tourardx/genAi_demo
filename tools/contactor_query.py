from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import List, Dict, Type, Optional
import pandas as pd
import os

dir_database = os.path.join(os.getcwd(), 'database')


class ContactorInput(BaseModel):
    info = """
            variables:{
            "Dew Point":{
                "description": "Natural Gas DewPoint.",
                "unit":"°C"
            },
            "Contactor Pressure":{
                "description": "Contactor tower pressure.",
                "unit":"bar"
            },
            "Natural Gas Moisture":{
                "description": "Natural Gas Moisture or water content in natural gas.",
                "unit":"lbm/MMscf"
            },
            "Contactor Temperature":{
                "description": "Contactor Tower temperature.",
                "unit":"°C"
            },
            "Glycol Moisture":{
                "description": "Glycol moisture in contactor tower input.",
                "unit":" % v/v"
            }
            }
           """
    variables: List = Field(..., description=f"Here we need to insert a variables to verify.  To Natural Gas Dew Point, the variable is “Dew Point” in °C. To Contactor tower pressure, the variable is “Contactor Pressure” in bar. To Contactor Tower temperature, the variable is “Contactor Temperature” in °C. To Glycol moisture in contactor tower input, the variable is “Glycol Moisture” in % v/v.")


class ContactorQuery(BaseTool):
    name = 'contactor_query'
    description = "Use this function to query the data from contactor tower."
    args_schema: Type[BaseModel] = ContactorInput

    def _run(self,
             variables: List[str],
             path: str = os.path.join(dir_database, 'contactor_tower.csv'),
             run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """
        data_sources: A list of file names or paths to datasets.
        path: Data path, always equal to 'database/'.
        variables: A dictionary where keys are the names of paths and values are lists of variables.
        """
        print(variables)
        df = pd.read_csv(path, index_col="Timestamp",
                         parse_dates=["Timestamp"])
        df_filtered = df[variables]

        return df_filtered.to_string(index=False)

    async def _arun(self,
                    variables: Dict[str, List[str]],
                    path: str = '/Users/mitoura/Desktop/LYB/program/data/',
                    run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("QueryData does not support async.")
