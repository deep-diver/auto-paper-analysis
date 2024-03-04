import argparse
from paper.download import (
    download_pdf_from_arxiv,
    get_papers_from_hf_daily_papers
)
from paper.parser import extract_text_and_figures
from gen.gemini import get_basic_qa, get_deep_qa
from utils import push_to_hf_hub

def main(args):
    print("1. Get a list of papers from 🤗 Daily Papers")
    target_date, papers = get_papers_from_hf_daily_papers(args.target_date)
    print("...DONE")
    
    print("2. Generating QAs for the paper")
    for paper in papers:
        try:
            title = paper['title']
            abstract = paper['paper']['summary']
            arxiv_id = paper['paper']['id']
            authors = []

            print(f"...PROCESSING ON[{arxiv_id}, {title}]")
            print(f"......Extracting authors' names")
            for author in paper['paper']['authors']:
                if 'user' in author:
                    fullname = author['user']['fullname']
                else:
                    fullname = author['name']
                authors.append(fullname)
            print(f"......DONE")

            print(f"......Downloading the paper PDF")
            filename = download_pdf_from_arxiv(arxiv_id)
            print(f"......DONE")

            print(f"......Extracting text and figures")
            texts, figures = extract_text_and_figures(filename)
            text =' '.join(texts)
            print(f"......DONE")

            print(f"......Generating the seed(basic) QAs")
            qnas = get_basic_qa(text, gemini_api_key=args.gemini_api, trucate=30000)
            qnas['title'] = title
            qnas['abstract'] = abstract
            qnas['authors'] = ','.join(authors)
            qnas['arxiv_id'] = arxiv_id
            qnas['target_date'] = target_date
            qnas['full_text'] = text
            print(f"......DONE")

            print(f"......Generating the follow-up QAs")
            qnas = get_deep_qa(text, qnas, gemini_api_key=args.gemini_api, trucate=30000)
            del qnas["qna"]
            print(f"......DONE")

            print(f"......Exporting to HF Dataset repo at [{args.hf_repo_id}]")
            push_to_hf_hub(qnas, args.hf_repo_id, args.hf_token)
            print(f"......DONE")
        except:
            print(".......failed due to exception")
            continue

    print("...DONE")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="auto paper analysis")
    parser.add_argument("--gemini-api", type=str)
    parser.add_argument("--target-date", type=str, default=None)
    parser.add_argument("--hf-token", type=str)
    parser.add_argument("--hf-repo-id", type=str)
    args = parser.parse_args()

    main(args)