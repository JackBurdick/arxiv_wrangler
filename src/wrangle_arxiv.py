from pathlib import Path

import requests

from citation import get_citation, get_cite_id, get_title
from defaults import return_defaults
from g_drive import upload_file_to_drive_folder


def write_local_pdf(pdf_req, pdf_name=None, local_dir_path=None):
    write_path = Path(local_dir_path).joinpath(f"{pdf_name}.pdf")
    open(write_path, "wb").write(pdf_req.content)
    return write_path


def write_to_bib_file(path, citation):
    # TODO: make sure citation isn't already present
    with open(path, "a") as myfile:
        myfile.write(citation)


def write_to_tex_file(tex_path, pdf_title, citation_id, tex_wrap):
    # NOTE: only run if `write_to_bib_file` completes (which will check if it
    # is already cited).
    write_str = f"{pdf_title} \\cite{{{citation_id}}}"
    if tex_wrap:
        write_str = f"\\{tex_wrap}{{{write_str}}}"

    # wrap in new lines
    write_str = f"\n{write_str}\n"

    with open(tex_path, "a") as myfile:
        myfile.write(write_str)


if __name__ == "__main__":
    pass
    # TODO: convert to cli
    defaults = return_defaults()

    # TODO: config -- currently hardcoded
    abs_url = "https://arxiv.org/abs/1707.08114"

    # get citation
    citation = get_citation(abs_url)

    pdf_title = get_title(citation)
    citation_id = get_cite_id(citation)

    pdf_url = abs_url.replace("abs", "pdf")

    pdf_req = requests.get(pdf_url)

    # write local
    pdf_name = citation_id.replace(":", "_").replace("/", "_")
    local_pdf_path = write_local_pdf(
        pdf_req, pdf_name=pdf_name, local_dir_path=defaults["local_directory"]
    )
    print(f"pdf written locally: {local_pdf_path}")

    # upload to google drive from local
    upload_file_to_drive_folder(
        defaults["drive_folder_name"], pdf_name, local_pdf_path=local_pdf_path
    )
    print(f"pdf written to drive: {pdf_name}")

    # TODO: add to bibfile
    # can select which bibfile/location
    write_to_bib_file(defaults["bib_path"], citation)
    print("citation written to bibfile")

    # TODO: create TD citation in .tex file
    write_to_tex_file(
        defaults["tex_path"], pdf_title, citation_id, defaults["tex_wrap"]
    )
    print("citation written to texfile")

    # TODO: send to remarkable
    # maybe: https://github.com/dvandyk/syncrm

    # TODO: create todoist item
    # maybe: https://github.com/Doist/todoist-python

    # TODO: maybe delete local paper

    # TODO: it would be interesting to be able to which papers are being
    # downloaded
