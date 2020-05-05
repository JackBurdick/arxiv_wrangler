def return_defaults():
    d = {}
    d["drive_folder_name"] = "TCF_papers"
    d["local_directory"] = "."
    d["bib_path"] = "mybib.bib"
    d["tex_path"] = "mytex.tex"
    d["tex_wrap"] = "TD"
    d["todoist"] = {}
    d["todoist"]["project"] = "arxiv_bucket"
    d["todoist"]["days_due"] = None

    return d
