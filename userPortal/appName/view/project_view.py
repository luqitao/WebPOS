__author__ = 'aaron'

from appName.api import key_store as keystore_api
class Project():
    def list_project(self,user):
        code,project_list = keystore_api.list_project(user)
        if code == 200:
            return project_list

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


    def delete_project(self,user, project_id):
        code = keystore_api.delete_project(user,project_id)
        if code == 204:
            return {"Success":"OK"}
        else:
            return {"Error":"delete failed"}

    def create_project(self, user,**project):
        response = keystore_api.create_project(user,**project)
        if response[0] == 201:
            return {"Success":"OK"}
        else:
            return {"Error":"create Porject failed"}

    def update_project(self, user, **project):
        response = keystore_api.update_project(user,**project)
        if response[0] == 200:
            return {"Success":"OK"}
        else:
            return {"Error":"create failed"}

    def list_project_quota(self,user,admin_project_id,project_id):
        response_code,response_content = keystore_api.list_project_quota(user, admin_project_id,project_id)
        if response_code == 200:
            return response_content
        else:
            return {"Error":"list failed"}



    def update_project_quota(self,user,project_id):
        response_code,response_content = keystore_api.list_project_quota(user, project_id)
        if response_code == 200:
            return response_content
        else:
            return {"Error":"create failed"}