#!/usr/bin/env python3

# Manage micro-ROS Agent settings

import json
import os
import logging
from pathlib import Path

logger = logging.getLogger("micro_ros_agent.settings")

# Settings file path - stored in the extension's persistent storage directory
SETTINGS_FILE = Path("/app/settings/micro-ros-agent-settings.json")

# Default micro-ROS agent settings
# enabled:              false
# transport:            udp4
# port:                 2019
# verbose:              4

DEFAULT_SETTINGS = {
    "micro_ros_agent": {
        "enabled": False,
        "transport": "udp4",
        "port": "2019",
        "verbose": "4",
    },
}


# get the dictionary of settings from the settings file
def get_settings():
    """
    Load settings from the settings file.
    Creates default settings file if it doesn't exist.

    Returns:
        dict: The settings dictionary
    """
    try:
        if not SETTINGS_FILE.exists():
            logger.info(f"Settings file not found, creating default at {SETTINGS_FILE}")
            save_settings(DEFAULT_SETTINGS)
            return DEFAULT_SETTINGS

        with open(SETTINGS_FILE, "r") as f:
            settings = json.load(f)

            return settings
    except Exception as e:
        logger.error(f"Error loading settings, using defaults: {e}")
        # Try to save default settings for next time
        try:
            save_settings(DEFAULT_SETTINGS)
        except Exception:
            logger.exception("Failed to save default settings")

        return DEFAULT_SETTINGS


# save settings to the settings file
def save_settings(settings):
    """
    Save settings to the settings file

    Args:
        settings (dict): Settings dictionary to save
    """
    try:
        # Ensure parent directory exists
        os.makedirs(SETTINGS_FILE.parent, exist_ok=True)

        with open(SETTINGS_FILE, "w") as f:
            json.dump(settings, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving settings: {e}")


# get the micro-ROS agent enabled state
def get_micro_ros_agent_enabled():
    """
    Get the micro-ROS agent enabled state

    Returns:
        bool: True if the micro-ROS agent is enabled, False otherwise
    """
    try:
        settings = get_settings()

        # Check if the micro-ROS agent section exists
        if "micro_ros_agent" in settings and "enabled" in settings["micro_ros_agent"]:
            return settings["micro_ros_agent"]["enabled"]

        # Return default if not found
        return DEFAULT_SETTINGS["micro_ros_agent"]["enabled"]
    except Exception as e:
        logger.error(f"Error getting the micro-ROS agent enabled state: {e}")
        return False


# update the micro-ROS agent enabled state
def update_micro_ros_agent_enabled(enabled):
    """
    Update the micro-ROS agent enabled state

    Args:
        enabled (bool): Whether the micro-ROS agent is enabled

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure the micro-ROS agent section exists
        if "micro_ros_agent" not in settings:
            settings["micro_ros_agent"] = {}

        settings["micro_ros_agent"]["enabled"] = enabled

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating the micro-ROS agent enabled state: {e}")
        return False


# get the micro-ROS agent transport
def get_micro_ros_agent_transport():
    """
    Get the micro-ROS agent transport

    Returns:
        str: The transport (default: udp4)
    """
    settings = get_settings()
    return settings.get("micro_ros_agent", {}).get(
        "transport", DEFAULT_SETTINGS["micro_ros_agent"]["transport"]
    )


# update the micro-ROS agent transport
def update_micro_ros_agent_transport(transport):
    """
    Update micro-ROS Agent transport

    Args:
        transport (str): The transport name

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure the micro-ROS agent section exists
        if "micro_ros_agent" not in settings:
            settings["micro_ros_agent"] = {}

        settings["micro_ros_agent"]["transport"] = transport

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating the micro-ROS agent settings: {e}")
        return False


# get the micro-ROS agent port
def get_micro_ros_agent_port():
    """
    Get the micro-ROS agent port

    Returns:
        int: The port (default: 2019)
    """
    settings = get_settings()
    return settings.get("micro_ros_agent", {}).get(
        "port", DEFAULT_SETTINGS["micro_ros_agent"]["port"]
    )


# update the micro-ROS agent port
def update_micro_ros_agent_port(port):
    """
    Update the micro-ROS agent port

    Args:
        port (int): The port

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure the micro-ROS agent section exists
        if "micro_ros_agent" not in settings:
            settings["micro_ros_agent"] = {}

        settings["micro_ros_agent"]["port"] = port

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating the micro-ROS agent settings: {e}")
        return False


# get the micro-ROS agent verbose level
def get_micro_ros_agent_verbose():
    """
    Get the micro-ROS agent verbose level

    Returns:
        int: The verbose level (default: 4)
    """
    settings = get_settings()
    return settings.get("micro_ros_agent", {}).get(
        "verbose", DEFAULT_SETTINGS["micro_ros_agent"]["verbose"]
    )


# update the micro-ROS agent verbose level
def update_micro_ros_agent_verbose(verbose):
    """
    Update the micro-ROS agent verbose level

    Args:
        verbose (int): The verbose level

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        settings = get_settings()

        # Ensure the micro-ROS agent section exists
        if "micro_ros_agent" not in settings:
            settings["micro_ros_agent"] = {}

        settings["micro_ros_agent"]["verbose"] = verbose

        save_settings(settings)
        return True
    except Exception as e:
        logger.error(f"Error updating the micro-ROS agent settings: {e}")
        return False
