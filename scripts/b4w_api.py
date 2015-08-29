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
#     "b4w_api": [{
#         "name": "name",
#         "methods": [{
#             "name": "name",
#             "inputs": [{
#                 "name": "name",
#                 "type": "type",
#                 "desc": "description"
#             }, ...
#             ],
#             "outputs": [{
#                 "type": "type",
#                 "desc": "description"
#             }],
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

def Vec3_sock_desc(name, connectible = 1):
    return {"name":name, "type": "Vec3", "connectible": connectible}
def String_sock_desc(name, connectible = 0):
    return {"name":name, "type": "String", "connectible": connectible}
def Bool_sock_desc(name, connectible = 0):
    return {"name":name, "type": "Bool", "connectible": connectible}
def Object3D_sock_desc(name):
    return {"name":name, "type": "Object3D", "connectible": 1}
def Number_sock_desc(name, connectible = 0):
    return {"name":name, "type": "Number", "connectible": connectible}
def Axis_sock_desc(name):
    return {"name":name, "type": "Axis", "connectible": 0}
def Date_sock_desc(name, connectible = 1):
    return {"name":name, "type": "Date", "connectible": connectible}
def Int_sock_desc(name, connectible = 1):
    return {"name":name, "type": "Int", "connectible": connectible}
def Array_sock_desc(name, connectible = 1):
    return {"name":name, "type": "Array", "connectible": connectible}
def Data_sock_desc(name, connectible = 1):
    return {"name":name, "type": "_Data", "connectible": connectible}
def Sensor_sock_desc(name, connectible = 1):
    return {"name":name, "type": "sensor", "connectible": connectible}


def Sensor_standard_output_desc(payload = True):
    r = [{"name":"sensor", "type":"Sensor"}, {"name":"value"}]
    if payload:
       r.append({"name":"payload"})
    return r

