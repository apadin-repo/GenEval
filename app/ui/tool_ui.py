import gradio as gr
from ui.style import Style

class Gradio_UI:

  def __init__(self, test_plan, threat_modeling):
    self.UI = self.build_ui(test_plan, threat_modeling)

  def dummy_generate(self, description, files):
      return "## Toxicity\nHigh Risk detected.\n\n## Bias & Fairness\nSome test cases here..."

  def dummy_assess(self, input_text):
      return f"Processed Output: {input_text}"

  def build_ui(self, test_plan, threat_mapping):
    with gr.Blocks(title="GenAI Evaluation Tool", css=Style.CSS) as demo:
      
      # ---------------------- Application Description ----------------------
      with gr.Row():
          gr.Markdown("# GenAI Evaluation Tool")
      with gr.Row(elem_id="output-container"):
        with gr.Column(scale=1):
          gr.Markdown("## Application Description")
          gr.Markdown("---")
          with gr.Row():
            with gr.Column(scale=4):
              app_description = gr.Textbox(
                  lines=10, 
                  label="",
                  placeholder="Describe the LLM App here..."
              )
            with gr.Column(scale=1):
              app_files = gr.File(
                file_types=[".pdf", ".md", ".txt"], 
                file_count="multiple", 
                label="Application Documentation",
                elem_id="upload-container"
              )
          with gr.Row():
            generate_btn = gr.Button("Generate Test Plan", elem_classes="green-button")
      # ./---------------------- Application Description ----------------------
    
      # ---------------------- Test Plan ----------------------
      with gr.Row(elem_id="output-container"):  
        with gr.Column():
          with gr.Row():
            with gr.Column(scale=4):
              gr.Markdown("## Test Plan")
            with gr.Column(scale=1):
              generate_btn = gr.Button("📥 Download Report")
          gr.Markdown("---")
          gr.Markdown(test_plan, elem_classes="markdown-box")
      # ./---------------------- Test Plan ----------------------

      # ---------------------- Test Results ----------------------
      with gr.Row(elem_id="output-container"): 
        with gr.Column():
          with gr.Row():
            with gr.Column(scale=4):
              gr.Markdown("## Test Results")
            with gr.Column(scale=1):
              generate_btn = gr.Button("📤 Upload Test")
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
              gr.Markdown("## Threat Mapping")
            with gr.Column(scale=1):
              generate_btn = gr.Button("📥 Export")
          gr.Markdown("---")
          gr.Markdown(threat_mapping, elem_classes="markdown-box")
      # ./---------------------- Threat Mapping ----------------------

    return demo

