import json
import datetime
import requests
from requests.exceptions import HTTPError

def _get_today():
    return str(datetime.date.today())

def _download_pdf_from_arxiv(filename):
    url = f'https://arxiv.org/pdf/{filename}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to download pdf for arXiv id {filename}")

def download_pdf_from_arxiv(arxiv_id):
    filename = f"{arxiv_id}.pdf"
    pdf_content = _download_pdf_from_arxiv(filename)

    # Save the pdf content to a file
    with open(filename, "wb") as f:
        f.write(pdf_content)

    return filename

def _get_papers_from_hf_daily_papers(target_date):
    if target_date is None:
        target_date = _get_today()
    url = f"https://huggingface.co/api/daily_papers?date={target_date}"

    response = requests.get(url)

    if response.status_code == 200:
        return target_date, response.text
    else:
        raise HTTPError(f"Error fetching data. Status code: {response.status_code}")

def get_papers_from_hf_daily_papers(target_date):
    target_date, results = _get_papers_from_hf_daily_papers(target_date)
    return target_date, json.loads(results)