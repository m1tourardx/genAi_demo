from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
import os
import sys
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import List, Dict, Type, Optional
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from typing import Union, Tuple
sys.path.append(os.getcwd())  # noqa

dir_database = os.path.join(os.getcwd(), 'database')


class limitEfficiency:
    def get_value(self):
        """Função para obter o valor do limite de eficiência do trocador de calor"""
        sys.path.append(os.getcwd())  # noqa
        from agent_handler import CustomAgent
        limit_info = CustomAgent().info_getter(query="whats the limit efficiency of the thermal exchanger?",
                                               instructions="Dont answer with a phrase, just the value")
        limit = limit_info.replace(
            "%", "") if "%" in limit_info else limit_info
        limit = float(limit)
        return limit

# class HXMInput(BaseModel):
#     # limit: float = Field(
#     #     default=90, description=f"This is the limit value for the thermal efficiency of the verified heat exchanger. If the user does not inform, the adopted value must be 90.")
#     path: str = Field(default='/Users/mitoura/Desktop/LYB/program/data/',
#                       description="Indicates the path to the data, always equal to '/Users/mitoura/Desktop/LYB/program/data/'.")
#     # limit: float = Field(default=limitEfficiency().get_limit())


class HXM(BaseTool):
    name = 'hxm_predict'
    description = "Use this function to predict the useful life of heat exchangers. This function indicates when the HX01 heat exchanger will require maintenance."
    # args_schema: Type[BaseModel] = HXMInput

    def _to_args_and_kwargs(self, tool_input: Union[str, Dict]) -> Tuple[Tuple, Dict]:
        return (), {}

    def _run(self,
             # limit: float,
             # run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
             ):

        # Aquisição do valor do limite de eficiência
        limit = limitEfficiency().get_value()

        # Leitura do banco de dados
        df = pd.read_csv(os.path.join(dir_database, 'heat_exchanger.csv'))
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df.set_index('Timestamp', inplace=True)
        df.sort_index(inplace=True)

        var = df['Heat Efficiency']

        cont = []
        n = 1
        for i in df.index:
            cont.append(n)
            n += 1

        DATA = pd.DataFrame({"HXE": var.values, "Cont": cont}, index=var.index)

        # We will do the regression based on the RMAA and the created column (cont)
        # since it is not possible to do a direct regression of the RMAA based on the
        # Timestemp using the package we know and how we know it

        y = DATA[["HXE"]]
        x = DATA[["Cont"]]

        # Defining the model
        model = LinearRegression()
        model.fit(x, y)

        # Calculating the initial values
        y = model.intercept_ + DATA['Cont'][0]*model.coef_
        init = df.index[0]

        # We will loop to extrapolate the entered range and identify
        # the time when the RMAA is less than or equal to the limit

        y_calc = []
        date = []
        cont = 1
        while y >= 92:
            cont += 1
            y = model.intercept_ + cont*model.coef_
            y_calc.append(float(y))
            day = init + timedelta(days=cont)
            date.append(day)

        response = f'The exchanger needs to be repaired at: {day}.\n* Maintenance team must be notified by {day - 30*timedelta(days=1)} (30 days before).\n* It must be checked which backup equipment should be used during the maintenance period.\n* The glycol stream must be directed to the backup exchanger so that the glycol flow rate is not drastically reduced.\n* A glycol flow can reach a minimum value of {limit} of the design flow.'

        return response

    async def _arun(self,
                    # limit: float,
                    # run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
                    ):
        raise NotImplementedError("QueryData does not support async.")
