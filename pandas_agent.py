import os
import pandas as pd
from dotenv import load_dotenv
from langchain_openai.chat_models import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.callbacks.manager import CallbackManagerForToolRun, AsyncCallbackManagerForToolRun
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from typing import List, Type, Optional, Dict

load_dotenv()

class CustomAgent:
    def __init__(self, model):
        load_dotenv(override=True)
        self.llm = AzureChatOpenAI(
            openai_api_version="2023-07-01-preview",
            azure_endpoint=os.getenv("END_POINT"),
            openai_api_key=os.getenv("API_KEY"),
            azure_deployment=model
        )   

    def agent_exec(self, query):
        prompt = ChatPromptTemplate.from_messages([
            ('system', "You are a chatbot to support decision-making about biomass gasification processes in supercritical water."),
            MessagesPlaceholder(variable_name='char_history', optional=True),
            ('user', '{input}'),
            MessagesPlaceholder(variable_name="agent_scratchpad")
        ])

        tools = [ProcessQuery()]
        agent_executor = AgentExecutor(agent=create_openai_tools_agent(llm=self.llm, tools=tools, prompt=prompt),
                                    tools=tools, verbose=True)
        return agent_executor.invoke({'input': query})['output']

class ProcessInput(BaseModel):
    variables: List = Field(
        ..., description="""
    Here we need to select a variables to verify.
    To Methane formation, the variable is “Methane” in mols.
    To Water formation, the variable is Water in mols.
    To CarbonMonoxide formation, the variable is CarbonMonoxide in mols.
    To CarbonDioxide formation, the variable is CarbonDioxide in mols.
    To Hydrogen formation, the variable is Hydrogen in mols.
    To Carbon formation, the variable is Carbon in mols.
    To Methanol formation, the variable is Methanol in mols.
""")

class ProcessQuery(BaseTool):
    name = 'process_query'
    description = "Use this function to query the data RC01."
    args_schema: Type[BaseModel] = ProcessInput

    def _run(self,
             variables: List[str],
             run_manager: Optional[CallbackManagerForToolRun] = None) -> str:

        df = pd.read_csv('data.csv')
        
        if df.empty:
            return "No data available for the given date range."
        df_filtered = df[variables + ['Temperature (K)', 'Pressure (bar)']]
        summary = {}

        for variable in variables:
            max_value = df_filtered[variable].max()
            max_row = df_filtered[df_filtered[variable] == max_value].iloc[0]
            max_T = max_row['Temperature (K)']
            max_P = max_row['Pressure (bar)']

            min_value = df_filtered[variable].min()
            min_row = df_filtered[df_filtered[variable] == min_value].iloc[0]
            min_T = min_row['Temperature (K)']
            min_P = min_row['Pressure (bar)']

            summary[variable] = {
                "max_value": max_value,
                "max_T": max_T,
                "max_P": max_P,
                "min_value": min_value,
                "min_T": min_T,
                "min_P": min_P
            }

        summary_text = ""
        for variable, stats in summary.items():
            summary_text += (
                f"Maximum formation of {variable}:\n"
                f"Mols: {stats['max_value']} mols\n"
                f"Temperature: {stats['max_T']} K\n"
                f"Pressure: {stats['max_P']} bar\n\n"
                f"Minimum formation of {variable}:\n"
                f"Mols: {stats['min_value']} mols\n"
                f"Temperature: {stats['min_T']} K\n"
                f"Pressure: {stats['min_P']} bar\n\n"
            )

        return summary_text

    async def _arun(self,
                    variables: Dict[str, List[str]],
                    run_manager: Optional[AsyncCallbackManagerForToolRun] = None) -> str:
        raise NotImplementedError("QueryData does not support async.")