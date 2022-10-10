import os
from dotenv import load_dotenv
import supervisely as sly

# for debug
load_dotenv(os.path.expanduser("~/supervisely.env"))
load_dotenv("local.env")
api = sly.Api()

USER_ID = int(os.environ["CONTEXT_USERID"])
TEAM_ID = int(os.environ["CONTEXT_TEAMID"])
USER_LOGIN = os.environ["CONTEXT_USERLOGIN"]

# list available roles on Supervisely instance
roles = api.role.get_list()
print(f"Roles: {roles}")

# list all registered users
users = api.user.get_list()
for user in users:
    print("Id: {:<5} Login: {:<25s} logins_count: {:<5}".format(user.id, user.login, user.logins))


# get UserInfo about yourself
my_info = api.user.get_my_info()
print("my login:", my_info.login)
print("my ID:", my_info.id)


# get UserInfo by ID
user_info = api.user.get_info_by_id(USER_ID)
print(f"UserInfo by ID: {user_info}")

# get UserInfo by login
user_info = api.user.get_info_by_login(USER_LOGIN)
print(f"UserInfo by name: {user_info}")

# list all user teams with corresponding roles
def print_user_teams(login):
    user = api.user.get_info_by_login(login)
    user_teams = api.user.get_teams(user.id)
    print("\nTeams of user {!r}:".format(login))
    for team in user_teams:
        print("[team_id={}] {:<25s} [role_id={}] {}".format(team.id, team.name, team.role_id, team.role))

print_user_teams(USER_LOGIN)

# create new user
new_user = api.user.get_info_by_login('demo_user_451')
if new_user is None:
    new_user = api.user.create(login='demo_user_451', password='123abc', is_restricted=False)
print(f"New UserInfo: {new_user}")

# update UserInfo
new_password = 'abc123'
new_name = 'Bob'
user_info = api.user.update(user_info.id, password=new_password, name=new_name)
print(f"Updated UserInfo: {new_user}")


# disable/enable user
api.user.disable(user_info.id)
api.user.enable(user_info.id)

# invite user to team
user = api.user.get_info_by_login('demo_user_451')
team = api.team.get_info_by_id(TEAM_ID)
if api.user.get_team_role(user.id, team.id) is None:
    api.user.add_to_team(user.id, team.id, api.role.DefaultRole.ANNOTATOR) 
    
# list all team users with corresponding roles
team = api.team.get_info_by_id(TEAM_ID)
members = api.user.get_team_members(team.id)
print(f"Team members: {members}")

# change user role in team
user = api.user.get_info_by_login('demo_user_451')
team = api.team.get_info_by_id(TEAM_ID)
api.user.change_team_role(user.id, team.id, api.role.DefaultRole.VIEWER)
print_user_teams('demo_user_451')

# remove user from team
team = api.team.get_info_by_id(TEAM_ID)
user = api.user.get_info_by_login('demo_user_451')
api.user.remove_from_team(user.id, team.id)
print_user_teams('demo_user_451')
