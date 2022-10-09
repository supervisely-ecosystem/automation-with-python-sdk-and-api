# Labeling Jobs automation

[Read this tutorial in developer portal.](#)

## Introduction

In this tutorial you will learn how to manage `Labeling Jobs` using Supervisely SDK and API. Please, read tutorial about working with `User` before proceeding.

📗 Everything you need to reproduce [this tutorial is on GitHub](https://github.com/supervisely-ecosystem/automation-with-python-sdk-and-api/tree/master/examples/user-automation): source code and demo data.

## How to debug this tutorial

**Step 1.** Prepare `~/supervisely.env` file with credentials. [Learn more here.](https://developer.supervise.ly/getting-started/basics-of-authentication#how-to-use-in-python)

**Step 2.** Clone [repository](https://github.com/supervisely-ecosystem/automation-with-python-sdk-and-api) with source code and demo data and create [Virtual Environment](https://docs.python.org/3/library/venv.html).

```bash
git clone https://github.com/supervisely-ecosystem/automation-with-python-sdk-and-api
cd automation-with-python-sdk-and-api
./create_venv.sh
```

**Step 3.** Open repository directory in Visual Studio Code.&#x20;

```bash
code -r .
```

**Step 4.** change ✅ IDs ✅ in `local.env` file by copying the IDs from Supervisely instance.

```python
CONTEXT_TEAMID=8                 # ⬅️ change it
CONTEXT_USERID=7                 # ⬅️ change it
CONTEXT_USERLOGIN="my_username"  # ⬅️ change it
```

**Step 5.** Start debugging `examples/user-automation/main.py`&#x20;

## User automation

### Import libraries

```python
import os
from dotenv import load_dotenv
import supervisely as sly
```

### Init API client
​
Init API for communicating with Supervisely Instance. First, we load environment variables with credentials:

```python
load_dotenv("local.env")
load_dotenv(os.path.expanduser("~/supervisely.env"))
api = sly.Api()
```

### Get your IDs and username from environment

```python
TEAM_ID = int(os.environ["CONTEXT_TEAMID"])
USER_ID = int(os.environ["CONTEXT_USERID"])
USER_LOGIN = os.environ(["CONTEXT_USERLOGIN"])
```

## Labeling jobs

Create accounts for annotators with restrictions (learn more here: https://docs.enterprise.supervise.ly/jobs/).
User will be able to login only after being added to at least one team.

```python
labeler01 = api.user.get_info_by_login(login='labeler_01')
if labeler01 is None:
    labeler01 = api.user.create(login='labeler_01', password='labeler01pass', is_restricted=True)

labeler02 = api.user.get_info_by_login(login='labeler_02')
if labeler02 is None:
    labeler02 = api.user.create(login='labeler_02', password='labeler02pass', is_restricted=True)
```

### Step 1. Before creating labeling Job, it is needed to add annotators to team

```python
team = api.team.get_info_by_name('max')
workspace = api.workspace.get_info_by_name(team.id, 'First Workspace')

if api.user.get_team_role(labeler01.id, team.id) is None:
    api.user.add_to_team(labeler01.id, team.id, api.role.DefaultRole.ANNOTATOR)
if api.user.get_team_role(labeler02.id, team.id) is None:
    api.user.add_to_team(labeler02.id, team.id, api.role.DefaultRole.ANNOTATOR)
```

### Step 2. Define project and datasets to label

```python
project = api.project.get_info_by_name(workspace.id, 'tutorial_project')
project_meta_json = api.project.get_meta(project.id)
project_meta = sly.ProjectMeta.from_json(project_meta_json)
print(project_meta)

# ProjectMeta:
# Object Classes
# +--------+-----------+----------------+
# |  Name  |   Shape   |     Color      |
# +--------+-----------+----------------+
# |  bike  | Rectangle | [246, 255, 0]  |
# |  car   |  Polygon  | [190, 85, 206] |
# |  dog   |  Polygon  |  [253, 0, 0]   |
# | person |   Bitmap  |  [0, 255, 18]  |
# +--------+-----------+----------------+
# Tags
# +---------------+--------------+-----------------------+
# |      Name     |  Value type  |    Possible values    |
# +---------------+--------------+-----------------------+
# |   car_color   |  any_string  |          None         |
# |  cars_number  |  any_number  |          None         |
# |      like     |     none     |          None         |
# | person_gender | oneof_string |   ['male', 'female']  |
# |    situated   | oneof_string | ['inside', 'outside'] |
# |  vehicle_age  | oneof_string | ['modern', 'vintage'] |
# +---------------+--------------+-----------------------+

datasets = api.dataset.get_list(project.id)
print(datasets)

# [
#   DatasetInfo(
#     id=1585, 
#     name='dataset_01',
#     description='', 
#     size='1277440',
#     project_id=511,
#     images_count=3, 
#     created_at='2019-07-18T15:39:57.377Z',
#     updated_at='2019-07-18T15:39:57.377Z'
#   ),
#    DatasetInfo(
#      id=1586,
#      name='dataset_02',
#      description='',
#      size='704971',
#      project_id=511,
#      images_count=2, 
#      created_at='2019-07-18T15:39:57.377Z',
#      updated_at='2019-07-18T15:39:57.377Z'
#   )
# ]
```

Labeler1 will label cars on the first dataset
```python
created_jobs = api.labeling_job.create(name='labeler1_cars_task',
                                       dataset_id=datasets[0].id,
                                       user_ids=[labeler01.id],
                                       readme='annotation manual for cars in markdown format here (optional)',
                                       description='short description is here (optional)',
                                       classes_to_label=["car"])
pprint.pprint(created_jobs)
[LabelingJobInfo(id=37, name='labeler1_cars_task (#18)', readme='annotation manual for cars in markdown format here (optional)', description='short description is here (optional)', team_id=4, workspace_id=7, workspace_name='First Workspace', project_id=511, project_name='tutorial_project', dataset_id=1585, dataset_name='dataset_01', created_by_id=4, created_by_login='max', assigned_to_id=29, assigned_to_login='labeler_01', created_at='2019-08-05T08:42:30.588Z', started_at=None, finished_at=None, status='pending', disabled=False, images_count=3, finished_images_count=0, rejected_images_count=0, accepted_images_count=0, classes_to_label=[], tags_to_label=[], images_range=(None, None), objects_limit_per_image=None, tags_limit_per_image=None, filter_images_by_tags=[], include_images_with_tags=[], exclude_images_with_tags=[])]
```

Stop Labeling Job, job will be unavailable for labeler

api.labeling_job.stop(created_jobs[0].id)
Labeler2 will label cars on the first dataset

```python
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
pprint.pprint(created_jobs)
[LabelingJobInfo(id=38, name='labeler2_task_with_complex_settings (#9)', readme='annotation manual for cars in markdown format here (optional)', description='short description is here (optional)', team_id=4, workspace_id=7, workspace_name='First Workspace', project_id=511, project_name='tutorial_project', dataset_id=1585, dataset_name='dataset_01', created_by_id=4, created_by_login='max', assigned_to_id=30, assigned_to_login='labeler_02', created_at='2019-08-05T08:42:36.092Z', started_at=None, finished_at=None, status='pending', disabled=False, images_count=3, finished_images_count=0, rejected_images_count=0, accepted_images_count=0, classes_to_label=[], tags_to_label=[], images_range=(None, None), objects_limit_per_image=2, tags_limit_per_image=5, filter_images_by_tags=[{'id': 4174, 'positive': False, 'name': 'situated'}], include_images_with_tags=[], exclude_images_with_tags=['situated'])]
```

Get all labeling jobs in a team

```python
jobs = api.labeling_job.get_list(team.id)
pprint.pprint(jobs)
[LabelingJobInfo(id=37, name='labeler1_cars_task (#18)', readme='annotation manual for cars in markdown format here (optional)', description='short description is here (optional)', team_id=4, workspace_id=7, workspace_name='First Workspace', project_id=511, project_name='tutorial_project', dataset_id=1585, dataset_name='dataset_01', created_by_id=4, created_by_login='max', assigned_to_id=29, assigned_to_login='labeler_01', created_at='2019-08-05T08:42:30.588Z', started_at=None, finished_at=None, status='stopped', disabled=False, images_count=3, finished_images_count=0, rejected_images_count=0, accepted_images_count=0, classes_to_label=[], tags_to_label=[], images_range=(None, None), objects_limit_per_image=None, tags_limit_per_image=None, filter_images_by_tags=[], include_images_with_tags=[], exclude_images_with_tags=[]),
 LabelingJobInfo(id=38, name='labeler2_task_with_complex_settings (#9)', readme='annotation manual for cars in markdown format here (optional)', description='short description is here (optional)', team_id=4, workspace_id=7, workspace_name='First Workspace', project_id=511, project_name='tutorial_project', dataset_id=1585, dataset_name='dataset_01', created_by_id=4, created_by_login='max', assigned_to_id=30, assigned_to_login='labeler_02', created_at='2019-08-05T08:42:36.092Z', started_at=None, finished_at=None, status='pending', disabled=False, images_count=3, finished_images_count=0, rejected_images_count=0, accepted_images_count=0, classes_to_label=[], tags_to_label=[], images_range=(None, None), objects_limit_per_image=2, tags_limit_per_image=5, filter_images_by_tags=[{'id': 4174, 'positive': False, 'title': 'situated'}], include_images_with_tags=[], exclude_images_with_tags=['situated'])]
```

Labeling Jobs Filtering (filters [created_by_id, assigned_to_id, project_id, dataset_id] can be used in various combinations)
Get all labeling that were created by user 'max'

```python
user = api.user.get_info_by_login('max')
jobs = api.labeling_job.get_list(team.id, created_by_id=user.id)
pprint.pprint(jobs)
[LabelingJobInfo(id=37, name='labeler1_cars_task (#18)', readme='annotation manual for cars in markdown format here (optional)', description='short description is here (optional)', team_id=4, workspace_id=7, workspace_name='First Workspace', project_id=511, project_name='tutorial_project', dataset_id=1585, dataset_name='dataset_01', created_by_id=4, created_by_login='max', assigned_to_id=29, assigned_to_login='labeler_01', created_at='2019-08-05T08:42:30.588Z', started_at=None, finished_at=None, status='stopped', disabled=False, images_count=3, finished_images_count=0, rejected_images_count=0, accepted_images_count=0, classes_to_label=[], tags_to_label=[], images_range=(None, None), objects_limit_per_image=None, tags_limit_per_image=None, filter_images_by_tags=[], include_images_with_tags=[], exclude_images_with_tags=[]),
 LabelingJobInfo(id=38, name='labeler2_task_with_complex_settings (#9)', readme='annotation manual for cars in markdown format here (optional)', description='short description is here (optional)', team_id=4, workspace_id=7, workspace_name='First Workspace', project_id=511, project_name='tutorial_project', dataset_id=1585, dataset_name='dataset_01', created_by_id=4, created_by_login='max', assigned_to_id=30, assigned_to_login='labeler_02', created_at='2019-08-05T08:42:36.092Z', started_at=None, finished_at=None, status='pending', disabled=False, images_count=3, finished_images_count=0, rejected_images_count=0, accepted_images_count=0, classes_to_label=[], tags_to_label=[], images_range=(None, None), objects_limit_per_image=2, tags_limit_per_image=5, filter_images_by_tags=[{'id': 4174, 'positive': False, 'title': 'situated'}], include_images_with_tags=[], exclude_images_with_tags=['situated'])]
```

Get all labeling that were created by user 'max' and were assigned to labeler02

```python
jobs = api.labeling_job.get_list(team.id, created_by_id=user.id, assigned_to_id=labeler02.id)
pprint.pprint(jobs)
[LabelingJobInfo(id=38, name='labeler2_task_with_complex_settings (#9)', readme='annotation manual for cars in markdown format here (optional)', description='short description is here (optional)', team_id=4, workspace_id=7, workspace_name='First Workspace', project_id=511, project_name='tutorial_project', dataset_id=1585, dataset_name='dataset_01', created_by_id=4, created_by_login='max', assigned_to_id=30, assigned_to_login='labeler_02', created_at='2019-08-05T08:42:36.092Z', started_at=None, finished_at=None, status='pending', disabled=False, images_count=3, finished_images_count=0, rejected_images_count=0, accepted_images_count=0, classes_to_label=[], tags_to_label=[], images_range=(None, None), objects_limit_per_image=2, tags_limit_per_image=5, filter_images_by_tags=[{'id': 4174, 'positive': False, 'title': 'situated'}], include_images_with_tags=[], exclude_images_with_tags=['situated'])]
```

Archive Labeling Job
```python
api.labeling_job.archive(jobs[0].id)
```

Get all active labeling jobs in a team

```python
jobs = api.labeling_job.get_list(team.id)
pprint.pprint(jobs)
[LabelingJobInfo(id=37, name='labeler1_cars_task (#18)', readme='annotation manual for cars in markdown format here (optional)', description='short description is here (optional)', team_id=4, workspace_id=7, workspace_name='First Workspace', project_id=511, project_name='tutorial_project', dataset_id=1585, dataset_name='dataset_01', created_by_id=4, created_by_login='max', assigned_to_id=29, assigned_to_login='labeler_01', created_at='2019-08-05T08:42:30.588Z', started_at=None, finished_at=None, status='stopped', disabled=False, images_count=3, finished_images_count=0, rejected_images_count=0, accepted_images_count=0, classes_to_label=[], tags_to_label=[], images_range=(None, None), objects_limit_per_image=None, tags_limit_per_image=None, filter_images_by_tags=[], include_images_with_tags=[], exclude_images_with_tags=[])]
```

### Labeling Jobs Statuses

`api.labeling_job.Status.PENDING` - labeling job is created, labeler still has not started
`api.labeling_job.Status.IN_PROGRESS` - labeler started, but not finished
`api.labeling_job.Status.ON_REVIEW` - labeler finished his job, reviewer is in progress
`api.labeling_job.Status.COMPLETED` - reviewer completed job
`api.labeling_job.Status.STOPPED` - job was stopped at some stage

```python
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
```
