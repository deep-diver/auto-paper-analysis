import gradio as gr

STYLE = """
.small-font{
  font-size: 12pt !important;
}

.small-font:hover {
  font-size: 20px !important;
  transition: font-size 0.3s ease-out;
  transition-delay: 0.3s;
}

.group {
  padding-left: 10px;
  padding-right: 10px;
  padding-bottom: 10px;
  border: 2px dashed gray;
  border-radius: 20px;
  box-shadow: 5px 3px 10px 1px rgba(0, 0, 0, 0.4) !important;
}

.accordion > button > span{
  font-size: 12pt !important;
}

.accordion {
  border-style: dashed !important;
  border-left-width: 2px !important;
  border-bottom-width: 2.5px !important;
  border-top: none !important;
  border-right: none !important;
  box-shadow: none !important;
}
"""

with gr.Blocks(css=STYLE) as demo:
  gr.Markdown(f"# {qna_json['title']}")
  gr.Markdown(f"{qna_json['summary']}", elem_classes=["small-font"])

  gr.Markdown("## Auto generated Questions & Answers")

  for qna in qnas:
    with gr.Column(elem_classes=["group"]):
      gr.Markdown(f"## 🙋 {qna['question']}")
      gr.Markdown(f"↪ **(ELI5)** {qna['answers']['eli5']}", elem_classes=["small-font"])
      gr.Markdown(f"↪ **(Technical)** {qna['answers']['expert']}", elem_classes=["small-font"])

      with gr.Accordion("Additional question #1", open=False, elem_classes=["accordion"]):
        gr.Markdown(f"## 🙋🙋 {qna['additional_depth_q']['follow up question']}")
        gr.Markdown(f"↪ **(ELI5)** {qna['additional_depth_q']['answers']['eli5']}", elem_classes=["small-font"])
        gr.Markdown(f"↪ **(Technical)** {qna['additional_depth_q']['answers']['expert']}", elem_classes=["small-font"])

      with gr.Accordion("Additional question #2", open=False, elem_classes=["accordion"]):
        gr.Markdown(f"## 🙋🙋 {qna['additional_breath_q']['follow up question']}")
        gr.Markdown(f"↪ **(ELI5)** {qna['additional_breath_q']['answers']['eli5']}", elem_classes=["small-font"])
        gr.Markdown(f"↪ **(Technical)** {qna['additional_breath_q']['answers']['expert']}", elem_classes=["small-font"])

demo.launch(share=True)