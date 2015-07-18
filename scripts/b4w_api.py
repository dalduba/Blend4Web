import os
import re
import json

B4W_PATH = ".."

# api_lib = {
#     "callbacks": {
#         "callback_name": {
#             "callback_params": [{
#                 "param_name": "name",
#                 "param_type": "type",
#                 "param_desc": "description"
#             }, ...
#             ]
#         }
#     },
#     "typedefs": {"new_name": "old_name"},
#     "types": ["type_name", ...],
#     "modules": [{
#         "module_name": "name",
#         "module_methods": [{
#             "method_name": "name",
#             "method_params": [{
#                 "param_name": "name",
#                 "param_type": "type",
#                 "param_desc": "description"
#             }, ...
#             ],
#             "method_return": {
#                 "return_type": "type",
#                 "return_desc": "description"
#             },
#             "depricated": {
#                 "is_depricated": true/false,
#                 "desc" : "description"
#             }
#         }, ...
#         ],
#         "module_consts": [{
#             "const_name": "name",
#             "const_type": "type"
#         }, ...
#         ],
#     }, ...
#     ]
# }

def get_b4w_api():

    path_to_src = os.path.join(B4W_PATH, "src")
    path_to_ext = os.path.join(path_to_src, "ext")
    os.path.normpath(path_to_ext)
    if not os.path.exists(path_to_ext):
        return None

    api_lib = {}
    api_lib["modules"] = []

    expr_begin_comment = re.compile("\/\*\*")
    expr_end_comment = re.compile("\*\/")
    expr_typedef       = re.compile("@typedef (.*)")
    expr_type          = re.compile("@type \{(.*)\}")
    expr_callback      = re.compile("@callback (.*)")
    expr_const         = re.compile("@const.*\{(.*)\}.*module:(.*)\.(.*)")
    expr_method        = re.compile("@method.*module:(.*)\.(.*)")
    expr_param         = re.compile("@param.* \{(.*)\} (.*?) (.*)")
    expr_returns       = re.compile("@returns.* \{(.*)\} (.*)")
    expr_deprecated    = re.compile("@deprecated *([^ ].*)")

    files = os.listdir(path_to_ext)

    typedefs = {}
    callbacks = {}
    types = set()

    for file in files:
        module_name = file.split(".")[0]

        api_lib["modules"].append({"module_name": module_name})
        file_src = open(os.path.join(path_to_ext, file))
        methods = []
        const = []
        in_comment = False
        new_type_name = ""
        cur_callback = ""
        for line in file_src.readlines():
            begin_comment_data = re.search(expr_begin_comment, line)
            if begin_comment_data:
                in_comment = True

            end_comment_data = re.search(expr_end_comment, line)
            if end_comment_data:
                in_comment = False

            if in_comment:
                typedef_name_data = re.search(expr_typedef, line)
                if typedef_name_data:
                    new_type_name = typedef_name_data.group(1);

                typedef_type_data = re.search(expr_type, line)
                if typedef_type_data and new_type_name:
                    typedefs[new_type_name] = typedef_type_data.group(1)

                callback_name_data = re.search(expr_callback, line)
                if callback_name_data:
                    in_callback = True
                    cur_callback = callback_name_data.group(1)
                    callbacks[cur_callback] = {}

                const_data = re.search(expr_const, line)
                if const_data:
                    const.append({"const_name":const_data.group(3),
                                  "const_type":const_data.group(1)})

                method_data = re.search(expr_method, line)
                if method_data:
                    in_method = True
                    methods.append({"method_name":method_data.group(2)})

                param_data = re.search(expr_param, line)
                if param_data:
                    param_type = check_aliases(param_data.group(1), typedefs)
                    types.add(param_type)
                    if in_method and len(methods):
                        if "method_params" not in methods[-1]:
                            methods[-1]["method_params"] = []
                        methods[-1]["method_params"].append(
                                {"param_type": param_type,
                                 "param_name": param_data.group(2),
                                 "param_desc": param_data.group(3)})
                    elif in_callback and cur_callback in callbacks:
                        if "callback_params" not in callbacks[cur_callback]:
                            callbacks[cur_callback]["callback_params"] = []
                        callbacks[cur_callback]["callback_params"].append(
                                {"param_type": param_type,
                                 "param_name": param_data.group(2),
                                 "param_desc": param_data.group(3)})

                return_data = re.search(expr_returns, line)
                if return_data:
                    if len(methods):
                        methods[-1]["method_return"] = {"return_type": return_data.group(1),
                                                        "return_desc": return_data.group(2)}

                depricated_data = re.search(expr_deprecated, line)
                if depricated_data:
                    if len(methods):
                        methods[-1]["depricated"] = {"is_depricated": True,
                                                     "desc": depricated_data.group(1)}
            else:
                in_callback = False
                in_method = False
                new_type_name = ""
                cur_callback = ""


        if len(methods):
            api_lib["modules"][-1]["module_methods"] = methods
        if len(const):
            api_lib["modules"][-1]["module_const"] = const
    api_lib["types"] = list(types)
    api_lib["callbacks"] = callbacks
    api_lib["aliases"] = typedefs

    return api_lib

def check_aliases(name, typedefs):
    if name in typedefs:
        return typedefs[name]
    return name

def dump(data):
    path_to_b4w_addon = os.path.join(B4W_PATH, "blender_scripts/addons/blend4web")
    os.path.normpath(path_to_b4w_addon)

    if not os.path.exists(path_to_b4w_addon):
        return None

    path_to_b4w_api_json = os.path.join(path_to_b4w_addon, "b4w_api.json")
    file = open(path_to_b4w_api_json, "w")

    file.write(json.dumps(data))

if __name__ == '__main__':
    data = get_b4w_api()
    dump(data)
