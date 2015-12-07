import os
import re
import json

B4W_PATH = ".."

# api_lib = {
#     "callbacks": [{
#         "name": "callback_name",
#         "desc": "description"
#         "outputs": [{
#             "name": "name",
#             "type": "type",
#             "desc": "description"
#         }, ...
#         ]
#     }],
#     "typedefs": {"new_name": "old_name"},
#     "types": ["type_name", ...],
#     "b4w_api": [{
#         "name": "name",
#         "desc": "description"
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
def Expression_sock_desc(name):
    return {"name":name, "type": "expression", "connectible": 1}
def Sensor_sock_desc(name):
    return {"name":name, "type": "sensor", "connectible": 1}
def Order_sock_desc(name):
    return {"name":name, "type": "Order", "connectible": 1}
def Type_sock_desc(name):
    return {"name":name, "type": "Type", "connectible": 0}

def Sensor_standard_output_desc(payload = True):
    r = [{"name":"sensor", "type":"Sensor"}, {"name":"value"}]
    if payload:
       r.append({"name":"payload"})
    return r

other_stuff = [
# {"name":"variable", "methods":[
#     {"name": "define_local",
#      "inputs":[Order_sock_desc(">Order"),
#                String_sock_desc("name"),
#                Type_sock_desc("Type")],
#      "outputs":[Order_sock_desc("Order>"),],
#     },
#     {"name": "define_global",
#      "inputs":[String_sock_desc("name")],
#      "outputs":[],
#     },
#     {"name": "get_var",
#      "inputs":[
#          String_sock_desc("name", 0),
#      ],
#      "outputs":[
#          Data_sock_desc("variable"),
#           ]
#     },
#     {"name": "set_var",
#      "inputs":[
#          Order_sock_desc(">Order"),
#          String_sock_desc("name", 0),
#          Data_sock_desc("value"),
#      ],
#      "outputs":[
#          Order_sock_desc("Order>"),
#           ]
#     },
#     ]
# },
{"name":"callback", "methods":[
    {"name": "callback_interface",
     "inputs":[Sensor_sock_desc("sensor"),
               {"name":"control_type", "type": "enum", "connectible": 0,
                "enum": ["CT_CHANGE", "CT_CONTINUOUS", "CT_LEVEL", "CT_SHOT", "CT_TRIGGER"]
               },
               Object3D_sock_desc("object")
     ],
     "outputs":[Sensor_sock_desc("sensor"),
                Order_sock_desc("{}"),
                Int_sock_desc("pulse")],
    },
    ]
},
{"name":"data_get_set", "methods":[
    {"name": "get_attr",
     "inputs":[
         String_sock_desc("name", 1),
         Data_sock_desc("data"),
     ],
     "outputs":[
         Data_sock_desc("value"),
          ]
    },
    {"name": "set_attr",
     "inputs":[
         Order_sock_desc(">Order"),
         String_sock_desc("name", 1),
         Data_sock_desc("data"),
         Data_sock_desc("value"),
     ],
     "outputs":[
         Order_sock_desc("Order>"),
          ]
    },
    {"name": "get_value_by_key",
     "inputs":[
         String_sock_desc("name", 1),
         Data_sock_desc("data"),
     ],
     "outputs":[
         Data_sock_desc("value"),
          ]
    },
    {"name": "set_value_by_key",
     "inputs":[
         Order_sock_desc(">Order"),
         String_sock_desc("name", 1),
         Data_sock_desc("data"),
         Data_sock_desc("value"),
     ],
     "outputs":[
         Order_sock_desc("Order>"),
          ]
    },
    ]
},
{"name":"constant", "methods":[
    {"name": "integer",
     "inputs":[Int_sock_desc("value", 0),],
     "outputs":[Int_sock_desc("output", 0)]
    },
    {"name": "float",
     "inputs":[Number_sock_desc("value", 0),],
     "outputs":[Number_sock_desc("output", 0)]
    },
    {"name": "string",
     "inputs":[String_sock_desc("value", 0),],
     "outputs":[String_sock_desc("output", 0)]
    },
    ]
},
{"name":"algorithmic", "methods":[
    {"name": "ifelse",
     "inputs":[Order_sock_desc(">Order"),
               Expression_sock_desc("condition"),
     ],
     "outputs":[
                Order_sock_desc("Order>"),
                Order_sock_desc("True>"),
                Order_sock_desc("False>")
                ],
    },
    {"name": "for",
     "inputs":[Order_sock_desc(">Order"),
               Expression_sock_desc("(*;cond;*)"),
     ],
     "outputs":[
                Order_sock_desc("Order>"),
                Order_sock_desc("(init;*;*)"),
                Order_sock_desc("(*;*;Loop)"),
                Order_sock_desc("Cycle{}")
                ],
    },
    {"name": "forin",
     "inputs":[Order_sock_desc(">Order"),
               Data_sock_desc("collection"),
     ],
     "outputs":[
                Order_sock_desc("Cycle{}"),
                Data_sock_desc("element")
                ],
    },
    {"name": "break",
     "inputs":[Order_sock_desc(">Order"),],
     "outputs":[],
    },
    {"name": "continue",
     "inputs":[Order_sock_desc(">Order"),],
     "outputs":[],
    },
    {"name": "return",
     "inputs":[Order_sock_desc(">Order"),
               Data_sock_desc("value")],
     "outputs":[],
    },
    ]
}
]