operators = [
{"name":"binary", "methods":[
    {"name": "+",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1)],
     "outputs":[Number_sock_desc("result", 1)],
    },
    {"name": "-",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1)],
     "outputs":[Number_sock_desc("result", 1)]
    },
    {"name": "*",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1)],
     "outputs":[Number_sock_desc("result", 1)]
    },
    {"name": "/",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1)],
     "outputs":[Number_sock_desc("result", 1)]
    },
    {"name": "%",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1)],
     "outputs":[Number_sock_desc("result", 1)]
    },
    {"name": "<<",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1)],
     "outputs":[Number_sock_desc("result", 1)]
    },
    {"name": ">>",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1)],
     "outputs":[Number_sock_desc("result", 1)]
    },
    {"name": ">>>",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1)],
     "outputs":[Number_sock_desc("result", 1)]
    },
    ]
},
{"name":"relational", "methods":[
    {"name": "!==",
     "inputs":[Data_sock_desc("op1", 1),
               Data_sock_desc("op2", 1)],
     "outputs":[Bool_sock_desc("result", 1)],
    },
    {"name": "===",
     "inputs":[Data_sock_desc("op1", 1),
               Data_sock_desc("op2", 1)],
     "outputs":[Bool_sock_desc("result", 1)],
    },
    {"name": "!=",
     "inputs":[Data_sock_desc("op1", 1),
               Data_sock_desc("op2", 1)],
     "outputs":[Bool_sock_desc("result", 1)],
    },
    {"name": "==",
     "inputs":[Data_sock_desc("op1", 1),
               Data_sock_desc("op2", 1)],
     "outputs":[Bool_sock_desc("result", 1)],
    },
    {"name": "instanceof",
     "inputs":[Data_sock_desc("op1", 1),
               Data_sock_desc("op2", 1)],
     "outputs":[Bool_sock_desc("result", 1)],
    },
    {"name": ">=",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1)],
     "outputs":[Bool_sock_desc("result", 1)],
    },
    {"name": "<=",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1)],
     "outputs":[Bool_sock_desc("result", 1)],
    },
    {"name": ">",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1)],
     "outputs":[Bool_sock_desc("result", 1)],
    },
    {"name": "<",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1)],
     "outputs":[Bool_sock_desc("result", 1)],
    },
    ]
},
{"name":"logic", "methods":[
    {"name": "OR",
     "inputs":[Bool_sock_desc("op1", 1),
               Bool_sock_desc("op2", 1)],
     "outputs":[Bool_sock_desc("result", 1)],
    },
    {"name": "AND",
     "inputs":[Bool_sock_desc("op1", 1),
               Bool_sock_desc("op2", 1)],
     "outputs":[Bool_sock_desc("result", 1)],
    },
    {"name": "NOT",
     "inputs":[Bool_sock_desc("op", 1)],
     "outputs":[Bool_sock_desc("result", 1)],
    },
    ]
},
{"name":"unary", "methods":[
    {"name": "typeof",
     "inputs":[Data_sock_desc("op1", 1),],
     "outputs":[String_sock_desc("result", 1)],
    },
    {"name": "op--",
     "inputs":[Number_sock_desc("op", 1),],
     "outputs":[Number_sock_desc("result", 1),],
    },
    {"name": "--op",
     "inputs":[Number_sock_desc("op", 1),],
     "outputs":[Number_sock_desc("result", 1),],
    },
    {"name": "op++",
     "inputs":[Number_sock_desc("op", 1),],
     "outputs":[Number_sock_desc("result", 1),],
    },
    {"name": "++op",
     "inputs":[Number_sock_desc("op", 1),],
     "outputs":[Number_sock_desc("result", 1),],
    },
    ]
},
{"name":"sensor", "methods":[
    {"name": "OR",
     "inputs":[Sensor_sock_desc("sensor1", 1),
               Sensor_sock_desc("sensor2", 1)],
     "outputs":[Sensor_sock_desc("result", 1)],
    },
    {"name": "AND",
     "inputs":[Sensor_sock_desc("sensor1", 1),
               Sensor_sock_desc("sensor2", 1)],
     "outputs":[Sensor_sock_desc("result", 1)],
    },
    {"name": "NOT",
     "inputs":[Sensor_sock_desc("sensor", 1)],
     "outputs":[Sensor_sock_desc("result", 1)],
    },
    ]
}
]

sensors = [
{"name":"controls", "methods":[
    {"name": "keyboard",
     "inputs":[{"socket_name":"key", "socket_type": "Key", "connectible": 0},],
     "outputs":[]},

    {"name": "mouse_click",
     "inputs":[],
     "outputs":[]},

    {"name": "mouse_move",
     "inputs":[Axis_sock_desc("axis")],
     "outputs":[]},

    {"name": "mouse_wheel",
     "inputs":[],
     "outputs":[]},

    {"name": "touch_move",
     "inputs":[Axis_sock_desc("axis")],
     "outputs":[]},

    {"name": "touch_zoom",
     "inputs":[],
     "outputs":[]},
]},

{"name":"collision", "methods":[
     {"name": "collision",
     "inputs":[Object3D_sock_desc("obj"),
               String_sock_desc("id"),
               Bool_sock_desc("calc_pos_norm"),],
     "outputs":[]},

    {"name": "collision_impulse",
     "inputs":[Object3D_sock_desc("obj"),],
     "outputs":[]},

    {"name": "ray",
     "inputs":[Object3D_sock_desc("obj"),
               Vec3_sock_desc("from"),
               Vec3_sock_desc("to"),
               String_sock_desc("id"),
               Bool_sock_desc("is_binary_value"),
               Bool_sock_desc("calc_pos_norm"),
               Bool_sock_desc("ign_src_rot")],
     "outputs":[]},

    {"name": "selection",
     "inputs":[Object3D_sock_desc("obj"),
               Bool_sock_desc("auto_release"),],
     "outputs":[]},
]},

{"name":"time", "methods":[
    {"name": "timer",
     "inputs":[Number_sock_desc("period"),
               Bool_sock_desc("do_repeat"),],
     "outputs":[]},

    {"name": "elapsed",
     "inputs":[],
     "outputs":[]},

    {"name": "timeline",
     "inputs":[],
     "outputs":[]},
]},

{"name":"motion", "methods":[
     {"name": "motion",
     "inputs":[Object3D_sock_desc("obj"),
               Number_sock_desc("threshold"),
               Number_sock_desc("rotation_threshold"),],
     "outputs":[]},

    {"name": "vertical_velocity",
     "inputs":[Object3D_sock_desc("obj"),
               Number_sock_desc("threshold"),],
     "outputs":[]},

    {"name": "gyro_delta",
     "inputs":[],
     "outputs":[]},

    {"name": "gyro_angles",
     "inputs":[Number_sock_desc("threshold")],
     "outputs":[]},
]},
]

