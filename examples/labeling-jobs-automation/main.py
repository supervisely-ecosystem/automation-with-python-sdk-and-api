import os
from dotenv import load_dotenv
import supervisely as sly

# for debug
load_dotenv(os.path.expanduser("~/supervisely.env"))
load_dotenv("local.env")
api = sly.Api()

USER_ID = int(os.environ["CONTEXT_USERID"])
TEAM_ID = int(os.environ["CONTEXT_TEAMID"])
USER_LOGIN = os.environ(["CONTEXT_USERLOGIN"])

# create accounts for annotators with restrictions (learn more here: https://docs.enterprise.supervise.ly/jobs/)
# user will be able to login only after being added to at least one command
labeler01 = api.user.get_info_by_login(login='labeler_01')
if labeler01 is None:
    labeler01 = api.user.create(login='labeler_01', password='labeler01pass', is_restricted=True)

labeler02 = api.user.get_info_by_login(login='labeler_02')
if labeler02 is None:
    labeler02 = api.user.create(login='labeler_02', password='labeler02pass', is_restricted=True)

# Step 1. Before creating labeling Job, it is needed to add annotators to team
team = api.team.get_info_by_name('max')
workspace = api.workspace.get_info_by_name(team.id, 'First Workspace')

if api.user.get_team_role(labeler01.id, team.id) is None:
    api.user.add_to_team(labeler01.id, team.id, api.role.DefaultRole.ANNOTATOR)
if api.user.get_team_role(labeler02.id, team.id) is None:
    api.user.add_to_team(labeler02.id, team.id, api.role.DefaultRole.ANNOTATOR)

# Step 2. Define project and datasets to label
project = api.project.get_info_by_name(workspace.id, 'tutorial_project')
project_meta_json = api.project.get_meta(project.id)
project_meta = sly.ProjectMeta.from_json(project_meta_json)
print(project_meta)

datasets = api.dataset.get_list(project.id)
print(datasets)

# Labeler1 will label cars on the first dataset
created_jobs = api.labeling_job.create(name='labeler1_cars_task',
                                       dataset_id=datasets[0].id,
                                       user_ids=[labeler01.id],
                                       readme='annotation manual for cars in markdown format here (optional)',
                                       description='short description is here (optional)',
                                       classes_to_label=["car"])
print(created_jobs)
# Stop Labeling Job, job will be unavailable for labeler
api.labeling_job.stop(created_jobs[0].id)
# Labeler2 will label cars on the first dataset
created_jobs = api.labeling_job.create(name='labeler2_task_with_complex_settings',
                                       dataset_id=datasets[0].id,
                                       user_ids=[labeler02.id],
                                       readme='annotation manual for cars in markdown format here (optional)',
                                       description='short description is here (optional)',
                                       classes_to_label=["car", 'bike'],
                                       objects_limit_per_image=2,
                                       tags_to_label=["car_color", "vehicle_age"],
                                       tags_limit_per_image=5,
                                       exclude_images_with_tags=["situated"]
                                       )
print(created_jobs)

# Get all labeling jobs in a team
jobs = api.labeling_job.get_list(team.id)
print(jobs)
# Labeling Jobs Filtering (filters [created_by_id, assigned_to_id, project_id, dataset_id] can be used in various combinations)
# Get all labeling that were created by user 'max'
user = api.user.get_info_by_login('max')
jobs = api.labeling_job.get_list(team.id, created_by_id=user.id)
print(jobs)

# Get all labeling that were created by user 'max' and were assigned to labeler02
jobs = api.labeling_job.get_list(team.id, created_by_id=user.id, assigned_to_id=labeler02.id)
print(jobs)
# Archive Labeling Job
api.labeling_job.archive(jobs[0].id)
# Get all active labeling jobs in a team
jobs = api.labeling_job.get_list(team.id)
print(jobs)

# Labeling Jobs Statuses
job_id = 37
api.labeling_job.get_status(job_id)
# <Status.STOPPED: 'stopped'>
job_id = 39
api.labeling_job.get_status(job_id)
# <Status.PENDING: 'pending'>
api.labeling_job.wait(job_id, target_status=api.labeling_job.Status.ON_REVIEW) # it means that labeler is finished 
print('Labeler finished his work')
api.labeling_job.wait(job_id, target_status=api.labeling_job.Status.COMPLETED) # it meant that reviewer is finished
print('Reviewer finished job review')
