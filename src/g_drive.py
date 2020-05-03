from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


def _obtain_authenticated_drive():

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


def _get_target_folder_id(
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


def upload_file_to_drive_folder(drive_folder_name, file_name, local_pdf_path):

    drive = _obtain_authenticated_drive()

    folder_id = _get_target_folder_id(drive, folder_name=drive_folder_name)

    file_metadata = {
        "title": f"{file_name}.pdf",
        "parents": [{"id": folder_id, "kind": "drive#childList"}],
    }

    file_drive = drive.CreateFile(file_metadata)

    file_drive.SetContentFile(f"{local_pdf_path}")

    # if you want to convert a file to a doc, can use, but this doesn't work
    # well for pdfs: file_drive.Upload({"convert": True})
    file_drive.Upload()
