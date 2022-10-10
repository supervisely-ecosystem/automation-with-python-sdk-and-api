import os
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

print("Help for developers:")
module_info.arguments_help()

# validation on server
params = module_info.get_arguments(images_project=12489)

# @TODO: return namedtuple
# @TODO: fix queued
ppp = api.app.start(
    agent_id=agent_id,
    module_id=module_id,
    workspace_id=workspace_id,
    task_name="custom session name",
    params=params,
)
print(ppp)
