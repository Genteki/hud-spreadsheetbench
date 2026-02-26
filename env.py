"""SWE-Bench HUD Environment"""

import sys
import os
import logging
from hud import Environment
from tools import JupyterToolWithRecord
from scenarios import register_spreadsheetbench_all
logger = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stderr,
    level=logging.INFO,
    format="[%(levelname)s] %(name)s | %(message)s",
    force=True,
)

env = Environment("spreadsheetbench")

register_spreadsheetbench_all(env)
@env.initialize
async def initialize_environment():
    global jupyter_tool
    logger.info("Initializing jupyter environment")
    jupyter_tool = JupyterToolWithRecord(kernel_name="python3")
    await jupyter_tool._ensure_kernel()  # force kernel creation
    JupyterToolWithRecord.register_shared_kernel(
        "SpreadSheetBench", jupyter_tool.get_kernel_id()
    )
    env.add_tool(jupyter_tool)


__all__ = ["env"]

if __name__ == "__main__":
    sys.modules["env"] = sys.modules[__name__]
    transport = os.environ.get("MCP_TRANSPORT", "stdio")
    if transport == "http":
        env.run(transport="http", host="0.0.0.0", port=8765, path="/mcp")
    else:
        env.run(transport="stdio")
