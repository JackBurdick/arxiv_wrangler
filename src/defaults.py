def return_defaults():
    d = {}
    d["drive_folder_name"] = "TCF_papers"
    d["local_directory"] = "./papers"
    d[
        "bib_path"
    ] = "/home/jackburdick/dev/github/running_with_tensors/latex_guidebook/arxiv.bib"
    d[
        "tex_path"
    ] = "/home/jackburdick/dev/github/running_with_tensors/latex_guidebook/research_to_include.tex"
    d["tex_wrap"] = "TD"
    d["todoist"] = {}
    d["todoist"]["project"] = "arxiv_bucket"
    d["todoist"]["days_due"] = None

    return d
