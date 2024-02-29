import requests

def _download_pdf_from_arxiv(arxiv_id):
    url = f'http://export.arxiv.org/pdf/{arxiv_id}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download pdf for arXiv id {arxiv_id}")

def download_pdf_from_arxiv(arxiv_id):
    filename = f"{arxiv_id}.pdf"
    pdf_content = _download_pdf_from_arxiv(arxiv_id)

    # Save the pdf content to a file
    with open(filename, "wb") as f:
        f.write(pdf_content)

    return filename
