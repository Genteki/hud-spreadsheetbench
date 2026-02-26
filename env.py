"""SWE-Bench HUD Environment"""

import logging
import sys
import logging
from hud import Environment
from tools import JupyterTool
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

__all__ = ["env"]

@env.initialize
async def initialize_environment():
    """Initialize the environment."""
    global jupyter_tool
    logger.info("Initializing jupyter environment")

    # Create tool (kernel will be created on first use)
    jupyter_tool = JupyterTool(url_suffix="localhost:8888", kernel_name="python3")
    env.add_tool(jupyter_tool)

    # Ensure kernel is started and register it for reuse
    await jupyter_tool._ensure_kernel()
    JupyterTool.register_shared_kernel("SpreadSheetBench", jupyter_tool._kernel_id)

if __name__ == "__main__":
    sys.modules["env"] = sys.modules[__name__]
    env.run(transport="stdio")
