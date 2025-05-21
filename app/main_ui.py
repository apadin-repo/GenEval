import gradio as gr
from ui.style import Style
import os
from geneval.generate.test_plan import TestPlan
import pandas as pd
from tempfile import NamedTemporaryFile
import re
import tempfile
from markdown_pdf import MarkdownPdf, Section

# # TODO:
# - capture changes in the test plan 
# - When something changes in the df that is not the 'Actual Output' column, revert to original value?
# - review xml export, onoy 5 tabs?
# - Export PDF
# - another way to complete test plan?
# - take test plan and run risk assessmemnt, print assessment Markdown and PDF

TEST_PLAN = []
TEST_PLAN_DFS = []
CATEGORIES = TestPlan.get_categories()

def handle_generate(description, files):
  updates = [
    gr.update(interactive=False),
    gr.update(value="Generating test plan... This may take a few moments.")
  ]

  for _ in range(len(CATEGORIES)):
    updates.extend([
      gr.update(visible=False),  # Group
      gr.update(value=""),       # Title
      gr.update(value=""),       # Description
      gr.update(value=pd.DataFrame())  # Empty DataFrame
    ])

  updates.append(gr.update(visible=False))  # Hide container

  yield tuple(updates)

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
    
  for i, category in enumerate(CATEGORIES):
    
    df = TestPlan.generate(category['category'], context)
    
    TEST_PLAN_DFS.append(df)
    
    df.drop('Category', axis=1, inplace=True)
    df.drop('Actual Output', axis=1, inplace=True)
    
    TEST_PLAN.append({
      'title': category['category'],
      'description': category['description'],
      'test_plan': df
    })
    
    updates = [
      gr.update(interactive=False),
      gr.update(value="Generating test plan... This may take a few moments.")
    ]

    for i in range(len(CATEGORIES)):
      if i < len(TEST_PLAN):
        updates.extend([
          gr.update(visible=True),  # Group
          gr.update(value=f"### {TEST_PLAN[i]['title']}"),
          gr.update(value=TEST_PLAN[i]['description']),
          gr.update(value=TEST_PLAN[i]['test_plan'])
        ])
      else:
        updates.extend([
          gr.update(visible=False),  # Group
          gr.update(value=""),
          gr.update(value=""),
          gr.update(value=pd.DataFrame()),
        ])

    updates.append(gr.update(visible=True))  # Show container
    yield tuple(updates)

  updates[:2] = [ # Update the button when is done
      gr.update(interactive=True),
      gr.update(value="Generate Test Plan")
    ]

  yield tuple(updates)

def clean_sheet_name(name):
  return re.sub(r'[:\\/*?\[\]]', '', name)[:31]

def export_test_plan():
  result = pd.DataFrame()
  for df in TEST_PLAN_DFS:
      result = pd.concat([result, df], ignore_index=True)
  
  if not TEST_PLAN:
    return None
  
  with NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
    with pd.ExcelWriter(tmp.name, engine='xlsxwriter') as writer:
      result.to_excel(writer, sheet_name="Test Plan", index=False)
    return tmp.name

def export_test_pdf():
  md = TestPlan.get_test_plan_md()
  for idx, item in enumerate(TEST_PLAN, 1):
    md += f"## {idx}. {item['title']}\n\n"
    md += f"{item['description']}\n\n"

    df = item['test_plan']
    # df['Input'] = df['Input'].apply(lambda x: f"`{x}`")
    df['Expected Output'] = df['Expected Output'].apply(lambda x: f"`{x}`")

    md += df.to_markdown(index=False) + "\n\n"

  tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
  tmp_path = tmp.name

  # Generate PDF from markdown
  styled_md = f"""
<style>
table {{
  border-collapse: collapse;
  width: 100%;
}}
th, td {{
  border: 1px solid black;
  border-collapse: collapse;
  padding: 2px;
  text-align: left;
}}
</style>
{md}
"""


  pdf = MarkdownPdf()
  pdf.meta["title"] = "Markdown Export"
  pdf.add_section(Section(styled_md, toc=False))
  pdf.save(tmp_path)

  return tmp_path  # this becomes the downloadable file


# ----- UI -----
with gr.Blocks(title="GenAI Evaluation Tool", css=Style.CSS) as demo:
  # ---------------------- Application Description ----------------------
  with gr.Row():
    gr.Markdown("# GenAI Evaluation Tool")
  with gr.Row(elem_id="output-container"):
    with gr.Column(scale=1):
      gr.Markdown("# App Description (optional)")
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
        generate_test_plan_btn = gr.Button("Generate Test Plan")
  # ./---------------------- Application Description ----------------------

  # ---------------------- Test Plan ----------------------
  with gr.Row(elem_id="output-container", visible=True) as tp: 
    with gr.Column():
      with gr.Row():
        with gr.Column(scale=4):
          gr.Markdown("# Test Plan")
        with gr.Column(scale=1):
          export_btn = gr.DownloadButton("📥 Excel", visible=True)
        with gr.Column(scale=1):
          export_pdf = gr.DownloadButton("📥 PDF", visible=True)
          download_file = gr.File(label="Download PDF", visible=False)
      with gr.Row(): 
        gr.Markdown("This section displays the generated test plan tailored to your application\'s context. You can export it as an Excel file and complete the tests offline using the provided prompts. Alternatively, you can complete the tests directly within the application by filling in the \"Actual Output\" column for each test case. Once all results are provided - either by uploading the completed Excel file or entering them manually - the tool will analyze the results and assess the associated risks based on frameworks such as MITRE ATLAS, NIST AI RMF, and OWASP LLM Top 10.")
      gr.Markdown("---")

      with gr.Column(visible=False) as category_output_container:
        category_blocks = []
        for _ in range(len(CATEGORIES)): 
          with gr.Column(visible=False) as block:
            title = gr.Markdown()
            desc = gr.Markdown()
            df = gr.Dataframe(wrap=True, interactive=False)
            category_blocks.append((block, title, desc, df))

      with gr.Row():
        submit_btn = gr.Button("Submit Test Results", interactive=False)
  # ./---------------------- Test Test Plan ----------------------

  # ---------------------- Risk Assessment ----------------------
  with gr.Row(elem_id="output-container", visible=True) as ra: 
    with gr.Column():
      with gr.Row():
        with gr.Column(scale=4):
          gr.Markdown("# Risk Assessment")
          gr.Markdown("Based on your test results, this section evaluates the level of risk and provides a structured report. It maps findings to recognized frameworks such as MITRE ATLAS, NIST AI RMF, and OWASP LLM Top 10.")
        with gr.Column(scale=1):
          generate_btn = gr.Button("📥 Export")
      gr.Markdown("---")
      gr.Markdown("Risk Assessment will appear here.", elem_classes="markdown-box")
  # ./---------------------- Risk Assessment ----------------------

  generate_test_plan_btn.click(
    fn=handle_generate,
    inputs=[app_description, app_files],
    outputs=[
      generate_test_plan_btn,
      generate_test_plan_btn,
      *[c for block in category_blocks for c in block],
      category_output_container
    ],
    show_progress=True,
    queue=True
  )

  export_btn.click(
    fn=export_test_plan,
    inputs=[],
    outputs=[export_btn]
  )

  export_pdf.click(
    fn=export_test_pdf,
    inputs=[],
    outputs=[export_pdf]
  )

  export_pdf.click(fn=export_test_pdf, inputs=[], outputs=download_file)
  download_file.change(lambda x: gr.File(visible=True), inputs=download_file, outputs=download_file)



if __name__ == '__main__':
    demo.launch()