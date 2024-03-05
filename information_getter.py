from tools import DocumentQuery


class infomationGetter:
    def __init__(self):
        self.tool = DocumentQuery()

    def get_info(self, query, instructions):
        """Função para buscar informações especificas em documentos de texto
        Args: additional_instructions (Opcional): str   ->  String com instruções adicionais para o template do agente executor.
        Return: agent_executor: AgentExecutor   ->  Retorna uma instância do agente executor."""
        query = instructions+"."+query
        answer = self.tool.run(query)
        return answer
