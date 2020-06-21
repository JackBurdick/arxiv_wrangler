import requests
from bs4 import BeautifulSoup


def _get_citation_url(abs_url, class_id, target_str):

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
    content = content.find_all(attrs={"class": class_id})
    if len(content) > 1:
        raise ValueError("content in {class_id} is bigger than expected")
    else:
        try:
            content = content[0]
        except IndexError:
            return None

    # ref link
    list_items = "a"
    content = content.find_all(list_items)
    href_url = None
    for item in content:
        href_str = item["href"]
        if target_str in href_str:
            href_url = href_str

    if not href_url:
        raise ValueError(f"{target_str} link not found in {content}")

    return href_url


def _get_dblp(abs_url):
    bibtex_url = _get_citation_url(abs_url, "dblp", "bibtex")
    if not bibtex_url:
        return None

    bibtex_resp = requests.get(bibtex_url)
    content = BeautifulSoup(bibtex_resp.content, "html.parser")

    # will obtain the bibtex reference
    outter_class_id = "verbatim select-on-click"
    content = content.find_all(attrs={"class": outter_class_id})

    if len(content) > 1:
        raise ValueError("content in {outter_class_id} is bigger than expected")

    try:
        # content may not exist
        content = content[0]
        citation = content.contents[0]
    except IndexError:
        citation = None

    return citation


def _get_semscholar(abs_url):
    scholar_url = _get_citation_url(abs_url, "extra-ref-cite", "semanticscholar")
    if not scholar_url:
        return None

    scholar_resp = requests.get(scholar_url)
    content = BeautifulSoup(scholar_resp.content, "html.parser")

    # will obtain the bibtex reference
    outter_class_id = "bibtex-citation"
    content = content.find_all(attrs={"class": outter_class_id})

    try:
        # content may not exist
        content = content[0]
        citation = content.contents[0]
    except IndexError:
        citation = None

    return citation


def get_citation(abs_url):

    # try obtaining citation from dblp first
    citation = _get_dblp(abs_url)
    if not citation:
        # try semantic scholar
        citation = _get_semscholar(abs_url)

        # gscholar is a pain.. I tried using scholarly, but google didn't like
        # my request to the citation and I decided to go this route instead.
        # I think a work around could be figured out, but I didn't bother to explore
        # """
        # Your client does not have permission to get URL
        # /scholar.bib?q=info:7shpF8Tg3oIJ:scholar.google.com/&
        # output=citation&scisdr=CgWZb6bDGAA:AAGBfm0AAAAAXu6i8_fJ5gdooYzTlm0D8AG7sL
        # -4XON9&scisig=AAGBfm0AAAAAXu6i8wQC2eKhzYKxziE5DxfwQfmVwToK&scisf=
        # 4&ct=citation&cd=-1&hl=en
        #  from this server. (Client IP address: xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx)

        # Please see Google's Terms of Service posted at http://www.google.com/terms_of_service.html
        # """

    if not citation:
        raise ValueError(f"no citation found in {content}")

    return citation


def get_title(citation):
    contents = []
    for c in citation.split(","):
        contents.extend(c.split("="))
    contents = [c.rstrip(" ").lstrip("\n").lstrip(" ") for c in contents]
    title_ind = contents.index("title")
    title_content = contents[title_ind + 1]

    start = title_content.find("{") + len("{")
    end = title_content.find("}")
    title = title_content[start:end]

    return title


def get_cite_id(citation):
    citation = citation.split(",")[0]
    cite_id = citation.split("{")[1]
    return cite_id
