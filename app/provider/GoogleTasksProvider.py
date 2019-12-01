from googleapiclient import discovery

from app.routes.auth.GoogleAuth import get_user_info, build_credentials


def get_data():
    service = discovery.build("tasks", "v1", credentials=build_credentials())
    tasks = {}
    task_lists = service.tasklists().list().execute()
    for task_list in task_lists["items"]:
        list_tasks = service.tasks().list(tasklist=task_list["id"], showCompleted=True, showHidden=True, maxResults=100).execute()
        tasks[task_list["title"]] = []
        tasks[task_list["title"]].extend(list_tasks["items"])
        while "nextPageToken" in list_tasks:
            list_tasks = service.tasks().list(tasklist=task_list["id"], showCompleted=True, showHidden=True, maxResults=100, pageToken=list_tasks["nextPageToken"]).execute()
            tasks[task_list["title"]].extend(list_tasks["items"])
    return tasks
