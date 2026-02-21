import asyncio
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State

class Monitoring(State):
    async def run(self):
        print("State: Monitoring")
        await asyncio.sleep(2)
        print("Event: Fire Detected")
        self.set_next_state("RESPONDING")
        
class Responding(State):
    async def run(self):
        print("State: Responding")
        await asyncio.sleep(2)
        print("Arrived at scene")
        self.set_next_state("ASSISTING")
        
class Assisting(State):
    async def run(self):
        print("State: Assisting")
        await asyncio.sleep(2)
        print("Fire extinguished")
        self.set_next_state("REPORTING")
        
class Reporting(State):
    async def run(self):
        print("State: Reporting")
        await asyncio.sleep(2)
        print("Report sent to command center")
        self.set_next_state("MONITORING")

class Charging(State):
    async def run(self):
        print("State: Charging")
        await asyncio.sleep(2)
        print("Battery fully charged")
        self.set_next_state("MONITORING")
        
class FireAlarmAgent(Agent):
    async def setup(self):
        print("Fire Alarm Agent connected.")
        fsm = FSMBehaviour()
        fsm.add_state(name="MONITORING", state=Monitoring(), initial=True)
        fsm.add_state(name="RESPONDING", state=Responding())
        fsm.add_state(name="ASSISTING", state=Assisting())
        fsm.add_state(name="REPORTING", state=Reporting())
        fsm.add_state(name="CHARGING", state=Charging())

        fsm.add_transition(source="MONITORING", dest="RESPONDING")
        fsm.add_transition(source="RESPONDING", dest="ASSISTING")
        fsm.add_transition(source="ASSISTING", dest="REPORTING")
        fsm.add_transition(source="REPORTING", dest="MONITORING")

        self.add_behaviour(fsm)

async def main():
    agent = FireAlarmAgent("foaduncan@xmpp.jp", "Duncandothis")
    await agent.start(auto_register=True)

    await asyncio.sleep(20)
    await agent.stop()

if __name__ == "__main__":
    asyncio.run(main())