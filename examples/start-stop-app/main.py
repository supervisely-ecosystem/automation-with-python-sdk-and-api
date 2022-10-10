import os
import json
from dotenv import load_dotenv
import supervisely as sly

load_dotenv("examples/start-stop-app/local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))
api = sly.Api()

team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
agent_id = sly.env.agent_id()
project_id = 12489  # ⬅️ change demo value to your one


module_id = api.app.get_ecosystem_module_id("supervisely-ecosystem/export-to-pascal-voc")
# module_id = 83  # or copy module ID of application in ecosystem
module_info = api.app.get_ecosystem_module_info(module_id)
print("Start app: ", module_info.name)

print("List of available app arguments for developers (like --help in terminal):")
module_info.arguments_help()

params = module_info.get_arguments(images_project=project_id)
print("App input arguments with predefined default values:")
print(json.dumps(params, indent=4))

# Let's modify some optional input arguments for this app:
params["trainSplitCoef"] = 0.7
params["pascalContourThickness"] = 2

# TODO: fix queued
# TODO: Check validation
session = api.app.start(
    agent_id=agent_id,
    module_id=module_id,
    workspace_id=workspace_id,
    task_name="custom session name",
    params=params,
)
print("App is started, task_id = ", session.task_id)
print(session)

try:
    # wait until task end or specific task status
    # api.app.wait(session.task_id, target_status=api.task.Status.FINISHED)

    # or infinite wait until task end
    # api.task.wait(session.task_id)

    # it is also possible to limit maximum waiting time
    # in the example below maximum waiting time will be 20*3=60 seconds
    api.app.wait(
        session.task_id,
        target_status=api.task.Status.FINISHED,
        attempts=20,
        attempt_delay_sec=3,
    )

except sly.WaitingTimeExceeded as e:
    print(e)
    # we don't want to wait more, let's stop our long-lived "zombie" task
    api.app.stop(session.task_id)
except sly.TaskFinishedWithError as e:
    print(e)

print("Task status: ", api.app.get_status(session.task_id))


# let's list all sessions of specific app in our team with additional optional filtering by statuses [finished]
sessions = api.app.get_sessions(
    team_id=team_id, module_id=module_id, statuses=[api.task.Status.FINISHED]
)
for session_info in sessions:
    print(session_info)
