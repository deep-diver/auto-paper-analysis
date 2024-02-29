import argparse
import gradio as gr
from paper.download import download_pdf_from_arxiv
from paper.parser import extract_text_and_figures
from gen.gemini import get_basic_qa
from constants.style import STYLE

def main(args):
    filename = download_pdf_from_arxiv(args.arxiv_id)
    texts, figures = extract_text_and_figures(filename)
    text =' '.join(texts)

    basic_qa = get_basic_qa(text, gemini_api_key=args.gemini_api, trucate=30000)
    print(basic_qa)

    with gr.Blocks(css=STYLE) as demo:
        gr.Markdown("hello world")
    #   gr.Markdown(f"# {qna_json['title']}")
    #   gr.Markdown(f"{qna_json['summary']}", elem_classes=["small-font"])

    #   gr.Markdown("## Auto generated Questions & Answers")

    #   for qna in qnas:
    #     with gr.Column(elem_classes=["group"]):
    #       gr.Markdown(f"## 🙋 {qna['question']}")
    #       gr.Markdown(f"↪ **(ELI5)** {qna['answers']['eli5']}", elem_classes=["small-font"])
    #       gr.Markdown(f"↪ **(Technical)** {qna['answers']['expert']}", elem_classes=["small-font"])

    #       with gr.Accordion("Additional question #1", open=False, elem_classes=["accordion"]):
    #         gr.Markdown(f"## 🙋🙋 {qna['additional_depth_q']['follow up question']}")
    #         gr.Markdown(f"↪ **(ELI5)** {qna['additional_depth_q']['answers']['eli5']}", elem_classes=["small-font"])
    #         gr.Markdown(f"↪ **(Technical)** {qna['additional_depth_q']['answers']['expert']}", elem_classes=["small-font"])

    #       with gr.Accordion("Additional question #2", open=False, elem_classes=["accordion"]):
    #         gr.Markdown(f"## 🙋🙋 {qna['additional_breath_q']['follow up question']}")
    #         gr.Markdown(f"↪ **(ELI5)** {qna['additional_breath_q']['answers']['eli5']}", elem_classes=["small-font"])
    #         gr.Markdown(f"↪ **(Technical)** {qna['additional_breath_q']['answers']['expert']}", elem_classes=["small-font"])

    demo.launch(share=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="auto paper analysis")
    parser.add_argument("--gemini-api", type=str, default=None)
    parser.add_argument("--arxiv-id", type=str)
    args = parser.parse_args()

    main(args)