from django.db import models

class SidebarModule(models.Model):
    #     slug """ user-management """
    #     module """ User Management """
    #     model_name """ user """
    #     permission = app_label.view_model_name """ users.view_user """
    slug = models.CharField(max_length=150, blank=True)
    module_name = models.CharField(max_length=150, blank=True)
    model_name = models.CharField(max_length=150, blank=True)
    permission = models.CharField(max_length=255, blank=True)



# Permission Management": [
#         {
#           "add": 1
#         },
#         {
#           "change": 2
#         },
#         {
#           "delete": 3
#         },
#         {
#           "view": 4
#         }
#       ]
#     }



# "permissions": {
#         "Role Management": [
#       {
#         "add": {'id': 5, 'has_permission': True}
#       },
#       {
#         "change": 6
#       },
#       {
#         "delete": 7
#       },
#       {
#         "view": 8
#       }
#     ],
#     "Permission Management": [
#       {
#         "add": 1
#       },
#       {
#         "change": 2
#       },
#       {
#         "delete": 3
#       },
#       {
#         "view": 4
#       }
#     ],
#     "User Management": [
#       {
#         "add": 13
#       },
#       {
#         "change": 14
#       },
#       {
#         "delete": 15
#       },
#       {
#         "view": 16
#       }
#     ]
#   }
#     },


[{""}]