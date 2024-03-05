from tools import ContactorQuery, HeatQuery, DocumentQuery, HXM
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import AgentExecutor, create_openai_tools_agent
import os


class CustomAgent:
    def __init__(self):
        load_dotenv(override=True)
        self.OPENAI_KEY = os.getenv("OPEN_AI_KEY")
        self.llm = ChatOpenAI(api_key=self.OPENAI_KEY)

    def agent_exec(self):
        """Função responsável pela criação de uma instância para o agente executor.	
        Args: additional_instructions (Opcional): str   ->  String com instruções adicionais para o template do agente executor.
        Return: agent_executor: AgentExecutor   ->  Retorna uma instância do agente executor"""

        prompt = prompt = ChatPromptTemplate.from_messages([
            ('system', f'''You serve as an assistant. You shoud always call available tools before any other action. Call DocumentQuery() first using whole prompt as input for this function.'''), MessagesPlaceholder(
                variable_name='char_history', optional=True),
            ('user', '{input}'), MessagesPlaceholder(variable_name="agent_scratchpad")])

        tools = [ContactorQuery(), HeatQuery(), DocumentQuery(), HXM()]
        agent_executor = AgentExecutor(agent=create_openai_tools_agent(llm=self.llm, tools=tools, prompt=prompt),
                                       tools=tools, verbose=True)
        return agent_executor

    def info_getter(self, query: str, instructions: str = ""):
        """Função para iniciar o agente executor em busca de informações específicas usando todas as tools disponíveis.
        Args: query: str   ->  String com a pergunta a ser feita ao agente executor.
        Return: answer: str   ->  String com a resposta da pergunta feita ao agente executor."""

        agente_executor = self.agent_exec()
        query = instructions+"."+query
        answer = agente_executor.invoke(
            {"input": query})

        return answer['output']
