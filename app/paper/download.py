import re
import json
import requests
import datetime
from datetime import date
from datetime import datetime
import xml.etree.ElementTree as ET
from requests.exceptions import HTTPError

def _get_today():
    return str(date.today())

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
        print(f"target_date is not set => scrap today's papers [{target_date}]")
    url = f"https://huggingface.co/api/daily_papers?date={target_date}"

    response = requests.get(url)

    if response.status_code == 200:
        return target_date, response.text
    else:
        raise HTTPError(f"Error fetching data. Status code: {response.status_code}")

def get_papers_from_hf_daily_papers(target_date):
    target_date, results = _get_papers_from_hf_daily_papers(target_date)
    results = json.loads(results)
    for result in results:
        result["target_date"] = target_date
    return target_date, results


def _get_paper_xml_by_arxiv_id(arxiv_id):
    url = f"http://export.arxiv.org/api/query?search_query=id:{arxiv_id}&start=0&max_results=1"
    return requests.get(url)

def _is_arxiv_id_valid(arxiv_id):
  pattern = r"^\d{4}\.\d{5}$" 
  return bool(re.match(pattern, arxiv_id))

def _get_paper_metadata_by_arxiv_id(response):
    root = ET.fromstring(response.content)

    # Example: Extracting title, authors, and abstract
    title = root.find('{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}title').text
    authors = [author.find('{http://www.w3.org/2005/Atom}name').text for author in root.findall('{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}author')]
    abstract = root.find('{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}summary').text
    target_date = root.find('{http://www.w3.org/2005/Atom}entry/{http://www.w3.org/2005/Atom}published').text    

    return title, authors, abstract, target_date

def get_papers_from_arxiv_ids(arxiv_ids):
    results = []

    for arxiv_id in arxiv_ids:
        print(arxiv_id)
        if _is_arxiv_id_valid(arxiv_id):
            try:
                xml_data = _get_paper_xml_by_arxiv_id(arxiv_id)
                title, authors, abstract, target_date = _get_paper_metadata_by_arxiv_id(xml_data)

                datetime_obj = datetime.strptime(target_date, "%Y-%m-%dT%H:%M:%SZ")
                formatted_date = datetime_obj.strftime("%Y-%m-%d")

                results.append(
                    {
                        "title": title,
                        "target_date": formatted_date,
                        "paper": {
                            "summary": abstract,
                            "id": arxiv_id,
                            "authors" : authors,
                        }
                    }
                )
            except:
                print("......something wrong happend when downloading metadata")
                print("......this usually happens when you try out the today's published paper")
                continue
        else:
            print(f"......not a valid arXiv ID[{arxiv_id}]")

    return results