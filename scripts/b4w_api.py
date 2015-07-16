import os
import re
import json
B4W_PATH = ".."

# api_lib = [{
#     "module_name": "name",
#     "module_methods": [{
#         "method_name": "name",
#         "method_params": [{
#             "param_name": "name",
#             "param_type": "type",
#             "param_desc": "description"
#         }, ...
#         ],
#         "method_return": {
#             "return_type": "type",
#             "return_desc": "description"
#         },
#         "depricated": {
#             "is_depricated": true/false,
#             "desc" : "description"
#         }
#     }, ...
#     ],
#     "module_consts": [{
#         "const_name": "name",
#         "const_type": "type"
#     }, ...
#     ],
# }, ...
# ]

def get_b4w_api():

    path_to_src = os.path.join(B4W_PATH, "src")
    path_to_ext = os.path.join(path_to_src, "ext")
    os.path.normpath(path_to_ext)
    if not os.path.exists(path_to_ext):
        return None

    api_lib = []
    expr_const = re.compile("@const.*\{(.*)\}.*module:(.*)\.(.*)")
    expr_method = re.compile("@method.*module:(.*)\.(.*)")
    expr_param = re.compile("@param.* \{(.*)\} (.*?) (.*)")
    expr_returns = re.compile("@returns.* \{(.*)\} (.*)")
    expr_deprecated = re.compile("@deprecated *([^ ].*)")

    files = os.listdir(path_to_ext)
    for file in files:
        module_name = file.split(".")[0]

        api_lib.append({"module_name": module_name})
        file_src = open(os.path.join(path_to_ext, file))
        methods = []
        const = []
        for line in file_src.readlines():
            const_data = re.search(expr_const, line)
            if const_data:
                const.append({"const_name":const_data.group(3),
                              "const_type":const_data.group(1)})

            method_data = re.search(expr_method, line)
            if method_data:
                methods.append({"method_name":method_data.group(2)})
            param_data = re.search(expr_param, line)
            if param_data:
                if len(methods):
                    if "method_params" not in methods[-1]:
                        methods[-1]["method_params"] = []
                    methods[-1]["method_params"].append({"param_type": param_data.group(1),
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

        if len(methods)
            api_lib[-1]["module_methods"] = methods
        if len(const):
            api_lib[-1]["module_const"] = const
    return api_lib

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
