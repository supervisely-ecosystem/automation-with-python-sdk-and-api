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


module_id = api.app.get_ecosystem_module_id("supervisely-ecosystem/export-to-pascal-voc")
# module_id = 83  # or copy module ID of application in ecosystem
module_info = api.app.get_ecosystem_module_info(module_id)
print("Start app: ", module_info.name)

print("Help for developers with the list of all available parameters:")
module_info.arguments_help()

params = module_info.get_arguments(images_project=12489)
print("App input arguments with predefined default values:")
print(json.dumps(params, indent=4))

# Let's modify some optional input arguments:
params["trainSplitCoef"] = 0.7
params["pascalContourThickness"] = 2

# @TODO: fix queued
# Check validation
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
    api.task.wait(session.task_id, target_status=api.task.Status.FINISHED)

    # or infinite wait
    # api.task.wait(session.task_id)

    # it is also possible to limit execution time
    # in the example below maximum waiting time will be 5*3=15 seconds
    # api.task.wait(
    #     session.task_id,
    #     target_status=api.task.Status.FINISHED,
    #     wait_attempts=5,
    #     wait_attempt_timeout_sec=3,
    # )

except sly.WaitingTimeExceeded as e:
    print(e)
except sly.TaskFinishedWithError as e:
    print(e)

print("Task status: ", api.task.get_status(session.task_id))
