from tools import ContactorQuery, HeatQuery, HXM
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
import os

##
class CustomAgent:
    def __init__(self):
        load_dotenv(override=True)
        self.OPENAI_KEY = "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"
        self.llm = ChatOpenAI(api_key=self.OPENAI_KEY)
        self.agent_executor = None

    def agent_exec(self):
        """Função responsável pela criação de uma instância para o agente executor.	
        Args: additional_instructions (Opcional): str   ->  String com instruções adicionais para o template do agente executor.
        Return: agent_executor: AgentExecutor   ->  Retorna uma instância do agente executor"""
        with open('./docs/refs.txt', 'r', encoding='utf-8') as file:
            content = file.read()
        prompt = ChatPromptTemplate.from_messages([
            ('system', f'''You serve as an assistant, you name is RAi, you are a Radix chatbot. Use this informations as context {content}.
                           If the user asks about external information, answer based on your knowledge.
                           If the user asks for information related to Reboiler variables, say "I am not allowed to check information about Reboiler variables."'''), MessagesPlaceholder(
                variable_name='char_history', optional=True),
            ('user', '{input}'), MessagesPlaceholder(variable_name="agent_scratchpad")])

        tools = [ContactorQuery(), HeatQuery(), HXM()]
        agent_executor = AgentExecutor(agent=create_openai_tools_agent(llm=self.llm, tools=tools, prompt=prompt),
                                       tools=tools, verbose=True)
        self.agent_executor = agent_executor
        return agent_executor

    def info_getter(self, query: str, instructions: str = ""):
        """Função para iniciar o agente executor em busca de informações específicas usando todas as tools disponíveis.
        Args: query: str   ->  String com a pergunta a ser feita ao agente executor.
        Return: answer: str   ->  String com a resposta da pergunta feita ao agente executor."""

        if not self.agent_executor:
            self.agent_exec()

        query = instructions + "." + query
        answer = self.agent_executor.invoke(
            {"input": query})
        answer = answer['output']

        return answer
