import gradio as gr
from ui.style import Style
import os
from geneval.generate.test_plan import TestPlan
import json

def handle_generate_with_status(description, files):
    yield gr.update(interactive=False), "### Generating test plan... This may take a few moments.", gr.update(value="")
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
    result = json.dumps(TestPlan.generate(context), indent=2)
    yield gr.update(interactive=True), "", result 

def convertToMarkDown():
  pass

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
  with gr.Row(elem_id="output-container"):  
    with gr.Column():
      with gr.Row():
        with gr.Column(scale=4):
          gr.Markdown("## Test Plan")
          gr.Markdown("This section displays the generated test plan tailored to your application's context. You’ll also have the option to download it as an Excel file for offline review and execution.")
        with gr.Column(scale=1):
          generate_btn = gr.Button("📥 Export")
      gr.Markdown("---")
      status_message = gr.Markdown("", elem_id="status-message")
      test_plan_output = gr.Markdown("### Test Plan will appear here.", elem_classes="markdown-box")
  # ./---------------------- Test Plan ----------------------

  # ---------------------- Test Results ----------------------
  with gr.Row(elem_id="output-container"): 
    with gr.Column():
      with gr.Row():
        with gr.Column(scale=4):
          gr.Markdown("## Test Results")
          gr.Markdown("Upload your completed test plan or enter test results manually in this section. The tool will use this data to analyze how your application performed against each test scenario.")
        with gr.Column(scale=1):
          generate_btn = gr.Button("📤 Import")
      gr.Markdown("---")
      with gr.Row():
        gr.Textbox(label="Prompt", lines=3, interactive=False, value="This is the default input text")
        gr.Textbox(label="Actual Output", lines=3)
      with gr.Row():
        gr.Textbox(label="Prompt", lines=3, interactive=False, value="This is the default input text")
        gr.Textbox(label="Actual Output", lines=3)
      with gr.Row():
        generate_btn = gr.Button("Submit Test Results", elem_classes="green-button")
  # ./---------------------- Test Results ----------------------

  # ---------------------- Threat Mapping ----------------------
  with gr.Row(elem_id="output-container"): 
    with gr.Column():
      with gr.Row():
        with gr.Column(scale=4):
          gr.Markdown("## Risk Assessment")
          gr.Markdown("Based on your test results, this section evaluates the level of risk and provides a structured report. It maps findings to recognized frameworks such as MITRE ATLAS, NIST AI RMF, and OWASP LLM Top 10.")
        with gr.Column(scale=1):
          generate_btn = gr.Button("📥 Export")
      gr.Markdown("---")
      gr.Markdown("Risk Assessment will appear here.", elem_classes="markdown-box")
  # ./---------------------- Threat Mapping ----------------------

  generate_test_plan_btn.click(
    fn=handle_generate_with_status,
    inputs=[app_description, app_files],
    outputs=[generate_test_plan_btn, status_message, test_plan_output],
    show_progress=True,
    queue=True  # must use queue to support yield
  )

if __name__ == '__main__':
    demo.launch()

