import requests
from bs4 import BeautifulSoup


def _get_citation_url(abs_url):

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
        raise ValueError("content in {class_id} is bigger than expected")
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
    bibtex_url = _get_citation_url(abs_url)

    bibtex_resp = requests.get(bibtex_url)
    content = BeautifulSoup(bibtex_resp.content, "html.parser")

    # will obtain the bibtex reference
    outter_class_id = "verbatim select-on-click"
    content = content.find_all(attrs={"class": outter_class_id})

    if len(content) > 1:
        raise ValueError("content in {outter_class_id} is bigger than expected")
    else:
        content = content[0]

    # obtain citation
    citation = content.contents[0]
    if not citation:
        raise ValueError(f"no citation found in {content}")

    return citation
