import os
from dotenv import load_dotenv
import supervisely as sly


load_dotenv("examples/start-stop-app/local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))
api = sly.Api()

team_id = sly.env.team_id()
