from todoist.api import TodoistAPI

from todoist_config import TODOIST_TOKEN


def create_todoist_task(
    task_name, citation_id, abs_url, project_name="arxiv_bucket", days_due=None
):

    # initialize
    api = TodoistAPI(TODOIST_TOKEN)
    api.sync()

    # obtain target project
    p_id = None
    projects = api.state["projects"]
    if not project_name in [p["name"] for p in projects]:
        # create
        arxiv_project = api.projects.add(f"{project_name}")
        p_id = arxiv_project["id"]
        api.commit()
    else:
        for project in projects:
            if project["name"] == f"{project_name}":
                p_id = project["id"]
    if not p_id:
        raise ValueError(f"project {project_name} could not be found")

    # add item if not present
    item_names = [item["content"] for item in api.state["items"]]
    if task_name not in item_names:
        due_dict = {"string": f"{str(days_due)} days from now"} if days_due else None
        cur_task = api.items.add(task_name, project_id=p_id, due=due_dict)

        comment_str = f"url: {abs_url}\n" f"citation: {citation_id}"
        _ = api.notes.add(cur_task["id"], comment_str)

        try:
            api.commit()
        except Exception as e:
            raise type(e)(f"project id may not have been found  - full error: {e}")
    else:
        # the item is already present
        pass
        # print(f"item {task_name} already in {project_name} and not added")
