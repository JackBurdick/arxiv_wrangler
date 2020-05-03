from pathlib import Path

import requests
from bs4 import BeautifulSoup

from defaults import return_defaults


def write_local_pdf(pdf_req, pdf_name=None, local_dir_path=None):
    write_path = Path(local_dir_path).joinpath(f"{pdf_name}.pdf")
    open(write_path, "wb").write(pdf_req.content)
    return write_path


def get_citation_url(abs_url):

    # I don't remember how to use bs4, so this likely is not the best way to
    # approach this

    abs_resp = requests.get(abs_url)
    content = BeautifulSoup(abs_resp.content, "html.parser")

    # outer
    outter_class_id = "extra-services"
    content = content.find_all(attrs={"class": outter_class_id})
    if len(content) > 1:
        raise ValueError("content in {outter_class_id} is bigger than expected")
    else:
        content = content[0]

    # inner
    class_id = "dblp"
    content = content.find_all(attrs={"class": class_id})
    if len(content) > 1:
        raise ValueError("content in {outter_class_id} is bigger than expected")
    else:
        content = content[0]

    # ref link
    list_items = "a"
    content = content.find_all(list_items)
    href_url = None
    for item in content:
        href_str = item["href"]
        if "bibtex" in href_str:
            href_url = href_str

    if not href_url:
        raise ValueError(f"bibtex link not found in {content}")

    return href_url


def get_citation(abs_url):
    bibtex_url = get_citation_url(abs_url)

    # bibtex_resp = requests.get(bibtex_url)
    # content = BeautifulSoup(bibtex_resp.content, "html.parser")

    return bibtex_url


if __name__ == "__main__":
    pass
    # TODO: convert to cli
    defaults = return_defaults()

    # TODO: config -- currently hardcoded
    abs_url = "https://arxiv.org/abs/1707.08114"
    pdf_url = abs_url.replace("abs", "pdf")

    citation = get_citation(abs_url)
    print(citation)

    # for a in citation:
    #     print(a.prettify())

    # print(citation.prettify())

    # pdf_req = requests.get(pdf_url)

    # TODO: get citation

    # TODO: obtain name from citation
    # pdf_name = "new_paper"

    # # write local
    # local_pdf_path = write_local_pdf(
    #     pdf_req, pdf_name=pdf_name, local_dir_path=defaults["local_directory"]
    # )
    # print(f"pdf written locally: {local_pdf_path}")

    # # upload to google drive from local
    # upload_file_to_drive_folder(
    #     defaults["drive_folder_name"], pdf_name, local_pdf_path=local_pdf_path
    # )
    # print(f"pdf written to drive: {pdf_name}")

    # TODO: add to bibfile
    # can select which bibfile/location

    # TODO: send to remarkable
    # maybe: https://github.com/dvandyk/syncrm

    # TODO: create todoist item
    # maybe: https://github.com/Doist/todoist-python

    # TODO: maybe delete local paper

    # TODO: it would be interesting to be able to which papers are being
    # downloaded
