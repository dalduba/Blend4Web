__author__ = 'dal'
import bpy
from bpy.types import NodeTree, Node, NodeSocket
from bpy.props import StringProperty
from bpy.types import Panel
from slimit import ast
import copy
# Implementation of custom nodes from Python
SensorSocketColor = (0.0, 1.0, 0.216, 0.5)
SensorNodeColor = (0.55, 0.93, 0.57)
B4WAPINodeColor = (0.71, 0.57, 0.96)
TargetSocketColor = (1.0, 1.0, 0.216, 0.5)
OrderSocketColor = (0.9, 0.4, 0.216, 0.5)
BoolSocketColor = (0.9, 0.4, 0.9, 0.5)
DataSocketColor = (0.9, 0.99, 0.99, 0.5)

class B4W_Name(bpy.types.PropertyGroup):
    bl_idname = 'Blend4Web_String'
    name = bpy.props.StringProperty(name="name")

# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class B4WLogicNodeTree(NodeTree):
    # Description string
    '''A custom node tree type that will show up in the node editor header'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B4WNodeScriptTreeType'
    # Label for nice name display
    bl_label = 'Blend4Web Logic Node Tree'
    # Icon identifier
    bl_icon = 'NODETREE'
    functions_names = bpy.props.CollectionProperty(
        name="B4W: functions names",
        type=B4W_Name,
        description="Functions names")
    variables_names = bpy.props.CollectionProperty(
        name="B4W: variables names",
        type=B4W_Name,
        description="variables names")
    types_names = bpy.props.CollectionProperty(
        name="B4W: types names",
        type=B4W_Name,
        description="types names")

# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.

class B4W_dyn_param_union(bpy.types.PropertyGroup):
    bl_idname = 'B4W_dyn_param_union'
    type = bpy.props.StringProperty(name="type")
    name = bpy.props.StringProperty(name="name")
    ui_type = bpy.props.StringProperty(name="ui_type")
    s = bpy.props.StringProperty(name="string")
    f = bpy.props.FloatProperty(name="float")
    b = bpy.props.BoolProperty(name="bool")
    v3 = bpy.props.FloatVectorProperty(name="vector3")
    i = bpy.props.IntProperty(name="integet")

editable_types = ['String', 'Axis', 'Key','Object3D', 'Bool', 'Number', 'Vec3', 'Int', 'Boolean']
def get_prop_name_by_type(type):
    if type in ['String', 'Axis', 'Key','Object3D']:
        return 's'
    if type in ['Bool', 'Boolean']:
       return 'b'
    if type in ['Number']:
        return 'f'
    if type in ['Vec3']:
        return 'v3'
    if type in ["Int"]:
        return 'i'

    return 's'

class B4WLogicSocket(NodeSocket):
    bl_idname = 'B4WLogicSocket'
    bl_label = 'B4WLogicSocket'

    prop = bpy.props.PointerProperty(name='socket prop', type = B4W_dyn_param_union)
    def draw(self, context, layout, node, text):
        p = self.prop
        type = p.type

        if type == "Order":
            layout.label(self.name)
            return

        if self['is_input']:
            attr_name = get_prop_name_by_type(type)
            if not self.is_linked:
                if type == 'Object3D':
                    r = layout.row()
                    r.prop_search(p, attr_name, bpy.data, 'objects', text=p.name+":"+p.type, icon='MARKER')
                elif type in editable_types:
                    layout.prop(p, attr_name, text=p.name+":"+p.type)
                else:
                    layout.label(p.name+":"+p.type)

        if self.is_linked or not self['is_input']:
            layout.label(p.name+":"+p.type)


    def draw_color(self, context, node):
        if self.prop.type == 'Order':
            return OrderSocketColor
        else:
            return DataSocketColor

class B4WLogicNode(Node):
    bl_idname = 'B4WLogicNode'
    bl_label = 'B4WLogicNode'
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'B4WNodeScriptTreeType'
    def draw_dyn_props(self, dyn_props, layout):
        for p in dyn_props:
            pass
            connectible = False
            if hasattr(p, 'ui_type'):
                if p.ui_type == 'connectible':
                    connectible = True
            if not connectible:
                attr_name = get_prop_name_by_type(p.type)
                if p.type == 'Object3D':
                    row = layout.row()
                    row.prop_search(p, attr_name, bpy.data, 'objects', text=p.name, icon='MARKER')
                else:
                    row = layout.row()
                    row.prop(p, attr_name, text=p.name)

    def create_sockets(self,  dyn_props, layout):
        for p in dyn_props:
            if p['ui_type'] == 'input':
                pass
            if p['ui_type'] == 'output':
                pass

    def draw_buttons(self,context, layout):
        pass

    def init(self, context):
        pass

#----------------------
class TargetSocket(NodeSocket):
    bl_idname = 'TargetSocketType'
    bl_label = 'Target Node Socket'
    def draw(self, context, layout, node, text):
        # if self.is_output or self.is_linked:
        #     # layout.prop(self, "ObjectsProperty", text=text)
        #     pass
        # else:
        layout.label(text)

    def draw_color(self, context, node):
        return TargetSocketColor


class TargetNode(B4WLogicNode):
    def updateNode(self, context):
        pass
        # self.process_node(context)

    bl_idname = 'TargetNode'
    bl_label = 'Target'
    obj_name = bpy.props.StringProperty(
        default='',
        description='stores the name of the obj this node references',
        update=updateNode)
    input_text = bpy.props.StringProperty(
        default='', update=updateNode)

    def init(self, context):
        self.outputs.new('TargetSocketType', "")

    def copy(self, node):
        print("Copying from node ", node)

    def draw_buttons(self, context, layout):
        col = layout.column()
        # col.prop(self, "activate", text="Update")
        col.prop_search(self, 'obj_name', bpy.data, 'objects', text='', icon='HAND')
        # col.prop(self, 'input_text', text='')
        layout.label("Node settings")

    def draw_label(self):
        return "Target node"
#--------------------------------

class OrderSocket(NodeSocket):
    bl_idname = 'OrderSocketType'
    bl_label = 'Order Node Socket'
    def draw(self, context, layout, node, text):
        layout.label(text)
    def draw_color(self, context, node):
        return OrderSocketColor

class DataSocket(NodeSocket):
    bl_idname = 'DataSocketType'
    bl_label = 'Data Node Socket'
    b4w_type = "*"
    def draw(self, context, layout, node, text):
        layout.label(text)
    def draw_color(self, context, node):
        return DataSocketColor

class JSScriptNode(B4WLogicNode):
    bl_idname = 'JSScriptNode'
    bl_label = 'JS Script'

    def updateNode(self, context):
        pass

    script_name = bpy.props.StringProperty(
        default='',
        description='name of JavaScript text',
        update=updateNode)

    def init(self, context):
        self.inputs.new('OrderSocketType', ">Order")
        self.outputs.new('OrderSocketType', "Order>")
    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop_search(self, 'script_name', bpy.data, 'texts', text='')

#-------------------------------
global ID
ID = 0
class AddOutSockets(bpy.types.Operator):
    bl_idname = "node.b4w_js_add_out_sockets"
    bl_label = "add output sockets"
    bl_options = {'REGISTER', 'UNDO'}
    node_name = StringProperty(name='name node', description='it is name of node',
                               default='')
    tree_name = StringProperty(name='name tree', description='it is name of tree',
                               default='')

    def execute(self, context):
        node = bpy.data.node_groups[self.tree_name].nodes[self.node_name]
        outputs = node.outputs
        global ID
        while "socket_%s" % ID in outputs:
            ID += 1
        s = outputs.new('B4WLogicSocket', "socket_%s" % ID)
        s.node_name = self.node_name
        s.tree_name = self.tree_name
        s['is_input'] = True
        s.prop.name = "param"
        s.prop.type = "_Data"
        extend_not_connectible_arr(node.dyn_props, [{"name":"param_name", "type": "String", "connectible": 0}])

        return {'FINISHED'}

#  ----------read B4W API--
import json
import os
curdir = os.path.dirname(os.path.abspath(__file__))
b4w_api_json_path = os.path.join(curdir,"b4w_api.json")
with open(b4w_api_json_path) as data_file:
    b4w_data = json.load(data_file)

global data_reloaded_at_startup
data_reloaded_at_startup = False

#--------------------------
def get_module(data, name):
    for m in b4w_data["modules"]:
        if m['name'] == name:
            return m
def get_method(data, name):
    if not "methods" in data:
        return None
    for m in data["methods"]:
        if m['name'] == name:
            return m

def is_connectible(sock_desc):
    connectible = True
    if 'connectible' in sock_desc:
        if not sock_desc['connectible']:
            connectible = False
    return connectible

def get_sock_desc_type(desc):
    type = "_Data"
    if 'type' in desc:
        type = desc['type']
    return type

def add_method_sockets(ss, socks_desc, is_input):
    for sd in socks_desc:
        add = True
        if is_input:
            if not is_connectible(sd):
                add = False
        if add:
            if not 'name' in sd:
                sd['name'] = sd['type']
            s = ss.new('B4WLogicSocket', sd['name'])
            s.prop.type = get_sock_desc_type(sd)
            s.prop.name = sd['name']
            # print(s.prop.type)
            s['is_input'] = copy.copy(is_input)

def extend_not_connectible_arr(dst, search_src):
    for sd in search_src:
        if not is_connectible(sd):
            dst.add()
            sock_type = get_sock_desc_type(sd)
            s = dst[-1]
            s.type = sock_type
            s.name = sd["name"]
            s['is_input'] = True

def update_types(tree):
    global data_reloaded_at_startup
    if not data_reloaded_at_startup:
        tree.types_names.clear()
        print("reload")
        for t in b4w_data["types"]:
            tree.types_names.add()
            tree.types_names[-1].name = t
        data_reloaded_at_startup = True

class AnyAPINode(B4WLogicNode):
    bl_idname = 'AnyAPINode'
    bl_label = 'AnyAPINode'
    def true_init(self, context):
        self.update_node(context)

    def var_update(self, context):
        tree = self.id_data
        update_types(tree)
        if self.bl_idname == "AnyAPINode":
            if self.api_type == "Function":
                tree.functions_names.clear()
            if self.api_type == "Variable":
                tree.variables_names.clear()
        for n in tree.nodes:
            if n.bl_idname == "AnyAPINode":
                if n.api_type == "Function":
                    if n.method_name == "func_decl":
                        if not n.var_name == "":
                            tree.functions_names.add()
                            tree.functions_names[-1].name = n.var_name
                    if n.method_name == "func_call":
                        for nn in tree.nodes:
                            if nn.bl_idname == "AnyAPINode":
                                if nn.api_type == "Function":
                                    if nn.method_name == "func_decl":
                                        if nn.var_name == n.var_name:
                                            n.dyn_props.clear()
                                            n.modules_names.clear()
                                            n.methods_names.clear()
                                            n.inputs.clear()
                                            n.outputs.clear()
                                            for prop in nn.dyn_props:
                                                add_method_sockets(n.inputs,
                                                    [{"name":prop.s, "type": "_Data", "connectible": 1}], True)
                                            add_method_sockets(n.inputs, [{"name":">Order", "type": "Order", "connectible": 1}], True)
                                            add_method_sockets(n.outputs, [{"name":"Order>", "type": "Order", "connectible": 1}], True)
                                            add_method_sockets(n.outputs, [{"name":"return", "type": "_Data", "connectible": 1}], True)
                if n.api_type == "Variable":
                    if n.method_name in ["define_global", "define_local"]:
                        if not n.var_name == "":
                            tree.variables_names.add()
                            tree.variables_names[-1].name = n.var_name
                    if n.method_name in ["get_var", "set_var"]:
                        for nn in tree.nodes:
                            if nn.bl_idname == "AnyAPINode":
                                if nn.api_type == "Variable":
                                    if nn.method_name in ["define_global", "define_local"]:
                                        if nn.var_name == n.var_name:
                                            n.dyn_props.clear()
                                            n.modules_names.clear()
                                            n.methods_names.clear()
                                            n.inputs.clear()
                                            n.outputs.clear()
                                            if n.method_name == "get_var":
                                                add_method_sockets(n.outputs,[{"name":"var", "type": nn.var_type, "connectible": 1}], True)
                                            if n.method_name == "set_var":
                                                add_method_sockets(n.inputs,[{"name":">Order", "type": "Order", "connectible": 1}], True)
                                                add_method_sockets(n.outputs,[{"name":"Order>", "type": "Order", "connectible": 1}], True)
                                                add_method_sockets(n.inputs,[{"name":"var", "type": nn.var_type, "connectible": 1}], True)
 
    api_type =  bpy.props.StringProperty(
        name = "API type",
        description = "API type",
        update=true_init
    )

    callback_name =  bpy.props.StringProperty(
        name = "Callback name",
        description = "Callback name",
    )

    modules_names = bpy.props.CollectionProperty(
        name="B4W: Modules names",
        type=B4W_Name,
        description="Modules names")

    methods_names = bpy.props.CollectionProperty(
        name="B4W: Methods names",
        type=B4W_Name,
        description="Methods names")

    dyn_props = bpy.props.CollectionProperty(
        name="B4W: Dynamic props",
        type=B4W_dyn_param_union,
        description="B4W: Dynamic props")

    var_name =  bpy.props.StringProperty(
        name = "Variable or function name",
        description = "Variable or function name",
        update=var_update
    )
    var_type =  bpy.props.StringProperty(
        name = "Variable type",
        description = "Variable type",
    )

    def update(self):
        pass

    def add_Order(self):
        s = self.inputs.new('B4WLogicSocket', '>Order')
        s["is_input"] = True
        s.prop.type = "Order"
        s = self.outputs.new('B4WLogicSocket', 'Order>')
        s["is_input"] = False
        s.prop.type = "Order"

    def add_Body(self):
        s = self.outputs.new('B4WLogicSocket', 'Body>')
        s["is_input"] = True
        s.prop.type = "Order"
    def is_callback(self):
        if self.module_name == "callbacks":
            return True
        if self.module_name == "all" and  \
            str(self.method_name).startswith("callbacks."):
            return True
        return False
    def update_node(self, context):
        tree = self.id_data
        update_types(tree)
        self.dyn_props.clear()
        self.modules_names.clear()
        self.methods_names.clear()
        self.inputs.clear()
        self.outputs.clear()

        addOrder = False
        if self.api_type in ["JS"]:
            addOrder = True

        if self.api_type in ["B4W"]:
            if not self.is_callback():
                addOrder = True
            else:
                self.add_Body()

        if addOrder:
            self.add_Order()

        api_name = None

        if self.api_type == "JS":
            api_name = "js_api"

        if self.api_type == "Sensor":
            api_name = "sensors"

        if self.api_type == "B4W":
            api_name = "b4w_api"

        if self.api_type == "Operators":
            api_name = "operators"

        if self.api_type == "OtherStuff":
            api_name = "other_stuff"

        if self.api_type == "Function":
            if self.method_name == "func_decl":
                add_method_sockets(self.outputs, [{"name":"Declaration>", "type": "Order", "connectible": 1}], True)
            return

        if self.api_type == "Variable":
            if self.method_name == "define_global":
                pass
            if self.method_name == "define_local":
                add_method_sockets(self.inputs, [{"name":">Order", "type": "Order", "connectible": 1}], True)
                add_method_sockets(self.outputs, [{"name":"Order>", "type": "Order", "connectible": 1}], True)
            return

        if api_name == None:
            return

        for m in b4w_data[api_name]:
            self.modules_names.add()
            self.modules_names[-1].name = m['name']
            if m['name'] == self.module_name:
                for meth in m['methods']:
                    self.methods_names.add()
                    self.methods_names[-1].name = meth['name']
                    if meth['name'] == self.method_name:
                        if self.is_callback():
                            if "outputs" in meth:
                                add_method_sockets(self.outputs, meth['outputs'], False)
                        else:
                            if "inputs" in meth:
                                extend_not_connectible_arr(self.dyn_props, meth['inputs'])
                                add_method_sockets(self.inputs, meth['inputs'], True)
                            if "outputs" in meth:
                                add_method_sockets(self.outputs, meth['outputs'], False)


    module_name = bpy.props.StringProperty(
        name = "Module name",
        description = "Module name",
        update = update_node,
        default = 'all'
    )

    method_name = bpy.props.StringProperty(
        name = "Method name",
        description = "Method name",
        update = update_node
    )
    def draw_dyn_param(self, container, prop_name, layout):
        row = layout.row()
        row.prop(container, prop_name, text=container['socket_name'])

    def draw_buttons(self, context, layout):

        stage1_name = "module"
        stage2_name = "method"

        if self.api_type == "Sensor":
            stage1_name = "category"
            stage2_name = "sensor"

        draw_module_name = False
        draw_method_name = False
        if self.api_type in ["JS", "Sensor", "B4W"]:
            draw_module_name = True
            draw_method_name = True

        if self.api_type in ["Operators"]:
            draw_method_name = True
        if draw_module_name:
            row = layout.row()
            row.prop_search(self, 'module_name', self, 'modules_names', text=stage1_name, icon='MARKER')
        if draw_method_name:
            row = layout.row()
            row.prop_search(self, 'method_name', self, 'methods_names', text=stage2_name, icon='MARKER')
        super(AnyAPINode, self).draw_dyn_props(self.dyn_props,layout)

        if self.is_callback():
            row = layout.row()
            row.prop(self, "callback_name", text="Callback Name")

        if self.api_type == "Function":
            if self.method_name == "func_decl":
                row = layout.row()
                row.prop(self, "var_name", "func_name")
                row = layout.row()
                opera = row.operator('node.b4w_js_add_out_sockets', text="Add input")
                opera.node_name = self.name
                opera.tree_name = self.id_data.name
            if self.method_name == "func_call":
                row = layout.row()
                row.prop_search(self, 'var_name', self.id_data, 'functions_names', text="function", icon='MARKER')
        if self.api_type == "Variable":
            if self.method_name in ["define_global", "define_local"]:
                row = layout.row()
                row.prop_search(self, 'var_type', self.id_data, 'types_names', text="type", icon='MARKER')
                row = layout.row()
                row.prop(self, "var_name", "var_name")
            if self.method_name in ["get_var", "set_var"]:
                row = layout.row()
                row.prop_search(self, 'var_name', self.id_data, 'variables_names', text="var", icon='MARKER')

    def draw_label(self):
        if self.api_type == "OtherStuff":
            return self.method_name
        if self.method_name:
            return self.api_type+": "+self.module_name+'.'+self.method_name
        else:
            return self.api_type
#-------------------------------
module_name_to_m_ident = {
    "anchors" : "m_anchors",
    "animation" : "m_anim",
    "camera" : "m_cam",
    "config" : "m_cfg",
    "constrains" : "m_constraints",
    "container" : "m_container",
    "controls" : "m_ctrls",
    "data" : "m_data",
    "debug" : "m_dbg",
    "geometry" : "m_geom",
    "assets" : "m_assets",
    "app" : "m_app",

}

def get_module_name(node):
    all = False
    if "module_name" in node:
        if node["module_name"] != "all":
            return node["module_name"]
        else:
            all = True
    else:
        all = True

    if all:
        if "method_name" in node:
            return node["method_name"].split(".")[0]
        else:
            return None
    return None

def get_module_ident(node):
    name = get_module_name(node)
    if name in module_name_to_m_ident:
        return name, module_name_to_m_ident[name]
    else:
        if name:
            return name, "m_%s" % name
        else:
            return None

def decl_global_vars(vars):
    # TODO make declarations corresponding to type
    items = []
    for v in vars:
        s = ast.VarDecl(ast.Identifier(v))
        items.append(ast.VarStatement([s]))
    return items

def get_target_node_and_socket(from_node, from_sock, node_data):
    for l in node_data["links"]:
        if l["from_node"] == from_node and l["from_socket"] == from_sock:
            return l["to_node"], l["to_socket"]
    return None

def get_source_node_and_socket(to_node, to_sock, node_data):
    print(to_node, to_sock)
    for l in node_data["links"]:
        if l["to_node"] == to_node and l["to_socket"] == to_sock:
            return l["from_node"], l["from_socket"]
    return None

def get_node(name, node_data):
    for n in node_data["nodes"]:
        if n["name"] == name:
            return n
    return None

def get_sock_type(node, socket_name, container = "outputs"):
    for s in node[container]:
        if s["identifier"] == socket_name:
            return s["type"]
    return None

def get_sock_index(container, sock_name):
    i = 0
    for s in container:
        if s["identifier"] == sock_name:
            return i
        i += 1
    return -1

def get_sock_by_name(container, sock_name):
    for s in container:
        if s["identifier"] == sock_name:
            return s
    return None

def gen_block(node, socket_name, data, main_block):
    ret = get_target_node_and_socket(node["name"], socket_name, data)
    while True:
        if not ret:
            return
        processed = False
        to_node, to_socket = ret
        cur_node = get_node(to_node, data)
        print(cur_node)
        type = get_sock_type(cur_node, to_socket, "inputs")
        if not type == "Order":
            raise "socket type must be 'Order', but %s" % type

        if cur_node["api_type"] == "Variable":
            if cur_node["method_name"] == "define_local":
                v = cur_node["props"]["var_name"]["value"]
                if v == "var":
                    v = "_var"
                s = ast.VarDecl(ast.Identifier(v))

                main_block.append(ast.VarStatement([s]))
                ret = get_target_node_and_socket(cur_node["name"], "Order>", data)
                processed = True

            if cur_node["method_name"] == "set_var":
                ret = get_source_node_and_socket(cur_node["name"], "value", data)
                if ret:
                    nd, sk = ret
                    # TODO implement
                    r = ast.Identifier("not_implemented_yet")
                else:
                    sock = get_sock_by_name(cur_node["inputs"], "var")
                    r = ast.Number(sock["value"])
                set = ast.Assign("=", ast.Identifier(cur_node["props"]["var_name"]["value"]), r)
                main_block.append(ast.ExprStatement(set))
                ret = get_target_node_and_socket(cur_node["name"], "Order>", data)
                processed = True

        elif cur_node["api_type"] == "OtherStuff":
            if cur_node["module_name"] == "algorithmic":
                if cur_node["method_name"] == "ifelse":
                    # gen condition
                    ret = get_source_node_and_socket(cur_node["name"], "condition", data)
                    if ret:
                        nd_name, sk_name = ret
                        nd = get_node(nd_name, data)
                        t = get_sock_type(nd, sk_name)
                        if not t or t == "Order":
                            raise "bad input socket type: %s" % t
                        predicate = None
                        if nd["api_type"] == "Function":
                            ind = get_sock_index(nd["outputs"], sk_name)
                            predicate = ast.Identifier(nd["props"]["param_name"][ind-1]["value"])
                        if not predicate:
                            predicate = ast.Identifier("false")
                        consequent = []
                        gen_block(cur_node, "True>", data, consequent)
                        print("====================")
                        print(consequent)
                        alternative = []
                        gen_block(cur_node, "False>", data, alternative)

                        ifelse = ast.If(predicate, ast.Block(consequent), ast.Block(alternative))
                        main_block.append(ifelse)
                    else:
                        raise "no condition"
                    # print(ret)
                    ret = get_target_node_and_socket(cur_node["name"], "Order>", data)
                    processed = True
                if cur_node["method_name"] == "return":
                    ret = get_source_node_and_socket(cur_node["name"], "value", data)
                    r = None
                    if ret:
                        nd_name, sk_name = ret
                        nd = get_node(nd_name, data)
                        t = get_sock_type(nd, sk_name)
                        if not t or t == "Order":
                            raise "bad input socket type: %s" % t

                        if nd["api_type"] == "Variable":
                            if nd["method_name"] == "get_var":
                                # TODO make renaming for reserved words
                                r = ast.Identifier(nd["props"]["var_name"]["value"])
                    if r:
                        ret = ast.Return(r)
                    else:
                        ret = ast.Return()
                    main_block.append(ret)
                    return
        if not processed:
            print("-----return-----")
            return


def gen_func_decl(node, data):
    params = []
    if "param_name" in node["props"]:
        for p in node["props"]["param_name"]:
            params.append(ast.Identifier(p["value"]))
    main_block = []
    gen_block(node, "Declaration>", data, main_block)
    print(node["props"]["var_name"])
    s = ast.VarDecl(ast.Identifier(node["props"]["var_name"]["value"]), ast.FuncExpr(None, params, main_block))
    return ast.VarStatement([s])
def process_node_script(node_tree):
    print (node_tree)
    data = {}

    # data["nodes"] = [{}, {},..., {}]
    # data["links"] = [
    #     {
    #         "from_node": node name
    #         "to_node": node name
    #         "from_socket": socket identifier
    #         "to_socket": socket identifier
    #     }, ...
    # ]

    data["nodes"] = []
    data["links"] = []
    data["sensor_nodes"] = []
    data["global_variable_decl_nodes"] = []
    data["global_function_decl_nodes"] = []
    data["usage_modules"] = set()
    # may be another data

    for node in node_tree.nodes:
        if node.bl_idname in ["AnyAPINode"]:

            node_data = {}

            node_data["name"] = node.name
            node_data["api_type"] = node.api_type

            props = {}
            pnames = []
            for p in node.dyn_props:
                if p.name == "param_name":
                    pname = {"type": p.type, "value":getattr(p, get_prop_name_by_type(p.type))}
                    pnames.append(pname)
                    props[p.name] = pnames
                else:
                    props[p.name] = {"type": p.type, "value":getattr(p, get_prop_name_by_type(p.type))}

            if "method_name" in node:
                node_data["method_name"] = node["method_name"]
                if node_data["method_name"] in ["define_global", "define_local"]:
                    props["var_name"] = {"type": "String", "value": node.var_name}
                    props["var_type"] = {"type": "String", "value": node.var_type}
                if node_data["method_name"] in ["set_var", "get_var", "func_decl"]:
                    props["var_name"] = {"type": "String", "value": node.var_name}

            if "module_name" in node:
                node_data["module_name"] = node["module_name"]

            node_data["props"] = props

            node_data["inputs"] = []
            for sock in node.inputs:
                socket_data = {}
                socket_data["name"] = sock.name
                socket_data["identifier"] = sock.identifier
                socket_data["type"] = sock.prop.type
                socket_data["value"] = getattr(sock.prop, get_prop_name_by_type(sock.prop.type))
                node_data["inputs"].append(socket_data)

            node_data["outputs"] = []
            for sock in node.outputs:
                socket_data = {}
                socket_data["name"] = sock.name
                socket_data["identifier"] = sock.identifier
                socket_data["type"] = sock.prop.type
                socket_data["value"] = getattr(sock.prop, get_prop_name_by_type(sock.prop.type))
                node_data["outputs"].append(socket_data)

            if node_data["api_type"] == "B4W":
                if "module_name" in node and not node["module_name"] in data["usage_modules"]:
                    data["usage_modules"].add(node["module_name"])
            elif node_data["api_type"] == "Sensor":
                data["sensor_nodes"].append(node_data)
            elif node_data["api_type"] == "FuncDecl":
                data["global_function_decl_nodes"].append(node_data)
            elif node_data["api_type"] == "Variable" and node_data["method_name"] == "define_global":
                data["global_variable_decl_nodes"].append(node_data)

            data["nodes"].append(node_data)

    for link in node_tree.links:
        link_data = {}

        link_data["from_node"] = link.from_node.name
        link_data["to_node"] = link.to_node.name
        link_data["from_socket"] = link.from_socket.identifier
        link_data["to_socket"] = link.to_socket.identifier
        data["links"].append(link_data)

    import pprint
    pprint.pprint(data)

    # road map:
    # 1) independent script
    #   - firstly node script should work with not html apps
    #   - just generate here valid javascript and then manually include it into the app
    # 2) dependant script:
    #   - logic editor is main
    #   - node script is main

    #     --------------
    print("---------")
    exports = ast.Identifier("exports")
    require = ast.Identifier("require")

    modules = {}
    variables = {}
    func_decls = []
    for node in data["nodes"]:
        if node["api_type"] == "B4W":
            ret = get_module_ident(node)
            if ret:
                modules[ret[1]] = ret[0]
        elif node["api_type"] == "Variable":
            if node["method_name"] == "define_global":
                variables[node["props"]["var_name"]["value"]] = node["props"]["var_type"]["value"]
        elif node["api_type"] == "Function":
            if node["method_name"] == "func_decl":
                # gen function declaration
                # and then recursive invokation of body generation
                decl = gen_func_decl(node, data)
                if decl:
                    func_decls.append(decl)
                pass

    decl_vars = decl_global_vars(variables)
    import_modules = []
    for m in modules:
        init = ast.FunctionCall(require, [ast.Identifier('"%s"' % modules[m])])
        decl = ast.VarDecl(ast.Identifier(m), init)
        import_modules.append(ast.VarStatement([decl]))

    module_identifier = '"module_name"'

    use_strict = ast.ExprStatement(ast.String('"use_strict"'))
    root = ast.Program()
    main_block = []
    for s in import_modules:
        main_block.append(s)

    main_block.extend(decl_vars)
    main_block.extend(func_decls)

    main_func_decl = ast.FuncExpr(None, [exports, require], main_block)
    b4w_register = ast.ExprStatement(
        ast.FunctionCall(ast.DotAccessor(ast.Identifier("b4w"),ast.Identifier("register")),
                         [ast.String(module_identifier),main_func_decl]))

#--------------------
    identifier = ast.Identifier("f1")
    params = [ast.Identifier("p1"),ast.Identifier("p2")]
    elements = [
                ast.ExprStatement(ast.Assign("=", ast.Identifier("a"),
                ast.BinOp("+", ast.Identifier("p1"), ast.Identifier("p2")))),
                ast.Return(ast.Identifier("a"))]
    funcdecl = ast.FuncDecl(identifier, params, elements)
#--------------------
    root._children_list.append(use_strict)
    # b4w.register("module_name", function(exports, require) {})
    root._children_list.append(b4w_register)
    # var m_app   = require("app");

    # root._children_list.append(funcdecl)

    print((root.to_ecma()))

class NODE_ExportNodeScriptPanel(Panel):
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_label = 'Node Script to JS'
    @classmethod
    def poll(cls, context):
        snode = context.space_data
        return snode is not None and snode.node_tree is not None and snode.tree_type == "B4WNodeScriptTreeType"
    def draw(self, context):
        row = self.layout.row()
        row.operator("b4w.node_to_js", text="Export node tree", icon="NODETREE")

class B4WNodeScriptToJSOperator(bpy.types.Operator):
    bl_idname = "b4w.node_to_js"
    bl_label = "B4W Export node script to JS"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        process_node_script(context.space_data.node_tree)
        return {"FINISHED"}

#-------------------------------

### Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see release/scripts/startup/nodeitems_builtins.py

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem


# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type
class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'B4WNodeScriptTreeType'

# all categories in a list
node_categories = [
    # identifier, label, items list
    MyNodeCategory("Sensors", "Sensors", items=[
        # our basic node
        NodeItem("AnyAPINode", label="Sensor",  settings={
            "api_type": repr("Sensor"),
            }),
        NodeItem("AnyAPINode", label="Logic Sensor Operator",  settings={
            "api_type": repr("Operators"), "module_name": repr("sensor")
            }),
        ]),
    MyNodeCategory("Constant", "Constant", items=[
        NodeItem("AnyAPINode", label="Integer",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("constant"), "method_name": repr("integer")
            }),
        NodeItem("AnyAPINode", label="Float",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("constant"), "method_name": repr("float")
            }),
        NodeItem("AnyAPINode", label="String",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("constant"), "method_name": repr("string")
            }),
        ]),
    MyNodeCategory("Variable", "Variable", items=[
        NodeItem("AnyAPINode", label="Define Global",  settings={
            "api_type": repr("Variable"), "method_name": repr("define_global")
            }),
        NodeItem("AnyAPINode", label="Define Local",  settings={
            "api_type": repr("Variable"), "method_name": repr("define_local")
            }),
        NodeItem("AnyAPINode", label="Get Variable",  settings={
            "api_type": repr("Variable"), "method_name": repr("get_var")
            }),
        NodeItem("AnyAPINode", label="Set Variable",  settings={
            "api_type": repr("Variable"), "method_name": repr("set_var")
            }),
        ]),
    MyNodeCategory("Function", "Function", items=[
        NodeItem("AnyAPINode", label="Declaration",  settings={
            "api_type": repr("Function"), "method_name": repr("func_decl")
            }),
        NodeItem("AnyAPINode", label="Call",  settings={
            "api_type": repr("Function"),"method_name": repr("func_call")
            }),
        ]),
    MyNodeCategory("Data", "Data", items=[
        NodeItem("AnyAPINode", label="Get Attribute",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("data_get_set"), "method_name": repr("get_attr")
            }),
        NodeItem("AnyAPINode", label="Get Value By Key",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("data_get_set"), "method_name": repr("get_value_by_key")
            }),
        NodeItem("AnyAPINode", label="Set Attribute",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("data_get_set"), "method_name": repr("set_attr")
            }),
        NodeItem("AnyAPINode", label="Set Value By Key",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("data_get_set"), "method_name": repr("set_value_by_key")
            }),
        ]),
    MyNodeCategory("Objects", "Objects", items=[
        NodeItem("TargetNode", label="Target",),
        NodeItem("JSScriptNode", label="JS script",),
        ]),
    MyNodeCategory("Callbacks", "Callbacks", items=[
        # our basic node
        NodeItem("AnyAPINode", label="Callback Interface",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("callback"), "method_name": repr("callback_interface")
            }),
        ]),
    MyNodeCategory("Algorithmic", "Algorithmic", items=[
        # our basic node
        NodeItem("AnyAPINode", label="If Else",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("algorithmic"), "method_name": repr("ifelse")
            }),
        NodeItem("AnyAPINode", label="For",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("algorithmic"), "method_name": repr("for")
            }),
        NodeItem("AnyAPINode", label="For in",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("algorithmic"), "method_name": repr("forin")
            }),
        NodeItem("AnyAPINode", label="Break",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("algorithmic"), "method_name": repr("break")
            }),
        NodeItem("AnyAPINode", label="Continue",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("algorithmic"), "method_name": repr("continue")
            }),
        NodeItem("AnyAPINode", label="Return",  settings={
            "api_type": repr("OtherStuff"), "module_name": repr("algorithmic"), "method_name": repr("return")
            }),
        ]),
    MyNodeCategory("Operators", "Operators", items=[
        NodeItem("AnyAPINode", label="Binary",  settings={
            "api_type": repr("Operators"), "module_name": repr("binary")
            }),
        NodeItem("AnyAPINode", label="Unary",  settings={
            "api_type": repr("Operators"), "module_name": repr("unary")
            }),
        NodeItem("AnyAPINode", label="Logic",  settings={
            "api_type": repr("Operators"), "module_name": repr("logic")
            }),
        ]),
    MyNodeCategory("Call methods", "Call Methods", items=[
        NodeItem("AnyAPINode", label="JS API",  settings={
            "api_type": repr("JS"),
            }),
        NodeItem("AnyAPINode", label="B4W",  settings={
            "api_type": repr("B4W"),
            }),
        ]),
    ]

def register():
    bpy.utils.register_class(B4W_Name)
    nodeitems_utils.register_node_categories("B4W_NODE_SCRIPT_CUSTOM_NODES", node_categories)
    # exporter
    bpy.utils.register_class(B4WNodeScriptToJSOperator)

    # tree
    bpy.utils.register_class(B4WLogicNodeTree)

    bpy.utils.register_class(B4W_dyn_param_union)
    # sockets
    bpy.utils.register_class(TargetSocket)
    bpy.utils.register_class(AddOutSockets)
    bpy.utils.register_class(OrderSocket)
    bpy.utils.register_class(DataSocket)

    # nodes
    bpy.utils.register_class(B4WLogicNode)
    bpy.utils.register_class(AnyAPINode)
    bpy.utils.register_class(TargetNode)
    bpy.utils.register_class(JSScriptNode)
    bpy.utils.register_class(B4WLogicSocket)
    bpy.utils.register_class(NODE_ExportNodeScriptPanel)

def unregister():
    nodeitems_utils.unregister_node_categories("B4W_NODE_SCRIPT_CUSTOM_NODES")
    # exporter
    bpy.utils.register_class(B4WNodeScriptToJSOperator)

    # tree
    bpy.utils.unregister_class(B4WLogicNodeTree)

    # sockets
    bpy.utils.unregister_class(TargetSocket)
    bpy.utils.unregister_class(AddOutSockets)
    bpy.utils.unregister_class(OrderSocket)
    bpy.utils.unregister_class(DataSocket)

    # nodes
    bpy.utils.unregister_class(AnyAPINode)
    bpy.utils.unregister_class(TargetNode)
    bpy.utils.unregister_class(JSScriptNode)
    bpy.utils.unregister_class(B4W_Name)
    bpy.utils.unregister_class(B4W_dyn_param_union)
    bpy.utils.unregister_class(B4WLogicNode)
    bpy.utils.unregister_class(B4WLogicSocket)
    bpy.utils.unregister_class(NODE_ExportNodeScriptPanel)

if __name__ == "__main__":
    register()
