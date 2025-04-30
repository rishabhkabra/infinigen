import bpy

from infinigen.assets.objects.creatures.util.creature import PartFactory


class HumanArm(PartFactory):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def create_part(self):
        # Create a simple cylinder for the arm
        bpy.ops.mesh.primitive_cylinder_add(radius=0.2, depth=2)
        arm = bpy.context.active_object
        arm.name = "HumanArm"
        return arm 