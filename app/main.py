#!/usr/bin/env python3

# micro-ROS Agent Extension Python backend
# Implements these features required by the index.html frontend:
# - Save the micro-ROS Agent settings
# - Get the micro-ROS Agent settings including last used settings
# - Save/get the micro-ROS Agent enabled state (persistent across restarts)
# - "Run" button to enable the micro-ROS Agent
# - Status endpoint to check if the micro-ROS Agent is currently running

import logging.handlers
import sys
import asyncio

from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import Query
from typing import Dict, Any

# Import the local modules
from app import settings

# Configure console logging
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(console_formatter)

# Create logger
logger = logging.getLogger("micro_ros_agent")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)

app = FastAPI()


# Global exception handler to ensure all errors return JSON
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception in {request.url}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": f"Internal server error: {str(exc)}",
            "error": "Internal server error",
        },
    )


# Global variables
micro_ros_agent_running = False  # True if the micro-ROS Agent is currently running
micro_ros_agent = None

# log that the backend has started
logger.info("micro-ROS Agent backend started")


# Auto-start the micro-ROS Agent if it was previously enabled
async def startup_auto_restart():
    """Check if the micro-ROS Agent was previously enabled and auto-restart if needed"""

    # logging prefix for all messages from this function
    logging_prefix_str = "micro_ros_agent:"

    try:
        enabled = settings.get_micro_ros_agent_enabled()
        if enabled:
            logger.info(f"{logging_prefix_str} auto-restarting")

            # call startup function in a background thread
            asyncio.create_task(start_micro_ros_agent_internal())

    except Exception as e:
        logger.error(f"{logging_prefix_str} error during auto-restart: {str(e)}")


# Internal function to start the micro-ROS Agent
async def start_micro_ros_agent_internal():
    """Internal function to start the micro-ROS Agent"""
    global micro_ros_agent_running
    global micro_ros_agent

    # logging prefix for all messages from this function
    logging_prefix_str = "micro_ros_agent:"

    try:
        logger.info(f"{logging_prefix_str} starting...")
        micro_ros_agent_running = True

        # Get settings
        transport = settings.get_micro_ros_agent_transport()
        port = settings.get_micro_ros_agent_port()
        verbose = settings.get_micro_ros_agent_verbose()

        # if micro_ros_agent is None:
        #     micro_ros_agent = micro_ros_agent_process.Agent(
        #         transport, port, verbose
        #     )

        # update settings
        # micro_ros_agent.transport = transport
        # micro_ros_agent.port = port
        # micro_ros_agent.verbose = verbose

        # start
        # micro_ros_agent.start()

        # log settings used
        logger.info(
            f"{logging_prefix_str} "
            f"transport: {transport}, "
            f"port: {port}, "
            f"verbose:{verbose}, "
        )

    except Exception as e:
        logger.error(f"{logging_prefix_str} error {str(e)}")
    finally:
        logger.info(f"{logging_prefix_str} stopped")


# Internal function to stop the micro-ROS Agent
async def stop_micro_ros_agent_internal():
    """Internal function to stop the micro-ROS Agent"""
    global micro_ros_agent_running
    global micro_ros_agent

    # logging prefix for all messages from this function
    logging_prefix_str = "micro_ros_agent:"

    try:
        logger.info(f"{logging_prefix_str} stopping...")
        micro_ros_agent_running = False

        if micro_ros_agent is not None:
            micro_ros_agent.stop()

    except Exception as e:
        logger.error(f"{logging_prefix_str} error {str(e)}")
    finally:
        logger.info(f"{logging_prefix_str} stopped")

# micro-ROS Agent API Endpoints


# Load the micro-ROS Agent settings
@app.post("/micro-ros-agent/get-settings")
async def get_micro_ros_agent_settings() -> Dict[str, Any]:
    """Get saved the micro-ROS Agent settings"""
    logger.debug("Getting the micro-ROS Agent settings")

    try:
        # Get settings
        transport = settings.get_micro_ros_agent_transport()
        port = settings.get_micro_ros_agent_port()
        verbose = settings.get_micro_ros_agent_verbose()

        return {
            "success": True,
            "micro_ros_agent": {
                "transport": transport,
                "port": port,
                "verbose": verbose,
            },
        }
    except Exception as e:
        logger.exception(f"Error getting the micro-ROS Agent settings: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}"}


# Save the micro-ROS Agent settings
@app.post("/micro-ros-agent/save-settings")
async def save_micro_ros_agent_settings(
    transport: str = Query(...),
    port: int = Query(...),
    verbose: str = Query(...),
) -> Dict[str, Any]:
    """Save the micro-ROS Agent settings to persistent storage (using query parameters)"""
    logger.info(
        f"Saving the micro-ROS Agent settings: "
        f"transport={transport}, "
        f"port={port}, "
        f"verbose={verbose}, "
    )

    # Save settings
    transport_success = settings.update_micro_ros_agent_transport(transport)
    port_success = settings.update_micro_ros_agent_port(port)
    verbose_success = settings.update_micro_ros_agent_verbose(verbose)

    if (
        transport_success
        and port_success
        and verbose_success
    ):
        return {"success": True, "message": f"Settings saved"}
    else:
        return {"success": False, "message": "Failed to save some settings"}


