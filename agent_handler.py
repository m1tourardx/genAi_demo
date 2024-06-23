from tools import ContactorQuery, HeatQuery, HXM
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai.chat_models import AzureChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent
import os

##
class CustomAgent:
    def __init__(self):
        load_dotenv(override=True)
        self.llm = AzureChatOpenAI(openai_api_version="2023-07-01-preview",
                           azure_endpoint=os.getenv("OPENAI_URL"),
                           openai_api_key=os.getenv("OPEN_AI_KEY"),
                           azure_deployment=os.getenv("OPENAI_DEPLOY"),
                           temperature=0)

    def agent_exec(self):
        """Função responsável pela criação de uma instância para o agente executor.	
        Args: additional_instructions (Opcional): str   ->  String com instruções adicionais para o template do agente executor.
        Return: agent_executor: AgentExecutor   ->  Retorna uma instância do agente executor"""
        with open('./docs/refs.txt', 'r', encoding='utf-8') as file:
            content = file.read()
        prompt = ChatPromptTemplate.from_messages([
            ('system', f'''You serve as an assistant, you name is RAi, you are a Radix chatbot. Use this informations as context {content} and this: "Based on prediction models, the next glycol replacement should occur on December 11th".
                           Consult the tools only to answer questions about variables.
                           If the user asks about external information, answer based on your knowledge.
                           If the user asks for information related to Reboiler variables, say "I am not allowed to check information about Reboiler variables."'''), MessagesPlaceholder(
                variable_name='char_history', optional=True),
            ('user', '{input}'), MessagesPlaceholder(variable_name="agent_scratchpad")])

        tools = [ContactorQuery(), HeatQuery(), HXM()]
        agent_executor = AgentExecutor(agent=create_openai_tools_agent(llm=self.llm, tools=tools, prompt=prompt),
                                       tools=tools, verbose=True)
        self.agent_executor = agent_executor
        return agent_executor