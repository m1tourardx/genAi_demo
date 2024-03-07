# Como usar a classe `CustomAgent`

## Para usar o agent executor na função principal basta importá-la e chama-la na função.

Exemplo:

```python
from agent_handler import CustomAgent

def chat():
    agent_executor = CustomAgent().agent_exec()

```

A classe `CustomAgent` foi projetada para facilitar a obtenção de informações. Este tutorial mostrará como usar a função `info_getter` dessa classe para fazer perguntas e receber respostas.

## Passo 1: Importar a classe `CustomAgent`

Caso você queria importar a classe com a seguinte estrutura de diretório.

```python
pasta_do_projeto/
│
├── tools/
│   ├── __init__.py
│   └── some_tool.py
│
└── agent_handler.py

```

Você terá que importar os seguintes módulos para reconhecer o módulo dentro da tool específica

```python
import os
import sys
```

Tendo em vista a estrutura anterior, comece importando a classe `CustomAgent` dentro da função `def _run ():` existente na tool ou você pode criar uma nova função desde que faça o `import` dentro da função. Lembre-se de adicionar a linha anterior ao import conforme abaixo, para evitar problemas de importação. Fazendo isso você evita erros com `import` circular.

Exemplo 1:

```python
def _run(self,run_manager: Optional[CallbackManagerForToolRun]None) -> str:
    sys.path.append(os.getcwd())  # noqa
    from custom_agent import CustomAgent
    # Código restante
```

Exemplo 2:

```python
class limitEfficiency:
    def get_value(self):
        """Função para obter o valor do limite de eficiência do trocador de calor"""
        sys.path.append(os.getcwd())  # noqa
        from agent_handler import CustomAgent
        # Código restante

```

## Passo 2: Criar uma instância da classe `CustomAgent`

Depois de importar a classe `CustomAgent`, crie uma instância dela em seu código.

```python
def _run(self,run_manager: Optional[CallbackManagerForToolRun]None) -> str:
    sys.path.append(os.getcwd())  # noqa
    from agent_handler import CustomAgent
    # inicialização da classe
    custom_agent = CustomAgent()
    # Código restante
```

## Passo 3: Usar a função `info_getter` para obter informações

Agora você pode usar a função `info_getter` da classe `CustomAgent` para fazer perguntas e obter respostas usando o agente executor. Basta chamar a função e passar a pergunta como argumento da função `info_getter`. Caso você necessessite apenas um valor específico, é necessário alterar o argumento `instruction` para dizer ao agente executor que você precisa apenas do valor, ou você pode customizar a instrução conforme a necessidade, veja o exemplo a seguir:

```python
def _run(self,run_manager: Optional[CallbackManagerForToolRun]None) -> str:
    sys.path.append(os.getcwd())  # noqa
    from agent_handler import CustomAgent
    # inicialização da classe
    custom_agent = CustomAgent()
    query = "whats the limit efficiency of the thermal exchanger?"
    instructions = "Don't answer with a phrase, just the value"
    variable = custom_agent.info_getter(query=query,instruction=instructions)
    # Código restante
```

A função `info_getter` retorna a resposta para a pergunta fornecida como uma string. Você pode armazenar essa resposta em uma variável e usá-la conforme necessário em seu código.