# Get the micro-ROS Agent enabled state
@app.get("/micro-ros-agent/get-enabled-state")
async def get_micro_ros_agent_enabled_state() -> Dict[str, Any]:
    """Get saved the micro-ROS Agent enabled state (supports both GET and POST)"""
    logger.debug("Getting the micro-ROS Agent enabled state")

    try:
        enabled = settings.get_micro_ros_agent_enabled()
        return {"success": True, "enabled": enabled}
    except Exception as e:
        logger.exception(f"Error getting the micro-ROS Agent enabled state: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}", "enabled": False}


# Save the micro-ROS Agent enabled state
@app.post("/micro-ros-agent/save-enabled-state")
async def save_micro_ros_agent_enabled_state(enabled: bool = Query(...)) -> Dict[str, Any]:
    """Save the micro-ROS Agent enabled state to persistent storage (using query parameter)"""
    logger.info(f"micro-ROS Agent enabled state: {enabled}")
    success = settings.update_micro_ros_agent_enabled(enabled)

    if success:
        return {"success": True, "message": f"Enabled state saved: {enabled}"}
    else:
        return {"success": False, "message": "Failed to save enabled state"}


# Get the micro-ROS Agent status
@app.get("/micro-ros-agent/status")
async def get_micro_ros_agent_status() -> Dict[str, Any]:
    """Get the micro-ROS Agent status"""
    logger.debug("Getting the micro-ROS Agent status")

    try:
        return {
            "success": True,
            "running": micro_ros_agent_running,
            "message": "Running" if micro_ros_agent_running else "Stopped",
        }
    except Exception as e:
        logger.exception(f"Error getting the micro-ROS Agent status: {str(e)}")
        return {"success": False, "message": f"Error: {str(e)}", "running": False}


# Start the micro-ROS Agent (this is called by the frontend's "Run" button)
@app.post("/micro-ros-agent/start")
async def start_micro_ros_agent() -> Dict[str, Any]:
    """Start the micro-ROS Agent"""
    logger.info(f"Start the micro-ROS Agent request received")

    try:
        if micro_ros_agent_running:
            return {"success": False, "message": "the micro-ROS Agent is already running"}

        # Start the micro-ROS Agent
        asyncio.create_task(start_micro_ros_agent_internal())

        # Wait a few seconds to catch immediate failures
        await asyncio.sleep(2)

        # Check if it's actually running now
        if micro_ros_agent_running:
            return {
                "success": True,
                "message": f"the micro-ROS Agent started successfully",
            }
        else:
            return {
                "success": False,
                "message": "the micro-ROS Agent failed to start (check logs for details)",
            }

    except Exception as e:
        logger.exception(f"Error starting the micro-ROS Agent: {str(e)}")
        return {"success": False, "message": f"Failed to start: {str(e)}"}


# Stop the micro-ROS Agent (this is called by the frontend's "Stop" button)
@app.post("/micro-ros-agent/stop")
async def stop_micro_ros_agent() -> Dict[str, Any]:
    """Stop the micro-ROS Agent"""
    global micro_ros_agent_running

    logger.info("Stop the micro-ROS Agent request received")

    try:

        # Stop the micro-ROS Agent
        asyncio.create_task(stop_micro_ros_agent_internal())

        # Wait a few seconds to catch immediate failures
        await asyncio.sleep(2)

        # Check if it's stopped
        if not micro_ros_agent_running:
            return {
                "success": True,
                "message": f"the micro-ROS Agent stopped successfully",
            }
        else:
            return {
                "success": False,
                "message": "the micro-ROS Agent failed to stop (check logs for details)",
            }

    except Exception as e:
        logger.exception(f"Error stopping the micro-ROS Agent: {str(e)}")
        return {"success": False, "message": f"Failed to stop: {str(e)}"}


# Initialize auto-restart task
@app.on_event("startup")
async def on_startup():
    """Application startup event handler"""
    await startup_auto_restart()


# Mount static files AFTER defining API routes
# Use absolute path to handle Docker container environment
static_dir = Path(__file__).parent / "static"
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

# Set up logging for the app
log_dir = Path("./logs")  # Use local logs directory instead of /app/logs
log_dir.mkdir(parents=True, exist_ok=True)
fh = logging.handlers.RotatingFileHandler(
    log_dir / "lumber.log", maxBytes=2**16, backupCount=1
)
logger.addHandler(fh)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=9133)
