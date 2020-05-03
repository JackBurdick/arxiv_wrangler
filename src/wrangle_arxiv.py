from pathlib import Path

from citation import get_citation, get_cite_id, get_title
from defaults import return_defaults


def write_local_pdf(pdf_req, pdf_name=None, local_dir_path=None):
    write_path = Path(local_dir_path).joinpath(f"{pdf_name}.pdf")
    open(write_path, "wb").write(pdf_req.content)
    return write_path


if __name__ == "__main__":
    pass
    # TODO: convert to cli
    defaults = return_defaults()

    # TODO: config -- currently hardcoded
    abs_url = "https://arxiv.org/abs/1707.08114"

    # get citation
    citation = get_citation(abs_url)
    print("citation obtained")

    pdf_title = get_title(citation)
    print(pdf_title)

    citation_id = get_cite_id(citation)
    print(citation_id)

    pdf_url = abs_url.replace("abs", "pdf")

    # pdf_req = requests.get(pdf_url)

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
