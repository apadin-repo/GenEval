from config.settings import Config
from geneval.generate.test_plan_generator import TestPlanGenerator
from geneval.generate.prompts import Prompts
from markdown_pdf import MarkdownPdf, Section

test_plan_generator = TestPlanGenerator(
    Prompts.SYSTEM_PROMPT,
    Prompts.SYSTEM_CONTEXT,
    None, 
    Config.MODEL, 
    Config.TEMPERATURE
)

test_plan = test_plan_generator.generate(Prompts.CATEGORIES[0])
print(test_plan)
# pdf = MarkdownPdf()
# pdf.meta["title"] = 'Test Plan'
# pdf.add_section(Section(test_plan, toc=False))
# pdf.save('Test Plan.pdf')

