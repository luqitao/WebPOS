# coding=utf-8
__author__ = 'aaron'

import appName.api.glance as glance_api

global total_image_list
total_image_list = []

class Image():
    def list_images(self,user):
        image_list = self.list_all_image(user)
        global total_image_list
        total_image_list = []
        return image_list

    def list_all_image(self,user,parameter=None):
        global total_image_list
        if parameter is None:
            image_list = glance_api.list_image(user)
        else:
            image_list = glance_api.list_image(user,parameter)

        if  image_list[0] == 200:
            total_image_list.append(image_list[1])

            if 'next' in image_list[1]:
                parameter = image_list[1]['next']
                total_image_list.append(self.list_all_image(user,parameter))

        return total_image_list

    def list_all_image_names(self,user):
        image_list = self.list_images(user)
        new_image_list=[]
        dicttory = dict()
        if image_list is not None and len(image_list) >0:
            # new_image_list.append("200")
            	for img in image_list:
                	if type(img)==dict:
                    		new_image_list.append(img)

        dicttory['images']=[]
        total_image = []
        for images in new_image_list:
            	total_image = total_image+images['images']
        dicttory['images'].append(total_image)

        image_list = dicttory['images'][0]
        image_array = []
        for image_object in image_list:
            	if image_object['owner'] == user['projectid']:
                    	image = {}
                    	image['id'] = image_object['id']
                    	image['name'] = image_object['name']
                    	image_array.append(image)
        return image_array


    def delete_image(self, images_ids, user):
        response = glance_api.delete_image(user,**images_ids)
        if response == 204:
            return {"Success":"OK"}
        else:
            return {"Error":"delete failed"}

    def create_image(self, user,**image):
        response = glance_api.upload_image(user,**image)
        if response[0] == 204 or response[0] == 200:
            return {"Success":"OK"}
        else:
            return {"Error":"create failed"}

    def update_image(self, user, **image):
        response = glance_api.update_image(user,**image)
        if response[0] == 200:
            return {"Success":"OK"}
        else:
            return {"Error":"create failed"}