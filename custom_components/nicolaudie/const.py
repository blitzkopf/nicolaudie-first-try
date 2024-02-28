"""Constants for Nicolaudie."""
# Base component constants
NAME = "Nicolaudie"
DOMAIN = "nicolaudie"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.0"

ATTRIBUTION = "Data provided by http://jsonplaceholder.typicode.com/"
ISSUE_URL = "https://github.com/blitzkopf/nicolaudie/issues"

# Icons
ICON = "mdi:ipod"

# Platforms
REMOTE = "remote"
SCENE = "scene"
PLATFORMS = [REMOTE, 
             #SCENE
            ]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_HOST = "host"

# Defaults
DEFAULT_NAME = DOMAIN


STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
