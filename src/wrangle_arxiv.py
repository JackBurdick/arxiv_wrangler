import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def get_drive():

    gauth = GoogleAuth()

    # Try to load saved client credentials
    # https://stackoverflow.com/questions/24419188/automating-pydrive-verification-process
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")

    drive = GoogleDrive(gauth)
    return drive


def get_target_folder_id(
    drive, folder_name="TCF_papers", debug_print_folder_names=True
):
    # mimeType = 'application/vnd.google-apps.folder'
    # "q": "trashed=false"
    target_id = None
    # query information: https://developers.google.com/drive/api/v3/search-files
    folder_list = drive.ListFile(
        {"q": "mimeType = 'application/vnd.google-apps.folder'"}
    ).GetList()
    for folder in folder_list:
        if folder["title"] == folder_name:
            target_id = folder["id"]

    if not target_id:
        if debug_print_folder_names:
            print(f"all folders found: {[f['title'] for f in folder_list]}")

        raise ValueError(
            f"folder {folder_name} was not found in the drive -- please check spelling"
        )

    return target_id


def upload_file_to_specific_folder(drive, folder_id_to_upload_to, file_name):
    file_metadata = {
        "title": file_name,
        "parents": [{"id": folder_id_to_upload_to, "kind": "drive#childList"}],
    }

    file_drive = drive.CreateFile(file_metadata)

    file_drive.SetContentFile(f"{file_name}.pdf")

    # if you want to convert a file to a doc, can use, but this doesn't work
    # well for pdfs: file_drive.Upload({"convert": True})
    file_drive.Upload()


if __name__ == "__main__":
    pass
    # TODO: convert to cli

    drive = get_drive()

    # # txt_name = "file.txt"
    # pdf_name = "some_paper.pdf"

    # TODO: config -- currently hardcoded
    url = "https://arxiv.org/pdf/1707.08114"
    pdf_name = "new_paper"
    DRIVE_FOLDER_NAME = "TCF_papers"
    pdf_req = requests.get(url)
    open(f"{pdf_name}.pdf", "wb").write(pdf_req.content)

    folder_id = get_target_folder_id(drive, folder_name=DRIVE_FOLDER_NAME)
    upload_file_to_specific_folder(drive, folder_id, pdf_name)

    # TODO: get citation

    # TODO: add to bibfile
    # can select which bibfile/location

    # upload to google drive

    # TODO: send to remarkable
    # maybe: https://github.com/dvandyk/syncrm

    # TODO: create todoist item
    # maybe: https://github.com/Doist/todoist-python

    # TODO: delete local paper

    # url = "https://arxiv.org/abs/1707.08114/"

    # TODO: it would be interesting to be able to which papers are being downloaded

    #
