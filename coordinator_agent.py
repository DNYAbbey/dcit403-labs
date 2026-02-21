import asyncio
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class RiskBehaviour(CyclicBehaviour):

    async def run(self):
        msg = await self.receive(timeout=10)

        if msg:
            performative = msg.get_metadata("performative")
            sender = str(msg.sender)

            # -------------------------
            # CASE 1: Rainfall from Sensor
            # -------------------------
            if performative == "inform" and sender.startswith("sensor"):
                
                try:
                    rainfall = int(msg.body)
                    print(f"[RECEIVE] Rainfall: {rainfall}mm")

                    if rainfall > 120:
                        severity = "CRITICAL"
                    elif rainfall > 80:
                        severity = "HIGH"
                    else:
                        return  # No emergency

                    request = Message(
                        to="rescue-agent1@xmpp.jp",
                        body=f"Flood severity {severity}"
                    )
                    request.set_metadata("performative", "request")

                    await self.send(request)
                    print(f"[SEND] REQUEST → Rescue ({severity})")

                except ValueError:
                    print("[WARNING] Invalid rainfall data received")

            # CASE 2: Completion from Rescue
            elif performative == "inform" and sender.startswith("rescue"):
                print(f"[RECEIVE] Rescue Update: {msg.body}")

class RiskAssessmentAgent(Agent):
    async def setup(self):
        print("Risk Assessment Agent Started")
        self.add_behaviour(RiskBehaviour())


async def main():
    agent = RiskAssessmentAgent("coordinator_agent1@xmpp.jp", "coord123")
    agent.verify_security = False
    await agent.start()

    while agent.is_alive():
        await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())