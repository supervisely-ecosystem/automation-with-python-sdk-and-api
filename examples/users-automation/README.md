# Users automation

[Read this tutorial in developer portal.](#)

## Introduction

In this tutorial you will learn how to work with `User` and manage team members using Supervisely SDK and API.

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
CONTEXT_USERID=7          # ⬅️ change it
CONTEXT_TEAMID=8          # ⬅️ change it
CONTEXT_WORKSPACEID=349   # ⬅️ change it
CONTEXT_USERLOGIN="your_username"  # ⬅️ change it
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
USER_ID = os.environ.get("CONTEXT_USERID")
TEAM_ID = os.environ.get("CONTEXT_TEAMID")
WORKSPACE_ID = os.environ.get("CONTEXT_WORKSPACEID")

USER_LOGIN = os.environ.get("CONTEXT_USERLOGIN")
```

### Print all roles that are available on private Supervisely instance

```python
roles = api.role.get_list()
print(roles)
# [
#   RoleInfo(id=1, role='admin', created_at='2019-04-11T10:52:06.517Z', updated_at='2019-04-11T10:52:06.517Z'),
#   RoleInfo(id=2, role='developer', created_at='2019-04-11T10:52:06.517Z', updated_at='2019-04-11T10:52:06.517Z'),
#   RoleInfo(id=3, role='annotator', created_at='2019-04-11T10:52:06.517Z', updated_at='2019-04-11T10:52:06.517Z'),
#   RoleInfo(id=4, role='viewer', created_at='2019-04-11T10:52:06.517Z', updated_at='2019-04-11T10:52:06.517Z')
# ]
```

### List all registered users

```python
users = api.user.get_list()
print('Total number of users: ', len(users))
for user in users:
    print("Id: {:<5} Login: {:<25s} logins_count: {:<5}".format(user.id, user.login, user.logins))
# Total number of users:  22
# Id: 1     Login: admin                     logins_count: 88   
# Id: 2     Login: supervisely               logins_count: 0    
# Id: 3     Login: andrew                    logins_count: 18   
# Id: 4     Login: max                       logins_count: 7    
# Id: 5     Login: antonc                    logins_count: 24   
# Id: 6     Login: umar                      logins_count: 9    
# Id: 7     Login: test1                     logins_count: 2    
# Id: 8     Login: denis                     logins_count: 1    
# Id: 9     Login: denis2                    logins_count: 0    
# Id: 10    Login: test2                     logins_count: 1    
# Id: 11    Login: test3                     logins_count: 2    
# Id: 12    Login: umar1                     logins_count: 2    
# Id: 13    Login: anna                      logins_count: 1    
# Id: 14    Login: demo_user                 logins_count: 0    
# Id: 20    Login: demo_user1                logins_count: 0    
# Id: 22    Login: demo_user2                logins_count: 0    
# Id: 24    Login: demo_user3                logins_count: 0    
# Id: 25    Login: demo_user4                logins_count: 0    
# Id: 29    Login: labeler_01                logins_count: 0    
# Id: 30    Login: labeler_02                logins_count: 0    
# Id: 31    Login: labeler_03                logins_count: 0    
# Id: 32    Login: alex                      logins_count: 0    
```

### Get UserInfo by ID

```python
user_info = api.user.get_info_by_id(USER_ID)
print(user_info)
# UserInfo(
#   id=14, 
#   login='demo_user', 
#   name='', 
#   email=None, 
#   logins=0,
#   disabled=False, 
#   last_login=None,
#   created_at='2019-07-18T15:57:27.271Z', 
#   updated_at='2019-07-18T15:57:27.271Z'
# )
```

### Get UserInfo by login

```python
user_info = api.user.get_info_by_login(USER_LOGIN)
print(user_info)
# UserInfo(
#   id=4, 
#   login='max', 
#   name='max_k', 
#   email=None, 
#   logins=7, 
#   disabled=False, 
#   last_login='2019-08-02T09:18:09.155Z', 
#   created_at='2019-04-11T10:59:50.472Z', 
#   updated_at='2019-08-04T17:06:39.414Z'
# )
```

### Update user info

```python
new_password = '123321'
new_name = 'max_k'
user_info = api.user.update(user_info.id, password=new_password, name=new_name)
print(user_info)
# UserInfo(
#   id=4, 
#   login='max', 
#   name='max_k', 
#   email=None, 
#   logins=7, 
#   disabled=False, 
#   last_login='2019-08-02T09:18:09.155Z', 
#   created_at='2019-04-11T10:59:50.472Z', 
#   updated_at='2019-08-05T08:42:20.463Z'
# )
```

### Get User Membership (list all user teams with corresponding roles)

```python
def print_user_teams(login):
    user = api.user.get_info_by_login(login)
    user_teams = api.user.get_teams(user.id)
    print("\nTeams of user {!r}:".format(login))
    for team in user_teams:
        print("[team_id={}] {:<25s} [role_id={}] {}".format(team.id, team.name, team.role_id, team.role))

print_user_teams(USER_LOGIN)
# Teams of user 'andrew':
# [team_id=7] team_x                    [role_id=1] admin
# [team_id=3] jupyter_tutorials         [role_id=1] admin
```

### Create new user

```python
new_user = api.user.get_info_by_login('demo_user4')
if new_user is None:
    new_user = api.user.create(login='demo_user4', password='123abc', is_restricted=False)
print(new_user)
# UserInfo(
#   id=25, 
#   login='demo_user4',
#   name='',
#   email=None,
#   logins=0,
#   disabled=False,
#   last_login=None,
#   created_at='2019-07-19T09:44:45.750Z',
#   updated_at='2019-08-03T16:17:15.228Z'
# )
```

### Disable/Enable user

```python
api.user.disable(new_user.id)
api.user.enable(new_user.id)
```

### Invite user to team

```python
user = api.user.get_info_by_login('demo_user4')
team = api.team.get_info_by_name('max')
if api.user.get_team_role(user.id, team.id) is None:
    api.user.add_to_team(user.id, team.id, api.role.DefaultRole.ANNOTATOR)
print_user_teams(user.login)
# Teams of user 'demo_user4':
# [team_id=22] demo_user4                [role_id=1] admin
# [team_id=4] max                       [role_id=3] annotator
```

### List all team users with corresponding roles

```python
team = api.team.get_info_id(TEAM_ID)
members = api.user.get_team_members(team.id)
print(f"All members in team: '{team.name}'")
print(members)
# All members in team 'my_team'
# [
#   UserInfo(
#     id=4, 
#     login='max', 
#     name='max_k', 
#     email=None, 
#     logins=7, 
#     disabled=False,
#     last_login='2019-08-02T09:18:09.155Z',
#     created_at='2019-04-11T10:59:50.472Z',
#     updated_at='2019-08-05T08:42:20.463Z'
#   ),
#    UserInfo(
#      id=25, 
#      login='demo_user4',
#      name='', 
#      email=None,
#      logins=0, 
#      disabled=False,
#      last_login=None,
#      created_at='2019-07-19T09:44:45.750Z',
#      updated_at='2019-08-05T08:42:21.934Z'
#   ),
#    UserInfo(
#      id=29,
#      login='labeler_01',
#      name='',
#      email=None,
#      logins=0,
#      disabled=False,
#      last_login=None,
#      created_at='2019-07-20T15:12:51.898Z',
#      updated_at='2019-07-20T16:55:19.917Z'
#   ),
#    UserInfo(
#      id=30,
#      login='labeler_02',
#      name='',
#      email=None, 
#      logins=0, 
#      disabled=False,
#      last_login=None,
#      created_at='2019-07-20T15:12:52.448Z', 
#      updated_at='2019-07-20T15:12:52.448Z'
#   ),
#    UserInfo(
#      id=31, 
#      login='labeler_03',
#      name='',
#      email=None, 
#      logins=0, 
#      disabled=False,
#      last_login=None,
#      created_at='2019-07-20T15:12:52.779Z',
#      updated_at='2019-07-20T15:12:52.779Z'
#   )
# ]
 ```

### Change user role in team

```python
user = api.user.get_info_by_login('demo_user4')
team = api.team.get_info_by_name('max')
api.user.change_team_role(user.id, team.id, api.role.DefaultRole.VIEWER)
print_user_teams('demo_user4')
# Teams of user 'demo_user4':
# [team_id=22] demo_user4                [role_id=1] admin
# [team_id=4] max                       [role_id=4] viewer
```

### Remove user from team

```python
team = api.team.get_info_by_name('max')
user = api.user.get_info_by_login('demo_user4')
api.user.remove_from_team(user.id, team.id)
print_user_teams('demo_user4')
# Teams of user 'demo_user4':
# [team_id=22] demo_user4                [role_id=1] admin
```
