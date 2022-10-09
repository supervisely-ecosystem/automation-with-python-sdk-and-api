import os
from dotenv import load_dotenv
import supervisely as sly

load_dotenv("examples/start-stop-app/local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))
api = sly.Api()

team_id = sly.env.team_id()
workspace_id = sly.env.workspace_id()
agent_id = sly.env.agent_id()


module_id = 83  # module ID of application in ecosystem
module_id = api.app.get_ecosystem_module_id("supervisely-ecosystem/export-to-pascal-voc")
module_info = api.app.get_ecosystem_module_info(module_id)
print("Start app: ", module_info.name)

# optional arguments with default values from modal window before app started
app_args = module_info.get_arguments()

# -> module_info.validate_arguments(args)
api.app.start(
    agent_id=agent_id,
    module_id=module_id,
    workspace_id=workspace_id,
    task_name="custom session name",
    params=app_args,
)

# team_recent_apps = api.app.get_list(team_id)
# for app_info in team_recent_apps:
#     print(app_info.name)
