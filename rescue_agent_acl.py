import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class RescueBehaviour(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)

        if msg:
            print(f"[RESCUE] {msg.body}")

            if msg.get_metadata("performative") == "request":
                print("[RESCUE] Deploying team...")
                await asyncio.sleep(5)

                inform = Message(
                    to=str(msg.sender),
                    body="Flood emergency resolved"
                )
                inform.set_metadata("performative", "inform")
                await self.send(inform)

                print("[RESCUE] INFORM sent (completed)")


class RescueAgent(Agent):
    async def setup(self):
        print("Rescue Agent Started")
        self.add_behaviour(RescueBehaviour())


async def main():
    agent = RescueAgent("rescue-agent1@xmpp.jp", "rescue123")
    agent.verify_security = False
    await agent.start()

    while agent.is_alive():
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())