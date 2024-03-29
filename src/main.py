from pathlib import Path

import requests
import typer

from citation import get_citation, get_cite_id, get_title
from defaults import return_defaults
from g_drive import upload_file_to_drive_folder
from tex import does_citation_exist, write_to_bib_file, write_to_tex_file
from todo import create_todoist_task


def write_local_pdf(pdf_req, pdf_name=None, local_dir_path=None):
    Path(local_dir_path).mkdir(parents=True, exist_ok=True)
    write_path = Path(local_dir_path).joinpath(f"{pdf_name}.pdf")
    with open(write_path, "wb") as fh:
        fh.write(pdf_req.content)
    return write_path


def main(raw_url: str):

    # only support arxiv so far
    if not raw_url.startswith("https://arxiv.org"):
        raise ValueError(f"please use arxiv.org/abs url, not {raw_url}")

    if ".org/pdf/" in raw_url:
        raw_url = raw_url.replace("/pdf/", "/abs/")
        abs_url = raw_url.rstrip("pdf").rstrip(".")
    else:
        abs_url = raw_url

    # TODO: add logging + verbosity flag

    defaults = return_defaults()

    # obtain citation
    citation = get_citation(abs_url)
    pdf_title = get_title(citation)
    citation_id = get_cite_id(citation)

    # obtain PDF data
    pdf_url = abs_url.replace("abs", "pdf")
    pdf_req = requests.get(pdf_url)

    # write local, will overwrite current file
    pdf_name = citation_id.replace(":", "_").replace("/", "_")
    local_pdf_path = write_local_pdf(
        pdf_req, pdf_name=pdf_name, local_dir_path=defaults["local_directory"]
    )

    # upload to google drive from local, if not present
    try:
        upload_file_to_drive_folder(
            defaults["drive_folder_name"], pdf_name, local_pdf_path=local_pdf_path
        )
    except KeyError:
        pass

    # add to specified bib file and tex file if not already present in bib file
    # TODO: change this citation generation + look up to scholar
    citation_exists = does_citation_exist(defaults["bib_path"], citation_id)
    if citation_exists:
        print(f"already cited: {citation_id} \n(in: {defaults['bib_path']})")
    else:
        print(citation_id)
        write_to_bib_file(defaults["bib_path"], citation)

        write_to_tex_file(
            defaults["tex_path"], pdf_title, citation_id, defaults["tex_wrap"]
        )

    # create todoist item if not exist
    create_todoist_task(
        pdf_title,
        citation_id,
        abs_url,
        project_name=defaults["todoist"]["project"],
        days_due=defaults["todoist"]["days_due"],
    )

    # TODO: remarkable https://github.com/reHackable/awesome-reMarkable

    # TODO: it would be interesting to be able to which papers are being
    # downloaded


if __name__ == "__main__":
    typer.run(main)
