from .helper_dicts import SIDEBAR_SLUG_AND_MODEL, SIDEBAR_SLUG_AND_MODULE

def get_sidebar_which_have_perm(user_obj, sidebar_modules):
    sidebar = {}
    for module in sidebar_modules:
        perm = module.permission
        user_has_perm = user_obj.has_perm(perm)
        if user_has_perm:
            module_name = SIDEBAR_SLUG_AND_MODULE.get(module.slug)
            sidebar[module.slug] = module_name
    return sidebar

# def get_sidebar_which_have_perm(user_obj, model_permission_dict):
#     sidebar = {}
#     for slug, model in SIDEBAR_SLUG_AND_MODEL.items():
#         perm = model_permission_dict.get(model)
#         user_has_perm = user_obj.has_perm(perm)
#         if user_has_perm:
#             module_name = SIDEBAR_SLUG_AND_MODULE.get(slug)
#             sidebar[slug] = module_name
#     return sidebar
