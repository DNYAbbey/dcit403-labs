from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
import asyncio

class HelloBehaviour(CyclicBehaviour):
    async def run(self):
        print(f"[{self.agent.jid}] Agent is running...")
        await asyncio.sleep(5)

class BasicAgent(Agent):
    async def setup(self):
        print(f"[{self.jid}] Agent starting...")
        self.add_behaviour(HelloBehaviour())

async def main():
    agent = BasicAgent("basic_agent1@xmpp.jp", "password123")
    await agent.start()

    try:
        while agent.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        await agent.stop()


if __name__ == "__main__":
    asyncio.run(main())

