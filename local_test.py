"""Local testing for SpreadsheetBench.

Start the dev server first:  hud dev env:env
Then run:                     python local_test.py
"""

import asyncio
import os
import logging

import hud
from hud import Environment
from hud.agents import create_agent

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(name)s | %(message)s")

DEV_URL = os.getenv("HUD_DEV_URL", "http://localhost:8765/mcp")
MODEL = "claude-sonnet-4-5"

env = Environment("spreadsheetbench")
env.connect_url(DEV_URL)

async def test_spreadsheetbench():
    """Test the solve scenario with an agent."""
    print("\n=== Test: SpreadsheetBench ===")

    async with env:
        task = env("spreadsheetbench", id="59196", instruction="I need a formula to determine which column contains the highest value in a row, and then return the heading of that column. My Excel sheet example is attached.", spreadsheet_path="spreadsheet/59196", instruction_type="Cell-Level Manipulation", answer_position="H3:H5")
        async with hud.eval(task, trace=True) as ctx:
            agent = create_agent(model=MODEL)
            await agent.run(ctx, max_steps=70)
            print(f"Reward: {ctx.reward}")
            print(f"Resolved: {ctx.reward == 1.0}")


if __name__ == "__main__":
    asyncio.run(test_spreadsheetbench())
