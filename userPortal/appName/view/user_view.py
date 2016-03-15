__author__ = 'aaron'
from appName.api import key_store as keystore_api
class User():
    def list_user(self,user):
        user_list = keystore_api.list_user(user)
        return user_list

    def list_project_names(self,user):
        project_list = keystore_api.list_project(user)
        if project_list[0] == 200:
            project_dir = project_list[1]
            project_list = project_dir['projects']
            project_array = []
            for project_object in project_list:
                    project = {}
                    project['id'] = project_object['id']
                    project['name'] = project_object['name']
                    project_array.append(project)
            return project_array
        else:
            return {"Error":"list_project_name failed"}


    def list_user_names(self,user):
        user_list = keystore_api.list_user(user)
        if user_list[0] == 200:
            user_json = user_list[1]
            user_list = user_json['users']
            user_array = []
            for user_object in user_list:
                    user = {}
                    user['id'] = user_object['id']
                    user['name'] = user_object['name']
                    user_array.append(user)
            return user_array
        else:
            return {"Error":"list_user_name failed"}


    def list_user_roles(self,user):
        role_list = keystore_api.list_role(user)
        if role_list[0] == 200:
            role_dir = role_list[1]
            role_list = role_dir['roles']
            role_array = []
            for role_object in role_list:
                    role = {}
                    role['id'] = role_object['id']
                    role['name'] = role_object['name']
                    role_array.append(role)
            return role_array
        else:
            return {"Error":"list_project_name failed"}

    def delete_user(self,user, user_id):
        response = keystore_api.delete_user(user,user_id)
        if response == 204:
            return {"Success":"OK"}
        else:
            return {"Error":"delete failed"}

    def create_user(self, userinfo,**user):
        response = keystore_api.create_user(userinfo,**user)
        if response[0] == 204:
            return {"Success":"OK"}
        else:
            return {"Error":"create User failed"}

    def update_user(self, userinfo,**user):
        response = keystore_api.update_tenant(**user)
        if response[0] == 200:
            return {"Success":"OK"}
        else:
            return {"Error":"create failed"}