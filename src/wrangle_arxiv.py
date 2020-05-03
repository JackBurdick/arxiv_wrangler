import requests

from defaults import return_defaults
from g_drive import upload_file_to_drive_folder

if __name__ == "__main__":
    pass
    # TODO: convert to cli
    defaults = return_defaults()

    # TODO: config -- currently hardcoded
    url = "https://arxiv.org/pdf/1707.08114"

    pdf_req = requests.get(url)
    open(f"{pdf_name}.pdf", "wb").write(pdf_req.content)

    # TODO: get citation

    # TODO: obtain name from citation
    pdf_name = "new_paper"

    # upload to google drive
    upload_file_to_drive_folder(defaults["drive_folder_name"], pdf_name)

    # TODO: add to bibfile
    # can select which bibfile/location

    # TODO: send to remarkable
    # maybe: https://github.com/dvandyk/syncrm

    # TODO: create todoist item
    # maybe: https://github.com/Doist/todoist-python

    # TODO: maybe delete local paper

    # TODO: it would be interesting to be able to which papers are being
    # downloaded