operators = [
{"name":"binary", "methods":[
    {"name": "+",
     "inputs":[Number_sock_desc("op1", 1),
               Number_sock_desc("op2", 1),],
     "outputs":[Number_sock_desc("result", 1),],
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
     "inputs":[Sensor_sock_desc("sensor1"),
               Sensor_sock_desc("sensor2")],
     "outputs":[Sensor_sock_desc("result")],
    },
    {"name": "AND",
     "inputs":[Sensor_sock_desc("sensor1"),
               Sensor_sock_desc("sensor2")],
     "outputs":[Sensor_sock_desc("result")],
    },
    {"name": "NOT",
     "inputs":[Sensor_sock_desc("sensor")],
     "outputs":[Sensor_sock_desc("result")],
    },
    ]
}
]

sensors = [
{"name":"controls", "methods":[
    {"name": "keyboard",
     "inputs":[{"name":"key", "socket_type": "Key", "connectible": 0},],
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
                copy_meth["name"] = module["name"]+"."+copy_meth["name"]
                methods.append(copy_meth)

    modules.append({"name": "all", "methods": methods})

def parse_tag_tail(tag_head, tag_body):
    if tag_head in ["param", "const", "returns"]:
        param_all_parts = re.match("\{(.*)\}(.*)", tag_body)
        data = {"type": param_all_parts.group(1).strip()}

        if tag_head == "param":
            param_tail_parts = re.match("(\[.*\]|[^\s]*)(.*)", param_all_parts.group(2).strip())
            data["name"] = param_tail_parts.group(1).strip()
            data["desc"] = param_tail_parts.group(2).strip()
        elif tag_head == "const":
            data["name"] = param_all_parts.group(2).strip()
        elif tag_head == "returns":
            data["desc"] = param_all_parts.group(2).strip()
    elif tag_head in ["type"]:
        data = tag_body[1:-1]
    elif tag_head in ["deprecated", "method", "local", "module", "see", "typedef", "callback"]:
        data = tag_body
    else:
        data = None
    return data

def extract_tag_pair(comment_part):
    try:
        tag_head, tag_body = re.split("\s+", comment_part, 1)
        tag_body_data = parse_tag_tail(tag_head, tag_body)
        return tag_head, tag_body_data
    except:
        return comment_part, ""

def remove_comment_stars(comment_part):
    return re.sub("\n\s*\*", "\n", comment_part).strip()

def find_all_comments(js_text):
    return [(match.group(1).strip(), match.group(2).strip() if match.group(2) else "")
                    for match in re.finditer("/\*\*(.*?)\*/([\n\s]*[^/]*)?\n?", js_text, re.DOTALL)]

def auto_detect_func_name(lines_after_comment):
    for regexp in ["function (\w+)", "\s*(\w+)\s*=\s*function"]:
        match = re.search(regexp, lines_after_comment)
        if match:
            return match.group(1)
    return None

def auto_detect_func_params(lines_after_comment):
    match = re.search("\(([\w\s,]+)\)", lines_after_comment)
    if match:
        return [arg.strip() for arg in match.group(1).split(",")]
    else:
        return None

def parse_comment(comment, lines_after_comment):
    comment_parts = re.split("\n\s*@", comment)
    tags = {
        "description": comment_parts[0].strip(),
        "detected_method_name": auto_detect_func_name(lines_after_comment),
        "detected_method_params": auto_detect_func_params(lines_after_comment)
    }
    for part in comment_parts[1:]:
        tag_head, tag_body = extract_tag_pair(part)
        if tag_head in tags:
            tag_value = tags[tag_head]
            if not isinstance(tags[tag_head],list):
                tags[tag_head] = [tag_value]
            tags[tag_head].append(tag_body)
        else:
            tags[tag_head] = tag_body
    return tags

def parse_comments(js_text):
    return [parse_comment(remove_comment_stars(comment[0]), comment[1]) for comment in find_all_comments(js_text)]

def get_b4w_api():
    path_to_src = os.path.join(B4W_PATH, "src")
    path_to_ext = os.path.join(path_to_src, "ext")
    os.path.normpath(path_to_ext)
    if not os.path.exists(path_to_ext):
        return None
    files = os.listdir(path_to_ext)

    api_lib = {}
    api_lib["b4w_api"] = []

    typedefs = {}
    types = set()
    callbacks = []
    callbacks_dict = {}
    for file in files:


        file_src = open(os.path.join(path_to_ext, file))
        methods = []
        const = []
        cur_callback = ""

        file_text = file_src.read()
        comments_data = parse_comments(file_text)

        module = {"name": "unnamed"}
        def type_update(params):
            if isinstance(params, list):
                for param in params:
                    param["type"] = check_aliases(param["type"], typedefs)
                    types.add(param["type"])
            else:
                params["type"] = check_aliases(params["type"], typedefs)
                types.add(params["type"])
                params = [params]
            return params

        for comment_data in comments_data:
            if "module" in comment_data:
                module["name"] = comment_data["module"]
                if comment_data["description"]:
                    module["desc"] = comment_data["description"]

            if "typedef" in comment_data and "type" in comment_data:
                typedefs[comment_data["typedef"]] = comment_data["type"]

            if "callback" in comment_data:
                callback = {"name":comment_data["callback"]}

                if "param" in comment_data:
                    callback["outputs"] = type_update(comment_data["param"])

                if "description" in comment_data:
                    callback["desc"] = comment_data["description"]
                callbacks.append(callback)

            if "const" in comment_data:
                const.append({"const_name":comment_data["const"]["name"].split(".")[-1],
                              "const_type":comment_data["const"]["type"],
                              "const_desc":comment_data["description"]})

            if "method" in comment_data:
                method = {"name":comment_data["method"].split(".")[-1],
                          "desc":comment_data["description"]}

                if "param" in comment_data:
                    method["inputs"] = type_update(comment_data["param"])
                else:
                    method["inputs"] = []

                if "returns" in comment_data:
                    method["outputs"] = type_update(comment_data["returns"])
                else:
                    method["outputs"] = []

                if "depricated" in comment_data:
                    method["depricated"] = {
                        "is_depricated":True,
                        "desc": comment_data["depricated"]
                    }

                methods.append(method)

        if len(methods):
            module["methods"] = methods
        if len(const):
            module["module_const"] = const

        api_lib["b4w_api"].append(module)

    api_lib["b4w_api"].append({"name":"callbacks", "methods":callbacks})
    api_lib["types"] = list(types)
    api_lib["callbacks"] = callbacks
    api_lib["aliases"] = typedefs

    api_lib["sensors"] = sensors
    api_lib["js_api"] = js_api_modules
    api_lib["operators"] = operators
    api_lib["other_stuff"] = other_stuff

    add_all_module(api_lib, "sensors")
    add_all_module(api_lib, "js_api")
    add_all_module(api_lib, "b4w_api")

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
