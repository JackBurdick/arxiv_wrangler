def return_defaults():
    d = {}
    #d["drive_folder_name"] = "TCF_papers"
    d["local_directory"] = "./papers"
    d[
        "bib_path"
    ] = "/Users/leakymosfet/dev/github/teaching_a_computer_to_fish/latex_guidebook/arxiv.bib"
    d[
        "tex_path"
    ] = "/Users/leakymosfet/dev/github/teaching_a_computer_to_fish/latex_guidebook/research_to_include.tex"
    d["tex_wrap"] = "TD"
    d["todoist"] = {}
    d["todoist"]["project"] = "arxiv_bucket"
    d["todoist"]["days_due"] = None

    return d
