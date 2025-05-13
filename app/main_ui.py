import gradio as gr
from ui.style import Style
import os
from geneval.generate.test_plan import TestPlan
import pandas as pd

# # TODO:
# - fix category_titles (remove?)
# - capture changes in the test plan 
# - When something hangesin the df that is not the 'Actual Output' column, revert to original value?
# - Add short description to Description? 

MAX_CATEGORIES = 10

def handle_generate(description, files):
  yield gr.update(interactive=False), gr.update(value="Generating test plan... This may take a few moments."), *[gr.update(visible=False) for _ in range(MAX_CATEGORIES * 2)], gr.update(visible=False)

  file_contents = []
  if files:
    for file in files:
      file_path = file.name
      filename = os.path.basename(file_path)
      if filename.endswith(".md"):
        try:
          with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            file_contents.append(f"**{filename}**\n```\n{content[:1000]}\n```\n")
        except Exception as e:
          file_contents.append(f"--Failed to read {filename}: {e}--")

  context = "--- Application Description ---\n" + description + "\n\n--- Application README ---\n" + "\n".join(file_contents)
  result = TestPlan.generate(context)

  title_updates, table_updates = to_gDataframe(result, max_components=MAX_CATEGORIES)

  yield gr.update(interactive=True), gr.update(value="Generate Test Plan"), *title_updates, *table_updates, gr.update(visible=True)

def to_gDataframe(dfs: list[pd.DataFrame], max_components=5) -> tuple:
  title_updates = []
  dataframe_updates = []

  for i in range(max_components):
    if i < len(dfs):
      df = dfs[i]
      category = df["Category"].iloc[0] if "Category" in df.columns else f"Test Plan {i+1}"
      title_updates.append(gr.update(value=f"## {category}", visible=True))
      dataframe_updates.append(gr.update(value=df, visible=True))
    else:
      title_updates.append(gr.update(visible=False))
      dataframe_updates.append(gr.update(visible=False))

  return title_updates, dataframe_updates

# ----- UI -----
with gr.Blocks(title="GenAI Evaluation Tool", css=Style.CSS) as demo:
  # ---------------------- Application Description ----------------------
  with gr.Row():
    gr.Markdown("# GenAI Evaluation Tool")
  with gr.Row(elem_id="output-container"):
    with gr.Column(scale=1):
      gr.Markdown("## App Description (optional)")
      gr.Markdown("Describe your LLM-based application here to help the tool generate a customized test plan focused on security, bias, fairness, toxicity, and more. You can either paste a write-up or upload a README file. If no details are provided, a general-purpose test plan will be created.")
      gr.Markdown("---")
      with gr.Row():
        with gr.Column(scale=4):
          app_description = gr.Textbox(
            lines=10, 
            label="",
            placeholder="Describe the LLM App here or click \"Generate Test Plan\" to generate a general test plan for your LLM...")
        with gr.Column(scale=1):
          app_files = gr.File(
            file_types=[".md"], 
            file_count="multiple", 
            label="App README",
            elem_id="upload-container"
          )
      with gr.Row():
        generate_test_plan_btn = gr.Button("Generate Test Plan", elem_classes="green-button")
  # ./---------------------- Application Description ----------------------

  # ---------------------- Test Plan ----------------------
  with gr.Row(elem_id="output-container", visible=False) as tp: 
    with gr.Column():
      with gr.Row():
        with gr.Column(scale=4):
          gr.Markdown("## Test Plan")
          gr.Markdown("This section displays the generated test plan tailored to your application's context. You can export it as an Excel file and complete the tests offline using the provided prompts. Alternatively, you can complete the tests directly within the application by filling in the \"Actual Output\" column for each test case. Once all results are provided—either by uploading the completed Excel file or entering them manually - the tool will analyze the results and assess the associated risks based on frameworks such as MITRE ATLAS, NIST AI RMF, and OWASP LLM Top 10.")
      gr.Markdown("---")

      category_titles = []
      dataframe_outputs = []

      for i in range(MAX_CATEGORIES):
        title = gr.Markdown("## Category", visible=False)
        df = gr.Dataframe(visible=False, interactive=True, wrap=True)
        category_titles.append(title)
        dataframe_outputs.append(df)

      with gr.Row():
        submit_btn = gr.Button("Submit Test Results", elem_classes="green-button")
  # ./---------------------- Test Test Plan ----------------------

  # ---------------------- Risk Assessment ----------------------
  with gr.Row(elem_id="output-container", visible=False) as ra: 
    with gr.Column():
      with gr.Row():
        with gr.Column(scale=4):
          gr.Markdown("## Risk Assessment")
          gr.Markdown("Based on your test results, this section evaluates the level of risk and provides a structured report. It maps findings to recognized frameworks such as MITRE ATLAS, NIST AI RMF, and OWASP LLM Top 10.")
        with gr.Column(scale=1):
          generate_btn = gr.Button("📥 Export")
      gr.Markdown("---")
      gr.Markdown("Risk Assessment will appear here.", elem_classes="markdown-box")
  # ./---------------------- Risk Assessment ----------------------

  generate_test_plan_btn.click(
    fn=handle_generate,
    inputs=[app_description, app_files],
    outputs=[generate_test_plan_btn, generate_test_plan_btn, *category_titles, *dataframe_outputs, tp],
    show_progress=True,
    queue=True
  )

if __name__ == '__main__':
    demo.launch()

