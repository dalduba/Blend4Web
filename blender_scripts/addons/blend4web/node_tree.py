__author__ = 'dal'
import bpy
from bpy.types import NodeTree, Node, NodeSocket
from bpy.props import StringProperty

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

class RemoveSocket(bpy.types.Operator):
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
class AddSocket(bpy.types.Operator):
    bl_idname = "node.add_socket"
    bl_label = "add socket"
    bl_options = {'REGISTER', 'UNDO'}
    node_name = StringProperty(name='name node', description='it is name of node',
                               default='')
    tree_name = StringProperty(name='name tree', description='it is name of tree',
                               default='')
    def execute(self, context):
        global ID
        inputs = bpy.data.node_groups[self.tree_name].nodes[self.node_name].inputs
        s = inputs.new('LogicOperatorSocketInputType', "socket_%s" % ID)
        ID += 1
        s.node_name = self.node_name
        s.tree_name = self.tree_name
        s.logic_operation = bpy.data.node_groups[self.tree_name].nodes[self.node_name].logic_operation
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
            opera = row.operator('node.add_socket', text="Add input")
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
        NodeItem("LogicOperatorNode", label="LogicOperator",),
        ]),
    MyNodeCategory("Targets", "Targets", items=[
        NodeItem("TargetNode", label="Target",),

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
    ]


def register():
    bpy.utils.register_class(B4WLogicNodeTree)
    bpy.utils.register_class(SensorSocket)
    bpy.utils.register_class(SensorNode)
    bpy.utils.register_class(TargetNode)
    bpy.utils.register_class(TargetSocket)
    bpy.utils.register_class(FunctionNode)
    bpy.utils.register_class(FunctionSocket)
    bpy.utils.register_class(LogicOperatorNode)
    bpy.utils.register_class(LogicOperatorSocketInput)
    bpy.utils.register_class(LogicOperatorSocketOutput)
    bpy.utils.register_class(AddSocket)
    bpy.utils.register_class(RemoveSocket)
    bpy.utils.register_class(FunctionNodeSensorSocket)
    bpy.utils.register_class(FunctionNodeTargetSocket)
    bpy.utils.register_class(OrderSocket)
    bpy.utils.register_class(BoolSocket)
    bpy.utils.register_class(IfelseNode)
    bpy.utils.register_class(ForNode)
    bpy.utils.register_class(ForInNode)
    bpy.utils.register_class(DataSocket)
    bpy.utils.register_class(CallbackInterfaceNode)



    nodeitems_utils.register_node_categories("CUSTOM_NODES", node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories("CUSTOM_NODES")

    bpy.utils.unregister_class(B4WLogicNodeTree)
    bpy.utils.unregister_class(SensorSocket)
    bpy.utils.unregister_class(TargetNode)
    bpy.utils.unregister_class(TargetSocket)
    bpy.utils.unregister_class(FunctionNode)
    bpy.utils.unregister_class(FunctionSocket)
    bpy.utils.unregister_class(LogicOperatorNode)
    bpy.utils.unregister_class(LogicOperatorSocketInput)
    bpy.utils.unregister_class(LogicOperatorSocketOutput)
    bpy.utils.unregister_class(AddSocket)
    bpy.utils.unregister_class(RemoveSocket)
    bpy.utils.unregister_class(FunctionNodeSensorSocket)
    bpy.utils.unregister_class(FunctionNodeTargetSocket)
    bpy.utils.unregister_class(OrderSocket)
    bpy.utils.unregister_class(BoolSocket)
    bpy.utils.unregister_class(IfelseNode)
    bpy.utils.unregister_class(ForNode)
    bpy.utils.unregister_class(ForInNode)
    bpy.utils.unregister_class(DataSocket)
    bpy.utils.unregister_class(CallbackInterfaceNode)

if __name__ == "__main__":
    register()