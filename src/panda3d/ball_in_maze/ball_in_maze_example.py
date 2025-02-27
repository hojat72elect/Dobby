from direct.showbase.ShowBase import ShowBase
from direct.task.TaskManagerGlobal import taskMgr
from panda3d.core import CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay
from panda3d.core import Material, LRotationf, NodePath
from panda3d.core import AmbientLight, DirectionalLight
from panda3d.core import TextNode
from panda3d.core import LVector3, BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.interval.MetaInterval import Sequence, Parallel
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func, Wait
from direct.task.Task import Task
import sys

# Constants
ACCELERATION = 70  # Acceleration in feet per second^2
MAX_SPEED = 5  # Max speed in feet per second


class BallInMazeExample(ShowBase):

    def __init__(self):
        # Initialize the ShowBase class
        ShowBase.__init__(self)

        self.title = OnscreenText(
            text="Panda3D: Tutorial - Ball in a Maze Game",
            parent=base.a2dBottomRight,
            align=TextNode.ARight,
            fg=(1, 1, 1, 1),
            pos=(-0.1, 0.1),
            scale=.08,
            shadow=(0, 0, 0, 0.5)
        )
        self.instructions = OnscreenText(
            text="Mouse pointer tilts the board",
            parent=base.a2dTopLeft,
            align=TextNode.ALeft,
            pos=(0.05, -0.08),
            fg=(1, 1, 1, 1),
            scale=.06,
            shadow=(0, 0, 0, 0.5)
        )

        self.accept("escape", sys.exit)  # Escape key quits the game

        self.disableMouse()  # Disable default mouse-based camera control.
        camera.setPosHpr(0, 0, 25, 0, -90, 0)  # Position of the camera

        # Load the maze (it'll be a file with the ".egg.pz" extension)
        self.maze = loader.loadModel("models/maze")
        self.maze.reparentTo(render)

        self.walls = self.maze.find("**/wall_collide")  # the collision node for walls (They are already defined in our maze model)

        self.walls.node().setIntoCollideMask(BitMask32.bit(0))  # Walls collide with the ball
        #  Uncomment the next line to see the collision walls
        # self.walls.show()

        # Define 6 holes in the maze
        self.loseTriggers = []
        for i in range(6):
            trigger = self.maze.find(f"**/hole_collide{i}")
            trigger.node().setIntoCollideMask(BitMask32.bit(0)) # holes collide with the ball
            trigger.node().setName("loseTrigger")
            self.loseTriggers.append(trigger)
            # Uncomment this line to see the holes' triggers
            # trigger.show()

        self.mazeGround = self.maze.find("**/ground_collide")
        self.mazeGround.node().setIntoCollideMask(BitMask32.bit(1)) # The ground doesn't collide with the ball

        # Load the ball (Another file with the ".egg.pz" extension)
        self.ballRoot = render.attachNewNode("ballRoot")
        self.ball = loader.loadModel("models/ball")
        self.ball.reparentTo(self.ballRoot)

        # The collision sphere for the ball
        self.ballSphere = self.ball.find("**/ball")
        # the next 2 lines just define the ball as a rigid body which can collide with the other stuff.
        self.ballSphere.node().setFromCollideMask(BitMask32.bit(0))
        self.ballSphere.node().setIntoCollideMask(BitMask32.allOff())

        # The ray that starts from above the ball and towards the ground (in order to understand the tilting of the ground and the gravity it applies to the ball)
        self.ballGravityCollisionRay = CollisionRay()
        self.ballGravityCollisionRay.setOrigin(0, 0, 10)
        self.ballGravityCollisionRay.setDirection(0, 0, -1)

        self.ballGravityCollisionNode = CollisionNode('groundRay')
        self.ballGravityCollisionNode.addSolid(self.ballGravityCollisionRay)  # Add the ray
        self.ballGravityCollisionNode.setFromCollideMask(BitMask32.bit(1))
        self.ballGravityCollisionNode.setIntoCollideMask(BitMask32.allOff())

        self.ballGravityCollisionNodePath = self.ballRoot.attachNewNode(self.ballGravityCollisionNode)
        # Uncomment next line to see the collision ray
        # self.ballGravityCollisionNodePath.show()

        # CollisionTraverser walks through the scene graph and calculates collisions.
        self.cTrav = CollisionTraverser()

        # Collision traverser gives all the info it has to the collision handler.
        self.cHandler = CollisionHandlerQueue()

        self.cTrav.addCollider(self.ballSphere, self.cHandler)
        self.cTrav.addCollider(self.ballGravityCollisionNodePath, self.cHandler)

        # Uncomment the next line to see the collisions.
        # self.cTrav.showCollisions(render)

        # Ambient lighting and directional lighting for the ball (the maze already has pre-generated lighting from blender model)
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor((0.55, 0.55, 0.55, 1))
        directionalLight = DirectionalLight("directionalLight")
        directionalLight.setDirection(LVector3(0, 0, -1))
        directionalLight.setColor((0.375, 0.375, 0.375, 1))
        directionalLight.setSpecularColor((1, 1, 1, 1))
        self.ballRoot.setLight(render.attachNewNode(ambientLight))
        self.ballRoot.setLight(render.attachNewNode(directionalLight))

        # Material for the ball
        m = Material()
        m.setSpecular((1, 1, 1, 1))
        m.setShininess(96)
        self.ball.setMaterial(m, 1)

        # Finally, we call start for even more initialization
        self.start()

    def start(self):
        # The maze model also has a locator in it for where to start the ball
        startPos = self.maze.find("**/start").getPos()
        # Set the ball in the starting position
        self.ballRoot.setPos(startPos)
        self.ballV = LVector3(0, 0, 0)  # Initial velocity of the ball
        self.accelV = LVector3(0, 0, 0)  # Initial acceleration of the ball

        # first make sure it is not already running
        taskMgr.remove("rollTask")
        self.mainLoop = taskMgr.add(self.rollTask, "rollTask")

    # Handle the collision between the ray and the ground
    def groundCollideHandler(self, colEntry):
        # Update the Z value of the ball so it can be exactly on the ground
        newZ = colEntry.getSurfacePoint(render).getZ()
        self.ballRoot.setZ(newZ + .4)

        # Find the acceleration direction.
        norm = colEntry.getSurfaceNormal(render)
        accelSide = norm.cross(LVector3.up())
        self.accelV = norm.cross(accelSide)

    # Handle the collision between the ball and a wall
    def wallCollideHandler(self, colEntry):
        norm = colEntry.getSurfaceNormal(render) * -1  # The normal of the wall
        curSpeed = self.ballV.length()  # The current speed
        inVec = self.ballV / curSpeed  # The direction of travel
        velAngle = norm.dot(inVec)  # Angle of incidence
        hitDir = colEntry.getSurfacePoint(render) - self.ballRoot.getPos()
        hitDir.normalize()
        # The angle between the ball and the normal
        hitAngle = norm.dot(hitDir)

        """
         Ignore the collision if the ball is either moving away from the wall
         already (so that we don't accidentally send it back into the wall)
         and ignore it if the collision isn't dead-on (to avoid getting caught on
         corners)
        """
        if velAngle > 0 and hitAngle > 0.995:
            # Standard reflection equation
            reflectVec = (norm * norm.dot(inVec * -1) * 2) + inVec

            # This makes the velocity half of what it was if the hit was dead-on and nearly exactly what it was if this was a glancing blow
            self.ballV = reflectVec * (curSpeed * (((1 - velAngle) * .5) + .5))
            # Since we have a collision, the ball is already a little bit buried in
            # the wall. This calculates a vector needed to move it so that it is
            # exactly touching the wall
            disp = (colEntry.getSurfacePoint(render) - colEntry.getInteriorPoint(render))
            newPos = self.ballRoot.getPos() + disp
            self.ballRoot.setPos(newPos)

    # The task that deals with making everything interactive
    def rollTask(self, task):
        # Standard technique for finding the amount of time since the last frame (delta time)
        dt = base.clock.dt

        # If dt is large, then there has been a # hiccup that could cause the ball
        # to leave the field if this functions runs, so ignore the frame
        if dt > .2:
            return Task.cont

        # The collision handler collects the collisions. We dispatch which function
        # to handle the collision based on the name of what was collided into
        for i in range(self.cHandler.getNumEntries()):
            entry = self.cHandler.getEntry(i)
            name = entry.getIntoNode().getName()
            if name == "wall_collide":
                self.wallCollideHandler(entry)
            elif name == "ground_collide":
                self.groundCollideHandler(entry)
            elif name == "loseTrigger":
                self.loseGame(entry)

        # Read the mouse position and tilt the maze accordingly
        if base.mouseWatcherNode.hasMouse():
            mpos = base.mouseWatcherNode.getMouse()  # get the mouse position
            self.maze.setP(mpos.getY() * -10)
            self.maze.setR(mpos.getX() * 10)

        # Finally, we move the ball
        # Update the velocity based on acceleration
        self.ballV += self.accelV * dt * ACCELERATION
        # Clamp the velocity to the maximum speed
        if self.ballV.lengthSquared() > MAX_SPEED ** 2:
            self.ballV.normalize()
            self.ballV *= MAX_SPEED
        # Update the position based on the velocity
        self.ballRoot.setPos(self.ballRoot.getPos() + (self.ballV * dt))

        # This block of code rotates the ball. It uses something called a quaternion
        # to rotate the ball around an arbitrary axis. That axis perpendicular to
        # the balls rotation, and the amount has to do with the size of the ball
        # This is multiplied on the previous rotation to incrimentally turn it.
        prevRot = LRotationf(self.ball.getQuat())
        axis = LVector3.up().cross(self.ballV)
        newRot = LRotationf(axis, 45.5 * dt * self.ballV.length())
        self.ball.setQuat(prevRot * newRot)

        return Task.cont  # Continue the task indefinitely

    # If the ball hits a hole trigger, then it should fall in the hole.
    # This is faked rather than dealing with the actual physics of it.
    def loseGame(self, entry):
        # The triggers are set up so that the center of the ball should move to the
        # collision point to be in the hole
        toPos = entry.getInteriorPoint(render)
        taskMgr.remove('rollTask')  # Stop the maze task

        # Move the ball into the hole over a short sequence of time. Then wait a
        # second and call start to reset the game
        Sequence(
            Parallel(
                LerpFunc(self.ballRoot.setX, fromData=self.ballRoot.getX(),
                         toData=toPos.getX(), duration=.1),
                LerpFunc(self.ballRoot.setY, fromData=self.ballRoot.getY(),
                         toData=toPos.getY(), duration=.1),
                LerpFunc(self.ballRoot.setZ, fromData=self.ballRoot.getZ(),
                         toData=self.ballRoot.getZ() - .9, duration=.2)),
            Wait(1),
            Func(self.start)).start()


if __name__ == '__main__':
    BallInMazeExample().run()
