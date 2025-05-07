from config.settings import Config
from geneval.generate.test_plan_generator import TestPlanGenerator
from geneval.generate.prompts import Prompts


test_plan_generator = TestPlanGenerator(
    Prompts.SYSTEM_PROMPT,
    Prompts.SYSTEM_CONTEXT,
    None, 
    Config.MODEL, 
    Config.TEMPERATURE
)

answer = test_plan_generator.generate()

print(answer)

