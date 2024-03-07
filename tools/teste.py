import os
import sys
sys.path.append(os.getcwd())  # nopep8
import agent_handler

agent = agent_handler.CustomAgent()

answer = agent.info_getter(
    query="When the heat exchanger will require maintanance?")

print(answer)
