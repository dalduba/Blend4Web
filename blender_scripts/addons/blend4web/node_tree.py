__author__ = 'dal'
import bpy
from bpy.types import NodeTree, Node, NodeSocket
from bpy.props import StringProperty

import os
import re

def get_b4w_api():
    b4w_src_path = bpy.context.user_preferences.addons["blend4web"].preferences.b4w_src_path

    path_to_src = os.path.join(b4w_src_path, "src")
    path_to_ext = os.path.join(b4w_src_path, "ext")
    os.path.normpath(path_to_ext)
    if not (b4w_src_path != "" and os.path.exists(path_to_ext)):
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

        api_lib.append({"name": module_name})
        file_src = open(EXT_DIR + file)
        methods = []
        const = []
        for line in file_src.readlines():
            const_data = re.search(expr_const, line)
            if const_data:
                const.append({"name":const_data.group(3),
                              "type":const_data.group(1)})

            method_data = re.search(expr_method, line)
            if method_data:
                methods.append({"name":method_data.group(2)})
            param_data = re.search(expr_param, line)
            if param_data:
                if len(methods):
                    if "params" not in methods[-1]:
                        methods[-1]["params"] = []
                    methods[-1]["params"].append({"type": param_data.group(1),
                                                  "name": param_data.group(2),
                                                  "desc": param_data.group(3)})
            return_data = re.search(expr_returns, line)
            if return_data:
                if len(methods):
                    methods[-1]["return"] = {"type": return_data.group(1),
                                             "desc": return_data.group(2)}
            depricated_data = re.search(expr_deprecated, line)
            if depricated_data:
                if len(methods):
                    methods[-1]["depricated"] = {"is_depricated": True,
                                                 "desc": depricated_data.group(1)}

        api_lib[-1]["method"] = methods
        api_lib[-1]["const"] = const
    print(api_lib)
    return api_lib

# Implementation of custom nodes from Python
SensorSocketColor = (0.0, 1.0, 0.216, 0.5)
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
class B4WLogicNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'B4WLogicNodeTreeType'

class SensorSocket(NodeSocket):
    bl_idname = 'SensorSocketType'
    bl_label = 'Sensor Node Socket'
    my_items = [
        ("Init", "Init", "Fire at Initialisation time"),
        ("Always", "Always", "Fire every frame"),
        ("Bounding begin", "Bounding begin", "---"),
        ("Bounding end", "Bounding end", "---"),
    ]
    myEnumProperty = bpy.props.EnumProperty(name="SensorType", description="Sensor Type", items=my_items, default='Init')

    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.prop(self, "myEnumProperty", text=text)
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return SensorSocketColor


class SensorNode(Node, B4WLogicNode):
    bl_idname = 'SensorNode'
    bl_label = 'Sensor'

    def init(self, context):
        self.outputs.new('SensorSocketType', "")

    def copy(self, node):
        print("Copying from node ", node)

    def draw_buttons(self, context, layout):
        layout.label("Node settings")

    def draw_label(self):
        return "Sensor node"

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


class TargetNode(Node, B4WLogicNode):
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


class FunctionNode(Node, B4WLogicNode):
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
    def draw(self, context, layout, node, text):
        layout.label(text)
    def draw_color(self, context, node):
        return DataSocketColor

class VariableNode(Node, B4WLogicNode):
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
    input_text = bpy.props.StringProperty(
        default='', update=updateNode)

    def draw_buttons(self, context, layout):

        # TODO: check bug of "GET" action
        if self.action == "SET" and len(self.inputs) != 2:
            self.inputs.clear()
            self.outputs.clear()
            self.inputs.new('OrderSocketType', ">Order")
            self.inputs.new('DataSocketType', "Set")
            self.outputs.new('OrderSocketType', "Order>")
        elif self.action == "GET" and len(self.inputs) != 1:
            self.inputs.clear()
            self.outputs.clear()
            self.outputs.new('DataSocketType', "Get")

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

class GlobalVariableDeclarationNode(Node, B4WLogicNode):
    bl_idname = 'GlobalVariableDeclarationNode'
    bl_label = 'Global variable declaration'

    def updateNode(self, context):
        pass

    variable_name = bpy.props.StringProperty(
        default='',
        description='name of the variable',
        update=updateNode)
    input_text = bpy.props.StringProperty(
        default='', update=updateNode)

    def draw_buttons(self, context, layout):
        layout.label("Name")
        col = layout.column()
        col.prop_search(self, 'variable_name', bpy.data, 'objects', text='')

