# Como usar a classe `CustomAgent`

## Para usar o agent executor na função principal basta importá-la e chama-la na função.

Essa será estrutura de diretório usada como exemplo.

```python
pasta_do_projeto/
│
├── tools/
│   ├── __init__.py
│   └── some_tool.py
│
└── agent_handler.py

```

Tendo em vista a estrutura anterior. Podemos importar diretamente neste caso.

Exemplo:

```python
from agent_handler import CustomAgent

def chat():
    agent_executor = CustomAgent().agent_exec()

```

A classe `CustomAgent` foi projetada para facilitar a obtenção de informações. Este tutorial mostrará como usar a função `info_getter` dessa classe para fazer perguntas e receber respostas.

## Passo 1: Importar a classe `CustomAgent`

Tendo em vista a estrutura anterior, comece importando os modulos `os ` e `sys`, em seguida a classe `CustomAgent` dentro da função `def _run ():` existente na tool ou você pode criar uma nova função desde que faça o `import` dentro da função. Fazendo isso você evita erros com `import` circular.

Obs.: No comando `sys.path.append(path)` deve ser passado o path do módulo `agente_handler.py` como argumento de acordo com a estrutura do seu diretório, para que ocorra o import necessário. Esse comando deve ser adicionado antes de fazer a importação. Veja o exemplo a seguir.

Exemplo 1:

```python

import os
import sys

def _run(self,run_manager: Optional[CallbackManagerForToolRun]None) -> str:
    sys.path.append(os.getcwd())  # nopep8
    from custom_agent import CustomAgent
    # Código restante
```

Exemplo 2:

```python
class limitEfficiency:
    def get_value(self):
        """Função para obter o valor do limite de eficiência do trocador de calor"""
        sys.path.append(os.getcwd())  # nopep8
        from agent_handler import CustomAgent
        # Código restante

```

## Passo 2: Usar a função `info_getter` para obter informações

Agora você pode usar a função `info_getter` da classe `CustomAgent` para fazer perguntas e obter respostas usando o agente executor. Basta chamar a função e passar a pergunta como argumento da função `info_getter`. Caso você necessessite apenas um valor específico, é necessário alterar o argumento `instruction` para dizer ao agente executor que você precisa apenas do valor, ou você pode customizar a instrução conforme a necessidade, veja o exemplo a seguir:

```python
def _run(self,run_manager: Optional[CallbackManagerForToolRun]None) -> str:
    sys.path.append(os.getcwd())  # nopep8
    from agent_handler import CustomAgent

    # Consulta e instruções
    query = "whats the limit efficiency of the thermal exchanger?"
    instructions = "Don't answer with a phrase, just the value"
    variable = custom_agent.info_getter(query=query,instruction=instructions)
    # Código restante
```

A função `info_getter` retorna a resposta para a pergunta fornecida como uma string. Você pode armazenar essa resposta em uma variável e usá-la conforme necessário em seu código.
