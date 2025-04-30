import gin
import numpy as np
from numpy.random import normal as N
from numpy.random import uniform as U

from infinigen.assets.objects.creatures.util import creature, genome, joining
from infinigen.assets.objects.creatures.util.genome import Joint, IKParams
from infinigen.core.placement.factory import AssetFactory
from infinigen.core.util import blender as butil
from infinigen.core.util.math import clip_gaussian


def human_genome():
    # Define the body
    body_fac = parts.generic_nurbs.NurbsBody(
        prefix="body_human", tags=["body"], var=U(0.3, 1)
    )
    body = genome.part(body_fac)
    body_length = body_fac.params["length"][0]

    # Define the head with animation parameters
    head_fac = parts.head.HumanHead()
    head = genome.part(head_fac)
    # Add IK parameters for head movement
    head.iks = {
        1.0: IKParams(
            "head", 
            rotation_weight=0.1,
            chain_length=1,
            bounds=np.array([[-45, -45, -45], [45, 45, 45]])  # Rotation limits in degrees
        )
    }
    # Add joint constraints for natural head movement
    head.joints = {
        0: Joint(
            rest=(0, 0, 0),
            bounds=np.array([[-45, -45, -45], [45, 45, 45]])  # Rotation limits in degrees
        )
    }
    genome.attach(
        head, 
        body, 
        coord=(1, 0, 0), 
        joint=Joint(
            rest=(0, 0, 0),
            bounds=np.array([[-45, -45, -45], [45, 45, 45]])  # Rotation limits in degrees
        )
    )

    # Define the arms
    arm_fac = parts.arm.HumanArm()
    for side in [-1, 1]:
        arm = genome.part(arm_fac)
        genome.attach(
            arm, body, coord=(0.5, side * 0.5, 0.5), joint=Joint(rest=(0, 0, 0))
        )

    # Define the legs
    leg_fac = parts.leg.HumanLeg()
    for side in [-1, 1]:
        leg = genome.part(leg_fac)
        genome.attach(
            leg, body, coord=(0.5, side * 0.5, 0), joint=Joint(rest=(0, 0, 0))
        )

    return genome.CreatureGenome(
        parts=body,
        postprocess_params=dict(
            animation=dict(
                head_movement=dict(
                    freq=0.5,  # Frequency of head movements
                    amplitude=30,  # Maximum rotation angle in degrees
                    smoothness=0.8,  # How smooth the movement should be
                )
            ),
            hair=None,  # Add human hair parameters here if needed
            surface_registry=[],  # Add human-specific materials here
        ),
    )


@gin.configurable
class HumanFactory(AssetFactory):
    def __init__(self, factory_seed=None, coarse=False, **kwargs):
        super().__init__(factory_seed, coarse)

    def create_asset(self, i, **kwargs):
        genome = human_genome()
        root, parts = creature.genome_to_creature(
            genome, name=f"human({self.factory_seed}, {i})"
        )
        joined, extras, arma, ik_targets = joining.join_and_rig_parts(
            root, parts, genome, **kwargs
        )
        return root 