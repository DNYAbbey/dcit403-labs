import asyncio
import random
from datetime import datetime
from spade.agent import Agent
from spade.behaviour import FSMBehaviour, State


# Flood Event Model

class FloodEvent:
    def __init__(self, location, severity):
        self.location = location
        self.severity = severity
        self.timestamp = datetime.now()

    def __str__(self):
        return f"Flood at {self.location} | Severity: {self.severity}"


# FSM STATES

class IdleState(State):
    async def run(self):
        print("[IDLE] Monitoring weather and water levels...")
        await asyncio.sleep(3)

        # Simulate water level changes
        severity = random.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])

        if severity in ["HIGH", "CRITICAL"]:
            event = FloodEvent("River_Basin_A", severity)
            self.agent.current_event = event
            print(f"[RISK] {event}")
            self.set_next_state("RESPONDING")
        else:
            print("[SAFE] No emergency detected.")
            self.set_next_state("IDLE")


class RespondingState(State):
    async def run(self):
        event = self.agent.current_event
        print(f"[RESPONDING] Deploying to {event.location}")
        await asyncio.sleep(3)
        print("[ARRIVED]")
        self.set_next_state("RESCUING")


class RescuingState(State):
    async def run(self):
        event = self.agent.current_event
        print(f"[RESCUING] Managing flood (Severity: {event.severity})")

        severity_time = {
            "HIGH": 5,
            "CRITICAL": 8
        }

        await asyncio.sleep(severity_time.get(event.severity, 5))

        print("[RESCUE COMPLETE]")
        self.agent.rescues_completed += 1
        self.set_next_state("REPORTING")


class ReportingState(State):
    async def run(self):
        print("[REPORT] Flood emergency handled successfully.")
        await asyncio.sleep(2)
        self.agent.current_event = None
        self.set_next_state("IDLE")


# Rescue Agent

class FloodRescueAgent(Agent):

    async def setup(self):
        print("Flood Rescue Agent Started")
        self.current_event = None
        self.rescues_completed = 0

        fsm = FSMBehaviour()

        fsm.add_state(name="IDLE", state=IdleState(), initial=True)
        fsm.add_state(name="RESPONDING", state=RespondingState())
        fsm.add_state(name="RESCUING", state=RescuingState())
        fsm.add_state(name="REPORTING", state=ReportingState())

        fsm.add_transition("IDLE", "IDLE")
        fsm.add_transition("IDLE", "RESPONDING")
        fsm.add_transition("RESPONDING", "RESCUING")
        fsm.add_transition("RESCUING", "REPORTING")
        fsm.add_transition("REPORTING", "IDLE")

        self.add_behaviour(fsm)


async def main():
    agent = FloodRescueAgent("rescue-agent1@xmpp.jp", "rescue123")
    agent.verify_security = False

    await agent.start()

    while agent.is_alive():
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())