for m in sensors:
    for s in m['methods']:
        for out in Sensor_standard_output_desc().__reversed__():
            s['outputs'].insert(0, out)

#---------

js_api_modules=[
     {"name": "String", "methods":[
        {"name": "length",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[Int_sock_desc("Number", True)]},

        {"name": "charAt",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "charCodeAt",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[Int_sock_desc("Code", True)]},

        {"name": "concat",
         "inputs":[String_sock_desc("Str1", True), String_sock_desc("Str2", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "fromCharCode",
         "inputs":[String_sock_desc("Str", True), Int_sock_desc("Code", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "indexOf",
         "inputs":[String_sock_desc("Str1", True), String_sock_desc("Str2", True)],
         "outputs":[Int_sock_desc("Index", True)]},

        {"name": "lastIndexOf",
         "inputs":[String_sock_desc("Str1", True), String_sock_desc("Str2", True)],
         "outputs":[Int_sock_desc("Index", True)]},

        {"name": "localeCompare",
         "inputs":[String_sock_desc("Str1", True), String_sock_desc("Str2", True)],
         "outputs":[Int_sock_desc("Ret", True)]},

        {"name": "match",
         "inputs":[String_sock_desc("Str1", True), String_sock_desc("Str2", True)],
         "outputs":[Array_sock_desc("Ret", True)]},

        {"name": "replace",
         "inputs":[String_sock_desc("Str", True), String_sock_desc("Search", True), String_sock_desc("Replace", True)],
         "outputs":[String_sock_desc("Ret", True)]},

        {"name": "search",
         "inputs":[String_sock_desc("Str1", True), String_sock_desc("Str2", True)],
         "outputs":[Int_sock_desc("Ret", True)]},

        {"name": "slice",
         "inputs":[String_sock_desc("Str", True), Int_sock_desc("Start", True),Int_sock_desc("End", True)],
         "outputs":[Int_sock_desc("Ret", True)]},

        {"name": "split",
         "inputs":[String_sock_desc("Str", True), String_sock_desc("Sep", True)],
         "outputs":[Array_sock_desc("Ret", True)]},

        {"name": "substring",
         "inputs":[String_sock_desc("Str", True), Int_sock_desc("Start", True),Int_sock_desc("End", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "toLocaleLowerCase",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "toLocaleUpperCase",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "toLowerCase",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "toString",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "toUpperCase",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "trim",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "valueOf",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[Int_sock_desc("Val", True)]},

     ]},

     {"name": "Number", "methods":[
        {"name": "MAX_VALUE",
         "outputs":[Int_sock_desc("Val", True)]},

        {"name": "MIN_VALUE",
         "outputs":[Int_sock_desc("Val", True)]},

        {"name": "NEGATIVE_INFINITY",
         "outputs":[String_sock_desc("Val", True)]},

        {"name": "NaN",
         "outputs":[String_sock_desc("Val", True)]},

        {"name": "POSITIVE_INFINITY",
         "outputs":[String_sock_desc("Val", True)]},

        {"name": "toExponential",
         "inputs":[Number_sock_desc("Num", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "toFixed",
         "inputs":[Number_sock_desc("Num", True), Int_sock_desc("Val", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "toPrecision",
         "inputs":[Number_sock_desc("Num", True), Int_sock_desc("Val", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "toString",
         "inputs":[Number_sock_desc("Num", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "valueOf",
         "inputs":[Number_sock_desc("Num", True)],
         "outputs":[Int_sock_desc("Val", True)]},

     ]},

    {"name": "Boolean", "methods":[
        {"name": "toString",
         "inputs":[Bool_sock_desc("Bool", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "valueOf",
         "inputs":[Bool_sock_desc("Bool", True)],
         "outputs":[Bool_sock_desc("Str", True)]},
    ]},

    {"name": "Location", "methods":[

        {"name": "hash",
         "outputs":[String_sock_desc("hash", True)]},

        {"name": "host",
         "outputs":[String_sock_desc("host", True)]},

        {"name": "hostname",
         "outputs":[String_sock_desc("hostname", True)]},

        {"name": "href",
         "outputs":[String_sock_desc("href", True)]},

        {"name": "origin",
         "outputs":[String_sock_desc("origin", True)]},

        {"name": "pathname",
         "outputs":[String_sock_desc("pathname", True)]},

        {"name": "port",
         "outputs":[String_sock_desc("port", True)]},

        {"name": "protocol",
         "outputs":[String_sock_desc("protocol", True)]},

        {"name": "search",
         "outputs":[String_sock_desc("search", True)]},

        {"name": "assign",
         "inputs":[String_sock_desc("URL", True)],
         "outputs":[]},

        {"name": "reload",
         "inputs":[],
         "outputs":[]},

        {"name": "replace",
         "inputs":[String_sock_desc("URL", True)],
         "outputs":[]},

    ]},

    {"name": "Navigator", "methods":[
        {"name": "appCodeName",
         "outputs":[String_sock_desc("appCodeName", True)]},

        {"name": "appName",
         "outputs":[String_sock_desc("appName", True)]},

        {"name": "appVersion",
         "outputs":[String_sock_desc("appVersion", True)]},

        {"name": "cookieEnabled",
         "outputs":[Bool_sock_desc("cookieEnabled", True)]},

        {"name": "geolocation",
         "outputs":[Data_sock_desc("geolocation", True)]},

        {"name": "language",
         "outputs":[String_sock_desc("language", True)]},

        {"name": "onLine",
         "outputs":[Bool_sock_desc("onLine", True)]},

        {"name": "platform",
         "outputs":[String_sock_desc("platform", True)]},

        {"name": "product",
         "outputs":[String_sock_desc("product", True)]},

        {"name": "userAgent",
         "outputs":[String_sock_desc("userAgent", True)]},

        {"name": "javaEnabled",
         "outputs":[Bool_sock_desc("javaEnabled", True)]},
    ]},

    {"name": "Global", "methods":[
        {"name": "Infinity",
         "inputs":[],
         "outputs":[Data_sock_desc("Infinity", True)]},

        {"name": "NaN",
         "inputs":[],
         "outputs":[Data_sock_desc("NaN", True)]},

        {"name": "undefined",
         "inputs":[],
         "outputs":[Data_sock_desc("undefined", True)]},

        {"name": "decodeURI",
         "inputs":[String_sock_desc("Uri", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "decodeURIComponent",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[String_sock_desc("Uri", True)]},

        {"name": "encodeURI",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[String_sock_desc("Uri", True)]},

        {"name": "encodeURIComponent",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[String_sock_desc("Uri", True)]},

        {"name": "eval",
         "inputs":[String_sock_desc("Str", True)],
         "outputs":[Data_sock_desc("Ret", True)]},

        {"name": "isFinite",
         "inputs":[Data_sock_desc("In", True)],
         "outputs":[Bool_sock_desc("Ret", True)]},

        {"name": "isNaN",
         "inputs":[Data_sock_desc("In", True)],
         "outputs":[Bool_sock_desc("Ret", True)]},

        {"name": "Number",
         "inputs":[Data_sock_desc("In", True)],
         "outputs":[Number_sock_desc("Ret", True)]},

        {"name": "parseFloat",
         "inputs":[String_sock_desc("In", True)],
         "outputs":[Number_sock_desc("Ret", True)]},

        {"name": "parseInt",
         "inputs":[String_sock_desc("In", True)],
         "outputs":[Int_sock_desc("Ret", True)]},

        {"name": "String",
         "inputs":[Data_sock_desc("In", True)],
         "outputs":[String_sock_desc("Ret", True)]},
    ]},

    {"name": "RegExp", "methods":[
        {"name": "global",
         "inputs":[String_sock_desc("RegExp", True)],
         "outputs":[Bool_sock_desc("Ret", True)]},

        {"name": "ignoreCase",
         "inputs":[String_sock_desc("RegExp", True)],
         "outputs":[Bool_sock_desc("Ret", True)]},

        {"name": "lastIndex",
         "inputs":[String_sock_desc("RegExp", True)],
         "outputs":[Int_sock_desc("Index", True)]},

        {"name": "multiline",
         "inputs":[String_sock_desc("RegExp", True)],
         "outputs":[Bool_sock_desc("Ret", True)]},

        {"name": "source",
         "inputs":[String_sock_desc("RegExp", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "exec",
         "inputs":[String_sock_desc("RegExp", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "test",
         "inputs":[String_sock_desc("RegExp", True)],
         "outputs":[Bool_sock_desc("Ret", True)]},

        {"name": "toString",
         "inputs":[String_sock_desc("RegExp", True)],
         "outputs":[String_sock_desc("Str", True)]},
    ]},

    {"name": "Array", "methods":[
        {"name": "length",
         "inputs":[Array_sock_desc("Array", True)],
         "outputs":[Int_sock_desc("Length", True)]},

        {"name": "concat",
         "inputs":[Array_sock_desc("Array1", True), Array_sock_desc("Array2", True)],
         "outputs":[Array_sock_desc("Array", True)]},

        {"name": "indexOf",
         "inputs":[Array_sock_desc("Array1", True), Array_sock_desc("Array2", True)],
         "outputs":[Int_sock_desc("Index", True)]},

        {"name": "join",
         "inputs":[Array_sock_desc("Array1", True), Array_sock_desc("Array2", True)],
         "outputs":[Array_sock_desc("Array", True)]},

        {"name": "lastIndexOf",
         "inputs":[Array_sock_desc("Array1", True), Array_sock_desc("Array2", True)],
         "outputs":[Int_sock_desc("Index", True)]},

        {"name": "pop",
         "inputs":[Array_sock_desc("Array1", True)],
         "outputs":[Data_sock_desc("Elem", True)]},

        {"name": "push",
         "inputs":[Array_sock_desc("Array1", True), Data_sock_desc("Elem", True)],
         "outputs":[Int_sock_desc("Length", True)]},

        {"name": "reverse",
         "inputs":[Array_sock_desc("Array", True)],
         "outputs":[]},

        {"name": "shift",
         "inputs":[Array_sock_desc("Array", True)],
         "outputs":[Data_sock_desc("Elem", True)]},

        {"name": "slice",
         "inputs":[Array_sock_desc("Array", True), Int_sock_desc("Start", True), Int_sock_desc("End", True)],
         "outputs":[Array_sock_desc("Array", True)]},

        {"name": "sort",
         "inputs":[Array_sock_desc("Array", True)],
         "outputs":[]},

        {"name": "toString",
         "inputs":[Array_sock_desc("Array", True)],
         "outputs":[String_sock_desc("Str", True)]},

        {"name": "unshift",
         "inputs":[Array_sock_desc("Array", True), Data_sock_desc("Elem", True)],
         "outputs":[Int_sock_desc("Length", True)]},

        {"name": "valueOf",
         "inputs":[Array_sock_desc("Array", True)],
         "outputs":[Int_sock_desc("Val", True)]},
    ]},
    {"name": "Math", "methods":[

        {"name": "E",
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "LN2",
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "LN10",
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "LOG2E",
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "LOG10E",
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "PI",
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "SQRT1_2",
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "SQRT2",
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "abs",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "acos",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "asin",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "atan",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "atan2",
         "inputs":[Number_sock_desc("y", True), Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "ceil",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "cos",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "exp",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "flor",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "log",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "pow",
         "inputs":[Number_sock_desc("x", True), Number_sock_desc("y", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "round",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "sin",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "sqrt",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "tan",
         "inputs":[Number_sock_desc("x", True)],
         "outputs":[Number_sock_desc("Number", True)]},

        {"name": "random",
         "inputs":[],
         "outputs":[Number_sock_desc("Number", True)]},

# TODO make dynamic inputs for min/max
         {"name": "min",
         "inputs":[Number_sock_desc("x", True), Number_sock_desc("y", True)],
         "outputs":[Number_sock_desc("Number", True)]},

         {"name": "max",
         "inputs":[Number_sock_desc("x", True), Number_sock_desc("y", True)],
         "outputs":[Number_sock_desc("Number", True)]},
    ]

    },
    {"name": "Date", "methods":[
        {"name": "Date",
         "inputs":[],
         "outputs":[Date_sock_desc("Date", True)]},

        {"name": "getDate",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Day", True)]},

        {"name": "getDay",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Day", True)]},

        {"name": "getFullYear",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Year", True)]},

        {"name": "getHoursr",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Hours", True)]},

        {"name": "getMilliseconds",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("msec", True)]},

        {"name": "getMinutes",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("minutes", True)]},

        {"name": "getMonth",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Month", True)]},

        {"name": "getSeconds",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Seconds", True)]},

        {"name": "getTime",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("msec", True)]},

        {"name": "getTimezoneOffset",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Diff", True)]},

        {"name": "getUTCDate",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Day", True)]},

        {"name": "getUTCDay",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Day", True)]},

        {"name": "getUTCFullYear",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Year", True)]},

        {"name": "getUTCHours",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Hours", True)]},

        {"name": "getUTCMilliseconds",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("msec", True)]},

        {"name": "getUTCMinutes",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Minutes", True)]},

        {"name": "getUTCMonth",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Month", True)]},

        {"name": "getUTCSeconds",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("sec", True)]},

        {"name": "parse",
         "inputs":[Date_sock_desc("Date", True), String_sock_desc("DateString", True)],
         "outputs":[Date_sock_desc("Date", True)]},

        {"name": "setDate",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("Day", True)],
         "outputs":[]},

        {"name": "setFullYear",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("Year", True)],
         "outputs":[]},

        {"name": "setHours",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("Hours", True)],
         "outputs":[]},

        {"name": "setMilliseconds",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("msec", True)],
         "outputs":[]},

        {"name": "setMinutes",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("minutes", True)],
         "outputs":[]},

        {"name": "setMonth",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("Month", True)],
         "outputs":[]},

        {"name": "setSeconds",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("Sec", True)],
         "outputs":[]},

        {"name": "setTime",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("msec", True)],
         "outputs":[]},

        {"name": "setUTCDate",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("Day", True)],
         "outputs":[]},

        {"name": "setUTCFullYear",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("Year", True)],
         "outputs":[]},

        {"name": "setUTCHours",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("Hours", True)],
         "outputs":[]},

        {"name": "setUTCMilliseconds",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("mSec", True)],
         "outputs":[]},

        {"name": "setUTCMinutes",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("Minutes", True)],
         "outputs":[]},

        {"name": "setUTCMonth",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("Month", True)],
         "outputs":[]},

        {"name": "setUTCSeconds",
         "inputs":[Date_sock_desc("Date", True), Int_sock_desc("Sec", True)],
         "outputs":[]},

        {"name": "toDateString",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[String_sock_desc("String", True)]},

        {"name": "toISOString",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[String_sock_desc("String", True)]},

        {"name": "toJSON",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[String_sock_desc("String", True)]},

        {"name": "toLocaleDateString",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[String_sock_desc("String", True)]},

        {"name": "toLocaleTimeString",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[String_sock_desc("String", True)]},

        {"name": "toLocaleString",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[String_sock_desc("String", True)]},

        {"name": "toString",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[String_sock_desc("String", True)]},

        {"name": "toTimeString",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[String_sock_desc("String", True)]},

        {"name": "toUTCString",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[String_sock_desc("String", True)]},

        {"name": "UTC",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("mSec", True)]},

        {"name": "valueOf",
         "inputs":[Date_sock_desc("Date", True)],
         "outputs":[Int_sock_desc("Value", True)]},
    ]}
]

#---------
import copy
def add_all_module(api_lib, api_name):
    modules =  api_lib[api_name]
    methods = []

    for module in modules:
        if "methods" in module:
            for meth in module["methods"]:
                copy_meth = copy.deepcopy(meth)
                copy_meth["name"] = module['name']+"."+copy_meth["name"]
                methods.append(copy_meth)

    modules.append({"name": "all", "methods": methods})
def get_b4w_api():

    path_to_src = os.path.join(B4W_PATH, "src")
    path_to_ext = os.path.join(path_to_src, "ext")
    os.path.normpath(path_to_ext)
    if not os.path.exists(path_to_ext):
        return None

    api_lib = {}
    api_lib["b4w_api"] = []

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
    types = set()
    callbacks = []
    callbacks_dict = {}
    for file in files:
        module_name = file.split(".")[0]

        api_lib["b4w_api"].append({"name": module_name})
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
                    callbacks.append({"name":cur_callback})

                const_data = re.search(expr_const, line)
                if const_data:
                    const.append({"const_name":const_data.group(3),
                                  "const_type":const_data.group(1)})

                method_data = re.search(expr_method, line)
                if method_data:
                    in_method = True
                    methods.append({"name":method_data.group(2)})

                param_data = re.search(expr_param, line)
                if param_data:
                    param_type = check_aliases(param_data.group(1), typedefs)
                    types.add(param_type)
                    if in_method and len(methods):
                        if "inputs" not in methods[-1]:
                            methods[-1]["inputs"] = []
                        methods[-1]["inputs"].append(
                                {"type": param_type,
                                 "name": param_data.group(2),
                                 "desc": param_data.group(3)})
                    elif in_callback and cur_callback not in callbacks_dict:
                        if "outputs" not in callbacks[-1]:
                            callbacks[-1]["outputs"] = []
                        callbacks_dict[cur_callback] = callbacks[-1]
                        callbacks[-1]["outputs"].append(
                                {"type": param_type,
                                 "name": param_data.group(2),
                                 "desc": param_data.group(3)})

                return_data = re.search(expr_returns, line)
                if return_data:
                    if len(methods):
                        methods[-1]["outputs"] = [{"name": return_data.group(1),
                                                      "type": return_data.group(1),
                                                        "desc": return_data.group(2)}]

                depricated_data = re.search(expr_deprecated, line)
                if depricated_data:
                    if len(methods):
                        methods[-1]["depricated"] = {"is_depricated": True,
                                                     "desc": depricated_data.group(1)}
            else:
                in_callback = False
                in_method = False
                new_type_name = ""


        if len(methods):
            api_lib["b4w_api"][-1]["methods"] = methods
        if len(const):
            api_lib["b4w_api"][-1]["module_const"] = const

    api_lib["b4w_api"].append({"name":"callbacks", "methods":callbacks})
    api_lib["types"] = list(types)
    api_lib["callbacks"] = callbacks
    api_lib["aliases"] = typedefs

    api_lib["sensors"] = sensors
    api_lib["js_api"] = js_api_modules
    api_lib["operators"] = operators

    add_all_module(api_lib, "sensors")
    add_all_module(api_lib, "js_api")
    add_all_module(api_lib, "b4w_api")
    add_all_module(api_lib, "operators")
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

import pprint
if __name__ == '__main__':
    data = get_b4w_api()
    dump(data)
    pprint.pprint(data)
