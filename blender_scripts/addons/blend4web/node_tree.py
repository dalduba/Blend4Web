__author__ = 'dal'
import bpy
from bpy.types import NodeTree, Node, NodeSocket
from bpy.props import StringProperty

# Implementation of custom nodes from Python


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


# Custom socket type
class MyCustomSocket(NodeSocket):
    # Description string
    '''Custom node socket type'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomSocketType'
    # Label for nice name display
    bl_label = 'Custom Node Socket'

    # Enum items list
    my_items = [
        ("DOWN", "Down", "Where your feet are"),
        ("UP", "Up", "Where your head should be"),
        ("LEFT", "Left", "Not right"),
        ("RIGHT", "Right", "Not left")
    ]

    myEnumProperty = bpy.props.EnumProperty(name="Direction", description="Just an example", items=my_items, default='UP')

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text)
        else:
            layout.prop(self, "myEnumProperty", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)


# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class B4WLogicNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'B4WLogicNodeTreeType'


# Derived from the Node base type.
class MyCustomNode(Node, B4WLogicNode):
    # === Basics ===
    # Description string
    '''A custom node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomNodeType'
    # Label for nice name display
    bl_label = 'Custom Node'
    # Icon identifier
    bl_icon = 'SOUND'

    # === Custom Properties ===
    # These work just like custom properties in ID data blocks
    # Extensive information can be found under
    # http://wiki.blender.org/index.php/Doc:2.6/Manual/Extensions/Python/Properties
    myStringProperty = bpy.props.StringProperty()
    myFloatProperty = bpy.props.FloatProperty(default=3.1415926)

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    # This is the most common place to create the sockets for a node, as shown below.
    # NOTE: this is not the same as the standard __init__ function in Python, which is
    #       a purely internal Python method and unknown to the node system!
    def init(self, context):
        self.inputs.new('CustomSocketType', "Hello")
        self.inputs.new('NodeSocketFloat', "World")
        self.inputs.new('NodeSocketVector', "!")

        self.outputs.new('NodeSocketColor', "How")
        self.outputs.new('NodeSocketColor', "are")
        self.outputs.new('NodeSocketFloat', "you")

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.label("Node settings")
        layout.prop(self, "myFloatProperty")

    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "myFloatProperty")
        # myStringProperty button will only be visible in the sidebar
        layout.prop(self, "myStringProperty")

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        return "I am a custom node"

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
        return (1.0, 0.4, 0.216, 0.5)


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
        if self.is_output or self.is_linked:
            # layout.prop(self, "ObjectsProperty", text=text)
            pass
        else:
            layout.label(text)

    def draw_color(self, context, node):
        return (0.0, 1.0, 0.216, 0.5)


class TargetNode(Node, B4WLogicNode):
    def updateNode(self, context):
        self.process_node(context)

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
        return (0.0, 1.0, 0.216, 0.5)


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
        self.inputs.new('TargetSocketType', "")
        self.inputs.new('SensorSocketType', "")

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
        return (0.0, 1.0, 0.216, 0.5)

class LogicOperatorSocketOutput(NodeSocket):
    bl_idname = 'LogicOperatorSocketOutputType'
    bl_label = 'LogicOperator Node Socket'
    def draw(self, context, layout, node, text):
        pass

    def draw_color(self, context, node):
        return (0.0, 1.0, 0.216, 0.5)
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
        self.inputs.new('LogicOperatorSocketInputType', "")
        self.inputs.new[-1].logic_operation = self.logic_operation
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
        NodeItem("SensorNode", label="Sensor", settings={
            "myStringProperty": repr("Lorem ipsum dolor sit amet"),
            "myFloatProperty": repr(1.0),
            }),
        NodeItem("LogicOperatorNode", label="LogicOperator",),
        ]),
    MyNodeCategory("Targets", "Targets", items=[
        NodeItem("TargetNode", label="Target",),
        # the node item can have additional settings,
        # which are applied to new nodes
        # NB: settings values are stored as string expressions,
        # for this reason they should be converted to strings using repr()
        NodeItem("CustomNodeType", label="Node A", settings={
            "myStringProperty": repr("Lorem ipsum dolor sit amet"),
            "myFloatProperty": repr(1.0),
            }),
        NodeItem("CustomNodeType", label="Node B", settings={
            "myStringProperty": repr("consectetur adipisicing elit"),
            "myFloatProperty": repr(2.0),
            }),
        ]),
    MyNodeCategory("Callbacks", "Callbacks", items=[
        # our basic node
        NodeItem("FunctionNode", label="Function",),
        ]),
    ]


def register():
    bpy.utils.register_class(B4WLogicNodeTree)
    bpy.utils.register_class(MyCustomSocket)
    bpy.utils.register_class(SensorSocket)
    bpy.utils.register_class(MyCustomNode)
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

    nodeitems_utils.register_node_categories("CUSTOM_NODES", node_categories)


def unregister():
    nodeitems_utils.unregister_node_categories("CUSTOM_NODES")

    bpy.utils.unregister_class(B4WLogicNodeTree)
    bpy.utils.unregister_class(MyCustomSocket)
    bpy.utils.unregister_class(SensorSocket)
    bpy.utils.unregister_class(MyCustomNode)
    bpy.utils.unregister_class(TargetNode)
    bpy.utils.unregister_class(TargetSocket)
    bpy.utils.unregister_class(FunctionNode)
    bpy.utils.unregister_class(FunctionSocket)
    bpy.utils.unregister_class(LogicOperatorNode)
    bpy.utils.unregister_class(LogicOperatorSocketInput)
    bpy.utils.unregister_class(LogicOperatorSocketOutput)
    bpy.utils.unregister_class(AddSocket)
    bpy.utils.unregister_class(RemoveSocket)

if __name__ == "__main__":
    register()