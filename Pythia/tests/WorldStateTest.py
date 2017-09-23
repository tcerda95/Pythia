import context
import unittest
from Trigger import Trigger
from WorldState import WorldState


class TestWorldState(unittest.TestCase):

    def setUp(self):
        self.worldState = WorldState()

    def testInit(self):
        self.assertEqual(Trigger.noOneNear, self.worldState.proximity)
        self.assertEqual(Trigger.silence, self.worldState.sound)

    def testShouldNotUpdate(self):
        newWorldState = WorldState()

        self.worldState.update(Trigger.heartbeat)
        self.worldState.update(Trigger.endTransmit)

        self.assertEqual(newWorldState, self.worldState)

    def testShouldUpdate(self):
        self.worldState.update(Trigger.isNear)
        self.worldState.update(Trigger.talking)

        self.assertEqual(Trigger.isNear, self.worldState.proximity)
        self.assertEqual(Trigger.talking, self.worldState.sound)


if __name__ == '__main__':
    unittest.main()
