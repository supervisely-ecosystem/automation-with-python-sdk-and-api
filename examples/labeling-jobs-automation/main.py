import os
from dotenv import load_dotenv
import supervisely as sly

from prepare_project import prepare_project

# for debug
load_dotenv(os.path.expanduser("~/supervisely.env"))
load_dotenv("local.env")
api = sly.Api()

# TEAM_ID = int(os.environ["CONTEXT_TEAMID"])
# PROJECT_ID = int(os.environ["CONTEXT_PROJECTID"])
# USER_ID = int(os.environ["CONTEXT_USERID"])
# USER_LOGIN = os.environ(["CONTEXT_USERLOGIN"])


TEAM_ID = 8
PROJECT_ID = 13487
USER_ID = 7
USER_LOGIN = "cxnt"

# populate project meta with classes and tag metas
prepare_project(api=api, id=PROJECT_ID)

# Step 1. Create and add annotators to the team, before creating Labeling Job

# create accounts for annotators with restrictions
labeler_1 = api.user.get_info_by_login(login='labeler_1')
if labeler_1 is None:
    labeler_1 = api.user.create(login='labeler_1', password='11111abc', is_restricted=True)

labeler_2 = api.user.get_info_by_login(login='labeler_2')
if labeler_2 is None:
    labeler_2 = api.user.create(login='labeler_2', password='22222abc', is_restricted=True)

# labelers will be able to login only after being added to at least one team
if api.user.get_team_role(labeler_1.id, TEAM_ID) is None:
    api.user.add_to_team(labeler_1.id, TEAM_ID, api.role.DefaultRole.ANNOTATOR)
if api.user.get_team_role(labeler_2.id, TEAM_ID) is None:
    api.user.add_to_team(labeler_2.id, TEAM_ID, api.role.DefaultRole.ANNOTATOR)

# # Step 2. Define project and datasets for labeling job
project_meta_json = api.project.get_meta(PROJECT_ID)
project_meta = sly.ProjectMeta.from_json(project_meta_json)
print(project_meta)

datasets = api.dataset.get_list(PROJECT_ID)
print(datasets)

# Labeler 1 will label lemons on the first dataset
created_jobs = api.labeling_job.create(name='labeler1_lemons_task',
                                       dataset_id=datasets[0].id,
                                       user_ids=[labeler_1.id],
                                       readme='annotation manual for fruits in markdown format here (optional)',
                                       description='short description is here (optional)',
                                       classes_to_label=["lemon"])
print(created_jobs)

# Stop Labeling Job, job will be unavailable for labeler
api.labeling_job.stop(created_jobs[0].id)

# Labeler 2 will label kiwis on the first dataset
created_jobs = api.labeling_job.create(name='labeler2_kiwi_task_with_complex_settings',
                                       dataset_id=datasets[0].id,
                                       user_ids=[labeler_2.id],
                                       readme='annotation manual for fruits in markdown format here (optional)',
                                       description='short description is here (optional)',
                                       classes_to_label=["kiwi"],
                                       objects_limit_per_image=10,
                                       tags_to_label=["size", "origin"],
                                       tags_limit_per_image=20,
                                       )
print(created_jobs)

# Get all labeling jobs in a team
jobs = api.labeling_job.get_list(TEAM_ID)
print(jobs)

# Labeling Jobs Filtering (filters [created_by_id, assigned_to_id, project_id, dataset_id] can be used in various combinations)
# Get all labeling jobs that were created by yourself
user = api.user.get_info_by_login(USER_LOGIN)
jobs = api.labeling_job.get_list(TEAM_ID, created_by_id=user.id)
print(jobs)

# Get all labeling jobs that were created by yourself and were assigned to labeler 2
jobs = api.labeling_job.get_list(TEAM_ID, created_by_id=user.id, assigned_to_id=labeler_2.id)
print(jobs)

# Get all active labeling jobs in a team
jobs = api.labeling_job.get_list(TEAM_ID)
print(jobs)

# Labeling Jobs Statuses
job_id = jobs[-2].id
api.labeling_job.get_status(job_id)
# <Status.STOPPED: 'stopped'>
job_id = jobs[-1].id
api.labeling_job.get_status(job_id)
# <Status.PENDING: 'pending'>

# Archive Labeling Job
api.labeling_job.archive(jobs[0].id)
