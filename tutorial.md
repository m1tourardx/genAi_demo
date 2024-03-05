# Tutorial: Como usar a `info_getter` da classe `CustomAgent`

A classe `CustomAgent` foi projetada para facilitar a obtenção de informações específicas usando uma variedade de ferramentas disponíveis. Este tutorial mostrará como usar a função `info_getter` dessa classe para fazer perguntas e receber respostas usando o agente executor.

## Passo 1: Importar a classe `CustomAgent`

Caso você queria importar a classe com a seguinte estrutura de diretório.

```python
pasta_do_projeto/
│
├── tools/
│   ├── __init__.py
│   └── some_tool.py
│
└── custom_agent.py

```

Você terá que importar os seguintes módulos para reconhecer o módulo dentro da tool específica

```python
import os
import sys
sys.path.append(os.getcwd())  # noqa
```

Tendo em vista a estrutura anterior, comece importando a classe `CustomAgent` dentro da função `def _run ():` existente na tool. Fazendo isso você evita erros com import circular.

```python
def _run(self,run_manager: Optional[CallbackManagerForToolRun]None) -> str:
    from custom_agent import CustomAgent
    # Código restante
```

## Passo 2: Criar uma instância da classe `CustomAgent`

Depois de importar a classe `CustomAgent`, crie uma instância dela em seu código. Certifique-se de passar a chave de API do OpenAI durante a inicialização da classe.

```python
def _run(self,run_manager: Optional[CallbackManagerForToolRun]None) -> str:
    from custom_agent import CustomAgent
    # inicialização do agente executor
    custom_agent = CustomAgent()
    # Código restante
```

## Passo 3: Usar a função `info_getter` para obter informações

Agora você pode usar a função `info_getter` da classe `CustomAgent` para fazer perguntas e obter respostas usando o agente executor. Basta chamar a função e passar a pergunta como argumento da função `info_getter`. Caso você necessessite apenas um valor específico, é necessário alterar o argumento `instruction` para dizer ao agente executor que você precisa apenas do valor, conforme no exemplo abaixo:

```python
def _run(self,run_manager: Optional[CallbackManagerForToolRun]None) -> str:
    from custom_agent import CustomAgent
    # inicialização do agente executor
    custom_agent = CustomAgent()
    query = "whats the limit efficiency of the thermal exchanger?"
    instructions = "Dont answer with a phrase, just the value"
    variable = custom_agent.info_getter(query=query,instruction=instructions)
    # Código restante
```

A função `info_getter` retorna a resposta para a pergunta fornecida como uma string. Você pode armazenar essa resposta em uma variável e usá-la conforme necessário em seu código.
