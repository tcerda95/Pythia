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
        self.assertEqual(0, self.worldState.heartbeatCount)

    def testShouldNotUpdate(self):
        newWorldState = WorldState()

        self.worldState.update(Trigger.endTransmit)

        self.assertEqual(newWorldState, self.worldState)

    def testShouldUpdate(self):
        self.worldState.update(Trigger.isNear)
        self.worldState.update(Trigger.talking)
        self.worldState.update(Trigger.heartbeat)

        self.assertEqual(Trigger.isNear, self.worldState.proximity)
        self.assertEqual(Trigger.talking, self.worldState.sound)
        self.assertEqual(1, self.worldState.heartbeatCount)

    def testHeartbeatReset(self):
        self.assertEqual(0, self.worldState.heartbeatCount)

        self.worldState.update(Trigger.heartbeat)

        self.assertEqual(1, self.worldState.heartbeatCount)

        self.worldState.update(Trigger.endTransmit)

        self.assertEqual(0, self.worldState.heartbeatCount)


if __name__ == '__main__':
    unittest.main()
