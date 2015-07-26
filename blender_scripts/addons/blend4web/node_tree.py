__author__ = 'dal'
import bpy
from bpy.types import NodeTree, Node, NodeSocket
from bpy.props import StringProperty
import copy
# Implementation of custom nodes from Python
SensorSocketColor = (0.0, 1.0, 0.216, 0.5)
SensorNodeColor = (0.55, 0.93, 0.57)
B4WAPINodeColor = (0.71, 0.57, 0.96)
TargetSocketColor = (1.0, 1.0, 0.216, 0.5)
OrderSocketColor = (0.9, 0.4, 0.216, 0.5)
BoolSocketColor = (0.9, 0.4, 0.9, 0.5)
DataSocketColor = (0.9, 0.99, 0.99, 0.5)

# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class B4WLogicNodeTree(NodeTree):
    # Description string
    '''A custom node tree type that will show up in the node editor header'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B4WLogicNodeTreeType'
    # Label for nice name display
    bl_label = 'Blend4Web Logic Node Tree'
    # Icon identifier
    bl_icon = 'NODETREE'

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

editable_types = ['String', 'Axis', 'Key','Object3D', 'Bool', 'Number', 'Vec3', 'Int']
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
        return ntree.bl_idname == 'B4WLogicNodeTreeType'
    def draw_dyn_props(self, dyn_props, layout):
        box = None
        for p in dyn_props:
            pass
            connectible = False
            if hasattr(p, 'ui_type'):
                if p.ui_type == 'connectible':
                    connectible = True
            if not connectible:
                attr_name = get_prop_name_by_type(p.type)
                if box == None:
                    box = layout.box()
                if p.type == 'Object3D':
                    row = box.row()
                    row.prop_search(p, attr_name, bpy.data, 'objects', text=p.name, icon='MARKER')
                else:
                    row = box.row()
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
class FunctionSocket(NodeSocket):
    bl_idname = 'FunctionSocketType'
    bl_label = 'Function Node Socket'
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            # layout.prop(self, "ObjectsProperty", text=text)
            pass
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return SensorSocketColor

class FunctionNodeSensorSocket(NodeSocket):
    bl_idname = 'FunctionNodeSensorSocketType'
    bl_label = 'Function Node Sensor Socket'
    socket_type = ''
    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return SensorSocketColor

class FunctionNodeTargetSocket(NodeSocket):
    bl_idname = 'FunctionNodeTargetSocketType'
    bl_label = 'Function Node Target Socket'
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            # layout.prop(self, "ObjectsProperty", text=text)
            pass
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return TargetSocketColor


class FunctionNode(B4WLogicNode):
    my_items = [
        ("Delay", "Delay", "---"),
        ("SetVisible", "SetVisible", "---"),
    ]
    true_false = [
        ("True", "True", "---"),
        ("False", "False", "---"),
    ]
    delay = bpy.props.FloatProperty(name="DelayType", default = 0)
    setvisible = bpy.props.EnumProperty(name="SetVisibleType",items=true_false)
    def updateNode(self, context):
        pass
    FunctionEnumProperty = bpy.props.EnumProperty(name="FunctionType", description="Function Type", items=my_items, default='Delay', update=updateNode)
    bl_idname = 'FunctionNode'
    bl_label = 'Function'

    def init(self, context):
        self.outputs.new('FunctionSocketType', "")
        self.inputs.new('FunctionNodeSensorSocketType', "")
        self.inputs.new('FunctionNodeTargetSocketType', "")

    def copy(self, node):
        print("Copying from node ", node)

    def draw_buttons(self, context, layout):
        # col = layout.column()
        # # col.prop(self, "activate", text="Update")
        # col.prop_search(self, 'obj_name', bpy.data, 'objects', text='', icon='HAND')
        # if self.show_string_box:
        #     col.prop(self, 'input_text', text='')
        # layout.label("Node settings")
        layout.prop(self, "FunctionEnumProperty", text='')
        if self.FunctionEnumProperty == "Delay":
            layout.prop(self, "delay", text='')

        if self.FunctionEnumProperty == "SetVisible":
            layout.prop(self, "setvisible", text='')

    def draw_label(self):
        return "Function node"

class OrderSocket(NodeSocket):
    bl_idname = 'OrderSocketType'
    bl_label = 'Order Node Socket'
    def draw(self, context, layout, node, text):
        layout.label(text)
    def draw_color(self, context, node):
        return OrderSocketColor

class BoolSocket(NodeSocket):
    bl_idname = 'BoolSocketType'
    bl_label = 'Bool Node Socket'
    def draw(self, context, layout, node, text):
        layout.label(text)
    def draw_color(self, context, node):
        return BoolSocketColor

class DataSocket(NodeSocket):
    bl_idname = 'DataSocketType'
    bl_label = 'Data Node Socket'
    b4w_type = "*"
    def draw(self, context, layout, node, text):
        layout.label(text)
    def draw_color(self, context, node):
        return DataSocketColor

class VariableNode(B4WLogicNode):
    bl_idname = 'VariableNode'
    bl_label = 'Variable'

    action_enum = [
    ("SET", "SET", "---"),
    ("GET", "GET", "---"),
    ]

    action = bpy.props.EnumProperty(name="OperatorType", items=action_enum)
    def updateNode(self, context):
        pass

    variable_name = bpy.props.StringProperty(
        default='',
        description='name of the variable',
        update=updateNode)

    def draw_buttons(self, context, layout):
        if self.action == "SET" and len(self.inputs) != 2:
            self.inputs.clear()
            self.outputs.clear()
            self.inputs.new('OrderSocketType', ">Order")
            self.inputs.new('DataSocketType', "Set")
            self.outputs.new('OrderSocketType', "Order>")
            print("set")
        elif self.action == "GET" and len(self.inputs) == 2:
            self.inputs.clear()
            self.outputs.clear()
            self.outputs.new('DataSocketType', "Get")
            print("get")

        layout.label("Name")
        col = layout.column()
        row = col.row()
        row.prop(self, "action", text='')
        row = col.row()
        row.prop_search(self, 'variable_name', bpy.data, 'objects', text='')

    def init(self, context):
        self.inputs.new('OrderSocketType', ">Order")
        self.inputs.new('DataSocketType', "Set")

        self.outputs.new('OrderSocketType', "Order>")

class GlobalVariableDeclarationNode(B4WLogicNode):
    bl_idname = 'GlobalVariableDeclarationNode'
    bl_label = 'Global variable declaration'

    def updateNode(self, context):
        pass

    variable_name = bpy.props.StringProperty(
        default='',
        description='name of the variable',
        update=updateNode)

    def draw_buttons(self, context, layout):
        layout.label("Name")
        col = layout.column()
        col.prop_search(self, 'variable_name', bpy.data, 'objects', text='')

class UnaryOperatorNode(B4WLogicNode):
    bl_idname = 'UnaryOperatorNode'
    bl_label = 'Unary Operator'

    unary_operator_enum = [
    ("++", "++", "---"),
    ("--", "--", "---"),
    ("+", "+", "---"),
    ("-", "-", "---"),
    ("~", "~", "---"),
    ("!", "!", "---"),
    ("delete", "delete", "---"),
    ("typeof", "typeof", "---"),
    ]

    unary_operation = bpy.props.EnumProperty(name="OperatorType", items=unary_operator_enum)
    def init(self, context):
        s = self.inputs.new('DataSocketType', "")
        s.node_name = self.name
        s.unary_operation = self.unary_operation
        self.outputs.new('DataSocketType', "")

    def copy(self, node):
        print("Copying from node ", node)

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "unary_operation", text='')

    def draw_label(self):
        return "Unary operator node"

class RelationalOperatorNode(B4WLogicNode):
    bl_idname = 'RelationalOperatorNode'
    bl_label = 'Relational Operator'

    relational_operator_enum = [
    ("<", "<", "---"),
    (">", ">", "---"),
    ("<=", "<=", "---"),
    (">=", ">=", "---"),
    ("instanceof", "instanceof", "---"),
    ("==", "==", "---"),
    ("!=", "!=", "---"),
    ("===", "===", "---"),
    ("!==", "!==", "---"),
    ]

    relational_operator = bpy.props.EnumProperty(name="OperatorType", items=relational_operator_enum)
    def init(self, context):
        self.inputs.new('DataSocketType', "")
        self.inputs.new('DataSocketType', "")
        self.outputs.new('DataSocketType', "")

    def copy(self, node):
        print("Copying from node ", node)

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "relational_operator", text='')

    def draw_label(self):
        return "Relational operator node"

class OperatorNode(B4WLogicNode):
    bl_idname = 'OperatorNode'
    bl_label = 'Operator'

    operator_enum = [
    ("ADD", "ADD", "---"),
    ("SUB", "SUB", "---"),
    ("MUL", "MUL", "---"),
    ("DIV", "DIV", "---"),
    ("MOD", "MOD", "---"),
    ("<<", "<<", "Left shift operator"),
    (">>", ">>", "Right shift operator"),
    (">>>", ">>>", "Right shift operator"),
    ]

    operation = bpy.props.EnumProperty(name="OperatorType", items=operator_enum)
    def init(self, context):
        s = self.inputs.new('DataSocketType', "")
        s.node_name = self.name
        s.tree_name = self.id_data.name
        s.operation = self.operation
        self.outputs.new('DataSocketType', "")

    def copy(self, node):
        print("Copying from node ", node)

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "operation", text='')

        if self.operation in ["ADD", "SUB", "MUL"]:
            row = layout.row()
            row.scale_y = 0.8
            opera = row.operator('node.add_input_socket', text="Add input")
            opera.node_name = self.name
            opera.tree_name = self.id_data.name
        else:
            while len(self.inputs) > 2:
                self.inputs.remove(self.inputs[-1])
            while len(self.inputs) < 2:
                self.inputs.new('DataSocketType', "")

    def draw_label(self):
        return "Operator node"

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


class IfelseNode(B4WLogicNode):
    bl_idname = 'IfelseNode'
    bl_label = 'ifelse'
    def updateNode(self, context):
        pass
    def init(self, context):
        self.inputs.new('OrderSocketType', ">Order")
        self.inputs.new('BoolSocketType', "(Cond)")
        self.outputs.new('OrderSocketType', "Order>")
        self.outputs.new('OrderSocketType', "True{}")
        self.outputs.new('OrderSocketType', "False{}")

class ForNode(B4WLogicNode):
    bl_idname = 'ForNode'
    bl_label = 'for'
    def updateNode(self, context):
        pass
    def init(self, context):
        self.inputs.new('OrderSocketType', ">Order")
        self.inputs.new('BoolSocketType', "(*;Cond;*)")


        self.outputs.new('OrderSocketType', "Order>")
        self.outputs.new('OrderSocketType', "(Init;*;*)")
        self.outputs.new('OrderSocketType', "(*;*;Loop)")
        self.outputs.new('OrderSocketType', "Cycle{}")

class ForInNode(B4WLogicNode):
    bl_idname = 'ForInNode'
    bl_label = 'forin'
    def updateNode(self, context):
        pass
    def init(self, context):
        self.inputs.new('OrderSocketType', ">Order")
        self.inputs.new('DataSocketType', "Collection")

        self.outputs.new('OrderSocketType', "Order>")
        self.outputs.new('OrderSocketType', "Cycle{}")
        self.outputs.new('DataSocketType', "Element")


class CallbackInterfaceNode(B4WLogicNode):
    bl_idname = 'CallbackInterfaceNode'
    bl_label = 'Callback interface'
    def updateNode(self, context):
        pass
    def init(self, context):
        self.inputs.new('FunctionNodeSensorSocketType', ">Sensor")

        self.outputs.new('FunctionNodeSensorSocketType', "Sensor>")
        self.outputs.new('OrderSocketType', "Function{}")
        self.outputs.new('DataSocketType', "Pulse")
#-------------------------------

class RemoveInputSocket(bpy.types.Operator):
    bl_idname = "node.remove_socket"
    bl_label = "remove socket"
    bl_options = {'REGISTER', 'UNDO'}
    node_name = StringProperty(name='name node', description='it is name of node',
                               default='')
    socket_name = StringProperty(name='name socket', description='it is name of node',
                               default='')
    tree_name = StringProperty(name='name tree', description='it is name of tree',
                               default='')
    def execute(self, context):
        s = bpy.data.node_groups[self.tree_name].nodes[self.node_name].inputs
        s.remove(s[self.socket_name])
            # .remove(self.socket_name)
        # bpy.data.node_groups[self.tree_name].nodes[self.node_name].inputs.remove('LogicOperatorSocketType', "")
        return {'FINISHED'}

class LogicOperatorSocketInput(NodeSocket):
    bl_idname = 'LogicOperatorSocketInputType'
    bl_label = 'LogicOperator Node Socket'
    node_name = StringProperty(name='name node', description='it is name of node',
                               default='')
    tree_name = StringProperty(name='name tree', description='it is name of tree',
                               default='')
    logic_operation = StringProperty(name='logic operation', description='it is name of logic operation')
    def draw(self, context, layout, node, text):
        row = layout.row()
        row.scale_y = 1
        if not self.logic_operation in "NOT":
            opera = row.operator('node.remove_socket', text="X")
            opera.node_name = self.node_name
            opera.socket_name = self.name
            opera.tree_name = self.tree_name

    def draw_color(self, context, node):
        return SensorSocketColor

class LogicOperatorSocketOutput(NodeSocket):
    bl_idname = 'LogicOperatorSocketOutputType'
    bl_label = 'LogicOperator Node Socket'
    def draw(self, context, layout, node, text):
        pass

    def draw_color(self, context, node):
        return SensorSocketColor
global ID
ID=0
class AddInputSocket(bpy.types.Operator):
    bl_idname = "node.add_input_socket"
    bl_label = "add socket"
    bl_options = {'REGISTER', 'UNDO'}
    node_name = StringProperty(name='name node', description='it is name of node',
                               default='')
    tree_name = StringProperty(name='name tree', description='it is name of tree',
                               default='')

    def execute(self, context):
        global ID
        inputs = bpy.data.node_groups[self.tree_name].nodes[self.node_name].inputs

        if bpy.data.node_groups[self.tree_name].nodes[self.node_name].bl_idname in ["LogicOperatorNode"]:
            s = inputs.new('LogicOperatorSocketInputType', "socket_%s" % ID)
            s.logic_operation = bpy.data.node_groups[self.tree_name].nodes[self.node_name].logic_operation
        else:
            s = inputs.new('DataSocketType', "socket_%s" % ID)
        ID += 1
        s.node_name = self.node_name
        s.tree_name = self.tree_name
        return {'FINISHED'}

class AddInOutSockets(bpy.types.Operator):
    bl_idname = "node.add_inout_sockets"
    bl_label = "add input ad output sockets"
    bl_options = {'REGISTER', 'UNDO'}
    node_name = StringProperty(name='name node', description='it is name of node',
                               default='')
    tree_name = StringProperty(name='name tree', description='it is name of tree',
                               default='')

    def execute(self, context):
        global ID
        inputs = bpy.data.node_groups[self.tree_name].nodes[self.node_name].inputs
        outputs = bpy.data.node_groups[self.tree_name].nodes[self.node_name].outputs

        s = inputs.new('DataSocketType', "socket_%s" % ID)
        s.node_name = self.node_name
        s.tree_name = self.tree_name
        s = outputs.new('DataSocketType', "socket_%s" % ID)
        s.node_name = self.node_name
        s.tree_name = self.tree_name
        ID += 1

        return {'FINISHED'}

class LogicOperatorNode(B4WLogicNode):

    def updateNode(self, context):
        pass

    bl_idname = 'LogicOperatorNode'
    bl_label = 'LogicOperator'

    logic_enum = [
    ("NOT", "NOT", "---"),
    ("AND", "AND", "---"),
    ("OR", "OR", "---"),
    ]
    logic_operation = bpy.props.EnumProperty(name="LogicOperationType",items=logic_enum)
    def init(self, context):
        s = self.inputs.new('LogicOperatorSocketInputType', "")
        s.node_name = self.name
        s.tree_name = self.id_data.name
        s.logic_operation = self.logic_operation
        self.outputs.new('LogicOperatorSocketOutputType', "")


    def copy(self, node):
        print("Copying from node ", node)

    def draw_buttons(self, context, layout):
        row = layout.row()
        row.prop(self, "logic_operation", text='')
        # opera.tree_name = self.id_data.name
        # opera.grup_name = self.groupname
        # opera.sort = self.sort

        if self.logic_operation in ["AND", "OR"]:

            # for inp in self.inputs:
            #     if "LogicOperatorSocketInputStaticType".__eq__(inp.bl_idname):
            #         self.inputs.remove(inp)
            # self.inputs[-1].logic_operation = self.logic_operation
            row = layout.row()
            row.scale_y = 1
            opera = row.operator('node.add_input_socket', text="Add input")
            opera.node_name = self.name
            opera.tree_name = self.id_data.name
        else:
            while len(self.inputs) > 1:
                self.inputs.remove(self.inputs[-1])

            # print (dir(self.inputs[0]))
            # if not "LogicOperatorSocketInputStaticType".__eq__(self.inputs[0].bl_idname):
            #     self.inputs.clear()
            #     s = self.inputs.new('LogicOperatorSocketInputStaticType', "")

    def draw_label(self):
        return "LogicOperator node"


class B4W_Name(bpy.types.PropertyGroup):
    bl_idname = 'Blend4Web_String'
    name = bpy.props.StringProperty(name="name")

#  ----------read B4W API--
import json
import os
curdir = os.path.dirname(os.path.abspath(__file__))
b4w_api_json_path = os.path.join(curdir,"b4w_api.json")
with open(b4w_api_json_path) as data_file:
    b4w_data = json.load(data_file)
#--------------------------
def clear_with_exceptions(ss, exceptions):
    for s in ss:
        if s.bl_idname in exceptions:
            continue
        ss.remove(s)

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

class SensorSocket(NodeSocket):
    bl_idname = "SensorSocketType"
    def draw(self, context, layout, node, text):
        layout.label(text)

    def draw_color(self, context, node):
        return SensorSocketColor
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

class AnyAPINode(B4WLogicNode):
    bl_idname = 'AnyAPINode'
    bl_label = 'AnyAPINode'
    def true_init(self, context):
        self.update_node(context)

    api_type =  bpy.props.StringProperty(
        name = "API type",
        description = "API type",
        update=true_init
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

    def update(self):
        pass

    def add_Order(self):
        s = self.inputs.new('B4WLogicSocket', '>Order')
        s["is_input"] = True
        s.prop.type = "Order"
        s = self.outputs.new('B4WLogicSocket', 'Order>')
        s["is_input"] = False
        s.prop.type = "Order"
    def update_node(self, context):
        self.dyn_props.clear()
        self.modules_names.clear()
        self.methods_names.clear()
        self.inputs.clear()
        self.outputs.clear()

        if self.api_type in ["JS", "B4W"]:
            self.add_Order()

        if self.api_type == "JS":
            api_name = "js_api"

        if self.api_type == "Sensor":
            api_name = "sensors"

        if self.api_type == "B4W":
            api_name = "b4w_api"

        for m in b4w_data[api_name]:
            self.modules_names.add()
            self.modules_names[-1].name = m['name']
            if m['name'] == self.module_name:
                for meth in m['methods']:
                    self.methods_names.add()
                    self.methods_names[-1].name = meth['name']
                    if meth['name'] == self.method_name:
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

        if self.api_type in ["JS", "Sensor", "B4W"]:
            box = layout.box()
            row = box.row()
            row.prop_search(self, 'module_name', self, 'modules_names', text=stage1_name, icon='MARKER')
            row = box.row()
            row.prop_search(self, 'method_name', self, 'methods_names', text=stage2_name, icon='MARKER')
            super(AnyAPINode, self).draw_dyn_props(self.dyn_props,layout)
    def draw_label(self):
        if self.method_name:
            return self.api_type+": "+self.module_name+'.'+self.method_name
        else:
            return self.api_type

class FunctionDeclarationNode(B4WLogicNode):
    bl_idname = 'FunctionDeclarationNode'
    bl_label = 'Function declaration'

    def updateNode(self, context):
        pass

    function_name = bpy.props.StringProperty(
        default='',
        description='name of the function',
        update=updateNode)
    input_text = bpy.props.StringProperty(
        default='', update=updateNode)

    def draw_buttons(self, context, layout):
        layout.label("Name")
        col = layout.column()
        row = col.row()
        row.prop_search(self, 'function_name', bpy.data, 'objects', text='')
        row = col.row()
        opera = row.operator('node.add_inout_sockets', text="Add input")
        opera.node_name = self.name
        opera.tree_name = self.id_data.name

    def init(self, context):
        self.outputs.new('OrderSocketType', "Declaration>")
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
        return context.space_data.tree_type == 'B4WLogicNodeTreeType'

# all categories in a list
node_categories = [
    # identifier, label, items list
    MyNodeCategory("Sensors", "Sensors", items=[
        # our basic node
        NodeItem("AnyAPINode", label="Sensor",  settings={
            "api_type": repr("Sensor"),
            }),
        ]),
    MyNodeCategory("Objects", "Objects", items=[
        NodeItem("TargetNode", label="Target",),
        NodeItem("VariableNode", label="Variable",),
        NodeItem("JSScriptNode", label="JS script",),
        ]),
    MyNodeCategory("Callbacks", "Callbacks", items=[
        # our basic node
        NodeItem("CallbackInterfaceNode", label="Callback interface",),
        NodeItem("FunctionNode", label="Function",),
        ]),
    MyNodeCategory("Algorithmic", "Algorithmic", items=[
        # our basic node
        NodeItem("IfelseNode", label="If Else",),
        NodeItem("ForNode", label="For",),
        NodeItem("ForInNode", label="For In",),
        ]),
    MyNodeCategory("Declarations", "Declarations", items=[
        NodeItem("FunctionDeclarationNode", label="Function",),
        NodeItem("GlobalVariableDeclarationNode", label="Global VariabAle",),
        ]),
    MyNodeCategory("Operators", "Operators", items=[
        NodeItem("UnaryOperatorNode", label="Unary operator",),
        NodeItem("OperatorNode", label="Operator",),
        NodeItem("LogicOperatorNode", label="Logic Operator",),
        NodeItem("RelationalOperatorNode", label="Relational Operator",),
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
    nodeitems_utils.register_node_categories("CUSTOM_NODES1", node_categories)

    # tree
    bpy.utils.register_class(B4WLogicNodeTree)
    bpy.utils.register_class(B4W_Name)
    bpy.utils.register_class(B4W_dyn_param_union)
    # sockets
    bpy.utils.register_class(SensorSocket)
    bpy.utils.register_class(TargetSocket)
    bpy.utils.register_class(FunctionSocket)
    bpy.utils.register_class(LogicOperatorSocketInput)
    bpy.utils.register_class(LogicOperatorSocketOutput)
    bpy.utils.register_class(AddInputSocket)
    bpy.utils.register_class(AddInOutSockets)
    bpy.utils.register_class(RemoveInputSocket)
    bpy.utils.register_class(FunctionNodeSensorSocket)
    bpy.utils.register_class(FunctionNodeTargetSocket)
    bpy.utils.register_class(OrderSocket)
    bpy.utils.register_class(BoolSocket)
    bpy.utils.register_class(DataSocket)

    # nodes
    bpy.utils.register_class(B4WLogicNode)
    bpy.utils.register_class(AnyAPINode)
    bpy.utils.register_class(TargetNode)
    bpy.utils.register_class(FunctionNode)
    bpy.utils.register_class(UnaryOperatorNode)
    bpy.utils.register_class(OperatorNode)
    bpy.utils.register_class(LogicOperatorNode)
    bpy.utils.register_class(RelationalOperatorNode)
    bpy.utils.register_class(VariableNode)
    bpy.utils.register_class(JSScriptNode)
    bpy.utils.register_class(IfelseNode)
    bpy.utils.register_class(ForNode)
    bpy.utils.register_class(ForInNode)
    bpy.utils.register_class(CallbackInterfaceNode)
    bpy.utils.register_class(FunctionDeclarationNode)
    bpy.utils.register_class(GlobalVariableDeclarationNode)
    bpy.utils.register_class(B4WLogicSocket)

def unregister():
    nodeitems_utils.unregister_node_categories("CUSTOM_NODES1")

    # tree
    bpy.utils.unregister_class(B4WLogicNodeTree)

    # sockets
    bpy.utils.unregister_class(SensorSocket)
    bpy.utils.unregister_class(TargetSocket)
    bpy.utils.unregister_class(FunctionSocket)
    bpy.utils.unregister_class(LogicOperatorSocketInput)
    bpy.utils.unregister_class(LogicOperatorSocketOutput)
    bpy.utils.unregister_class(AddInputSocket)
    bpy.utils.unregister_class(AddInOutSockets)
    bpy.utils.unregister_class(RemoveInputSocket)
    bpy.utils.unregister_class(FunctionNodeSensorSocket)
    bpy.utils.unregister_class(FunctionNodeTargetSocket)
    bpy.utils.unregister_class(OrderSocket)
    bpy.utils.unregister_class(BoolSocket)
    bpy.utils.unregister_class(DataSocket)

    # nodes
    bpy.utils.unregister_class(AnyAPINode)
    bpy.utils.unregister_class(TargetNode)
    bpy.utils.unregister_class(FunctionNode)
    bpy.utils.unregister_class(UnaryOperatorNode)
    bpy.utils.unregister_class(OperatorNode)
    bpy.utils.unregister_class(LogicOperatorNode)
    bpy.utils.unregister_class(RelationalOperatorNode)
    bpy.utils.unregister_class(VariableNode)
    bpy.utils.unregister_class(JSScriptNode)
    bpy.utils.unregister_class(IfelseNode)
    bpy.utils.unregister_class(ForNode)
    bpy.utils.unregister_class(ForInNode)
    bpy.utils.unregister_class(CallbackInterfaceNode)
    bpy.utils.unregister_class(FunctionDeclarationNode)
    bpy.utils.unregister_class(GlobalVariableDeclarationNode)
    bpy.utils.unregister_class(B4W_Name)
    bpy.utils.unregister_class(B4W_dyn_param_union)
    bpy.utils.unregister_class(B4WLogicNode)
    bpy.utils.unregister_class(B4WLogicSocket)

if __name__ == "__main__":
    register()