class UnaryOperatorNode(Node, B4WLogicNode):
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

class RelationalOperatorNode(Node, B4WLogicNode):
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

class OperatorNode(Node, B4WLogicNode):
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
            while len(self.inputs) > 1:
                self.inputs.remove(self.inputs[-1])

    def draw_label(self):
        return "Operator node"

class IfelseNode(Node, B4WLogicNode):
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

class ForNode(Node, B4WLogicNode):
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

class ForInNode(Node, B4WLogicNode):
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


class CallbackInterfaceNode(Node, B4WLogicNode):
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

class LogicOperatorNode(Node, B4WLogicNode):

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

class FunctionDeclarationNode(Node, B4WLogicNode):
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
        opera = row.operator('node.add_input_socket', text="Add input")
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
        NodeItem("SensorNode", label="Sensor"),
        ]),
    MyNodeCategory("Objects", "Objects", items=[
        NodeItem("TargetNode", label="Target",),
        NodeItem("VariableNode", label="Variable",),
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
    ]


def register():
    nodeitems_utils.register_node_categories("CUSTOM_NODES", node_categories)

    # tree
    bpy.utils.register_class(B4WLogicNodeTree)

    # sockets
    bpy.utils.register_class(SensorSocket)
    bpy.utils.register_class(TargetSocket)
    bpy.utils.register_class(FunctionSocket)
    bpy.utils.register_class(LogicOperatorSocketInput)
    bpy.utils.register_class(LogicOperatorSocketOutput)
    bpy.utils.register_class(AddInputSocket)
    bpy.utils.register_class(RemoveInputSocket)
    bpy.utils.register_class(FunctionNodeSensorSocket)
    bpy.utils.register_class(FunctionNodeTargetSocket)
    bpy.utils.register_class(OrderSocket)
    bpy.utils.register_class(BoolSocket)
    bpy.utils.register_class(DataSocket)

    # nodes
    bpy.utils.register_class(SensorNode)
    bpy.utils.register_class(TargetNode)
    bpy.utils.register_class(FunctionNode)
    bpy.utils.register_class(UnaryOperatorNode)
    bpy.utils.register_class(OperatorNode)
    bpy.utils.register_class(LogicOperatorNode)
    bpy.utils.register_class(RelationalOperatorNode)
    bpy.utils.register_class(VariableNode)
    bpy.utils.register_class(IfelseNode)
    bpy.utils.register_class(ForNode)
    bpy.utils.register_class(ForInNode)
    bpy.utils.register_class(CallbackInterfaceNode)
    bpy.utils.register_class(FunctionDeclarationNode)
    bpy.utils.register_class(GlobalVariableDeclarationNode)


def unregister():
    nodeitems_utils.unregister_node_categories("CUSTOM_NODES")

    # tree
    bpy.utils.unregister_class(B4WLogicNodeTree)

    # sockets
    bpy.utils.unregister_class(SensorSocket)
    bpy.utils.unregister_class(TargetSocket)
    bpy.utils.unregister_class(FunctionSocket)
    bpy.utils.unregister_class(LogicOperatorSocketInput)
    bpy.utils.unregister_class(LogicOperatorSocketOutput)
    bpy.utils.unregister_class(AddInputSocket)
    bpy.utils.unregister_class(RemoveInputSocket)
    bpy.utils.unregister_class(FunctionNodeSensorSocket)
    bpy.utils.unregister_class(FunctionNodeTargetSocket)
    bpy.utils.unregister_class(OrderSocket)
    bpy.utils.unregister_class(BoolSocket)
    bpy.utils.unregister_class(DataSocket)

    # nodes
    bpy.utils.unregister_class(SensorNode)
    bpy.utils.unregister_class(TargetNode)
    bpy.utils.unregister_class(FunctionNode)
    bpy.utils.unregister_class(UnaryOperatorNode)
    bpy.utils.unregister_class(OperatorNode)
    bpy.utils.unregister_class(LogicOperatorNode)
    bpy.utils.unregister_class(RelationalOperatorNode)
    bpy.utils.unregister_class(VariableNode)
    bpy.utils.unregister_class(IfelseNode)
    bpy.utils.unregister_class(ForNode)
    bpy.utils.unregister_class(ForInNode)
    bpy.utils.unregister_class(CallbackInterfaceNode)
    bpy.utils.unregister_class(FunctionDeclarationNode)
    bpy.utils.unregister_class(GlobalVariableDeclarationNode)

if __name__ == "__main__":
    register()
