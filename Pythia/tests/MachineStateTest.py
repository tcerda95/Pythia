import context
import Condition
import unittest
from MachineState import MachineState
from WorldState import WorldState
from Trigger import Trigger
from Condition import *


class TestMachineState(unittest.TestCase):
    def setUp(self):
        self.machineState = MachineState('initialState')
        self.worldState = WorldState()
        self.actionRun = False

    def action(self):
        self.actionRun = True

    def testInit(self):
        self.assertEqual('initialState', self.machineState.state)
        self.assertEqual({'initialState'}, self.machineState.stateSet)
        self.assertEqual({}, self.machineState.transitions)

    def testAddTransition(self):
        self.machineState.addTransition('initialState', 'secondState', Trigger.mayBeNear, self.action)
        self.machineState.addTransition('secondState', 'initialState', Trigger.mayBeNear, self.action)

        self.assertEqual('initialState', self.machineState.state)
        self.assertEqual({'initialState', 'secondState'}, self.machineState.stateSet)
        self.assertEqual(2, len(self.machineState.transitions))

    def testTransition(self):
        self.machineState.addTransition('initialState', 'secondState', Trigger.mayBeNear, self.action)

        self.machineState.run(Trigger.isNear, self.worldState) # not registered trigger

        self.assertEqual('initialState', self.machineState.state)
        self.assertFalse(self.actionRun)
        self.assertEqual(Trigger.isNear, self.worldState.proximity)

        self.machineState.run(Trigger.mayBeNear, self.worldState) # registered trigger

        self.assertEqual('secondState', self.machineState.state)
        self.assertTrue(self.actionRun)
        self.assertEqual(Trigger.mayBeNear, self.worldState.proximity)

    def testTransitionWithCondition(self):
        self.machineState.addTransition('initialState', 'secondState', Trigger.talking, self.action)
        self.machineState.addTransition('secondState', 'thirdState', Trigger.mayBeNear, self.action, 
            allCondition([soundCondition(Trigger.talking), proximityCondition(Trigger.mayBeNear)]))
        
        self.machineState.run(Trigger.talking, self.worldState)
        self.actionRun = False
        self.machineState.run(Trigger.mayBeNear, self.worldState)

        self.assertEqual('thirdState', self.machineState.state)
        self.assertTrue(self.actionRun)


if __name__ == '__main__':
    unittest.main()
