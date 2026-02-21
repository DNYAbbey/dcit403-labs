import asyncio
import random
from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message


class WeatherBehaviour(PeriodicBehaviour):
    async def run(self):
        rainfall = random.randint(0, 200)

        msg = Message(
            to="coordinator_agent1@xmpp.jp",
            body=str(rainfall)
        )
        msg.set_metadata("performative", "inform")

        await self.send(msg)
        print(f"[SENSOR] Rainfall detected: {rainfall}mm")


class WeatherSensorAgent(Agent):
    async def setup(self):
        print("Weather Sensor Agent Started")
        self.add_behaviour(WeatherBehaviour(period=8))


async def main():
    agent = WeatherSensorAgent("sensor_agent1@xmpp.jp", "sensor123")
    agent.verify_security = False
    await agent.start()

    while agent.is_alive():
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())