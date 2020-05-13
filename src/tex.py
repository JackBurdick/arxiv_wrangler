def does_citation_exist(path, citation):
    # see if citation already exists
    citation_exists = False
    with open(path) as fp:
        line = fp.readline()
        while line:
            if citation in line:
                citation_exists = True
                break
            line = fp.readline()
    return citation_exists


def write_to_bib_file(path, citation):

    # TODO: make sure citation isn't already present
    write_str = f"\n{citation}\n"
    with open(path, "a") as myfile:
        myfile.write(write_str)


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
