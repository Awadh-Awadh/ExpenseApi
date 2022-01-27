from rest_framework import renderers
import json

"""
renderers help in customizing the response of data rendered by django into what you want it to look like.
For intance when creating a user and exists errors, you can create a prefix key 'errors' before the data.
Renders help in achieving this objective. To use renders we need to inherit from renderers.JSONRender and overide 
the render function
Charset should be specified.

"""

class AuthRender(renderers.JSONRenderer):
   """
    For renderes to work charset must be defined
   """
   charset = "utf-8"
   def render(self, data, accepted_media_type=None, renderer_context=None):
       response = ""
       if 'ErrorDetail' in data:
         response = json.dumps({"errors" : data})
       else:
         response = json.dumps({"data": data})
       return response