import asyncio
import time
from datetime import datetime
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from environment import DisasterEnvironment
from spade.message import Message

class SensorBehaviour(CyclicBehaviour):
    async def run(self):
        event = self.agent.env.sense_environment()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] Event: {event['event']}, Severity: {event['severity']}"
        print(log_entry)
        with open("event_log.txt", "a") as file:
            file.write(log_entry + "\n")
        await asyncio.sleep(5)

         # -------- NEW PART (Lab 3 & 4) --------
        msg = Message(to="coordinator_agent1@xmpp.jp")
        msg.set_metadata("performative", "inform")
        msg.body = f"Disaster severity {event['severity']}"


        await self.send(msg)
        print(f"[SENT] INFORM -> {event['severity']}")

        await asyncio.sleep(5)


class SensorAgent(Agent):
    async def setup(self):
        print("SensorAgent started.")
        self.env = DisasterEnvironment()
        self.add_behaviour(SensorBehaviour())


async def main():
    agent = SensorAgent("sensor_agent1@xmpp.jp", "sensor123")
    
    try:
        await agent.start()  # User already exists
        print("✓ Agent started!\n")
        
        while agent.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        if agent.is_alive():
            await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())