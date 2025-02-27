from math import pi, sin, cos

from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3
from panda3d.core import NodePath


class PandaWalkExample(ShowBase):
    """
    Shows a panda walking in a glade. And the camera spins around it.
    """

    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()  # Disable mouse control over camera

        self.scene: NodePath = self.loader.loadModel("models/environment")  # An internal model of the engine
        self.scene.reparentTo(self.render)
        self.scene.setScale(0.25, 0.25, 0.25)
        self.scene.setPos(-8, 42, 0)

        # Add the spinCameraTask procedure to the task manager (so the camera will be spinning).
        self.taskMgr.add(self.spinCamera, "SpinCameraTask")

        # Load the Panda model and attach the "walk" animation to it.
        self.pandaActor = Actor("models/panda-model", {"walk": "models/panda-walk4"})
        self.pandaActor.setScale(0.005, 0.005, 0.005)
        self.pandaActor.reparentTo(self.render)

        self.pandaActor.loop("walk")

        # Create the four lerp intervals needed for the panda to walk back and forth.
        posInterval1 = self.pandaActor.posInterval(13, Point3(0, -10, 0), startPos=Point3(0, 10, 0))
        posInterval2 = self.pandaActor.posInterval(13, Point3(0, 10, 0), startPos=Point3(0, -10, 0))
        hprInterval1 = self.pandaActor.hprInterval(3, Point3(180, 0, 0), startHpr=Point3(0, 0, 0))
        hprInterval2 = self.pandaActor.hprInterval(3, Point3(0, 0, 0), startHpr=Point3(180, 0, 0))

        # Create and play the sequence that coordinates the intervals.
        self.pandaPace = Sequence(posInterval1, hprInterval1, posInterval2, hprInterval2, name="pandaPace")
        self.pandaPace.loop()

    def spinCamera(self, task) -> int:
        angleDegrees = task.time * 6.0
        angleRadians = angleDegrees * (pi / 180.0)
        self.camera.setPos(20 * sin(angleRadians), -20 * cos(angleRadians), 3)
        self.camera.setHpr(angleDegrees, 0, 0)
        return Task.cont


if __name__ == '__main__':
    PandaWalkExample().run()
