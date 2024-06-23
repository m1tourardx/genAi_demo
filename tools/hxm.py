from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
import os
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import List, Type, Optional
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta

dir_database = os.path.join(os.getcwd(), 'database')

class HXMInput(BaseModel):
    limit: float = Field(default=91, description="Limit value for heat efficiency of HX01. If the user does not specify a value for limit, adopt limit = 91.")

class HXM(BaseTool):
    name = 'hxm_predict'
    description = "Use this function to predict the useful life of heat exchangers. This function indicates when the HX01 heat exchanger will require maintenance."
    args_schema: Type[BaseModel] = HXMInput

    def _run(self,
             limit: Optional[float] = None,
             run_manager: Optional[CallbackManagerForToolRun] = None) -> str:

        if limit is None:
            limit = 91
            
        df = pd.read_csv(os.path.join(dir_database, 'heat_exchanger.csv'))
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)
        df.sort_index(inplace=True)

        var = df['Heat Efficiency']

        cont = list(range(1, len(df) + 1))

        DATA = pd.DataFrame({"HXE": var.values, "Cont": cont}, index=var.index)

        y = DATA[["HXE"]]
        x = DATA[["Cont"]]

        model = LinearRegression()
        model.fit(x, y)

        y = model.intercept_ + DATA['Cont'][0] * model.coef_
        init = df.index[0]

        cont = 1
        while y >= limit:
            cont += 1
            y = model.intercept_ + cont * model.coef_

        repair_date = init + timedelta(days=cont)
        notify_date = repair_date - timedelta(days=30)

        response = (
            f'The exchanger needs to be repaired at: {repair_date.date()}.\n'
            f'* Maintenance team must be notified by {notify_date.date()} (30 days before).\n'
            f'* It must be checked which backup equipment should be used during the maintenance period.\n'
            f'* The glycol stream must be directed to the backup exchanger so that the glycol flow rate is not drastically reduced.\n'
            f'* A glycol flow can reach a minimum value of 93 % of the design flow.'
        )

        return response

    async def _arun(self):
        raise NotImplementedError("QueryData does not support async.")
