from enum import Enum


class Tag(Enum):
    user = "User"
    canvas = "Canvas"
    configuration = "Configuration"
    monitoring = "Monitoring"


tags_metadata = [
    {
        "name": Tag.user.value,
        "description": "Current user endpoints.",
    },
    {
        "name": Tag.canvas.value,
        "description": "Canvas endpoints.",
    },
    {
        "name": Tag.configuration.value,
        "description": "Configuration endpoints for the entire game.",
    },
    {
        "name": Tag.monitoring.value,
        "description": "Endpoints for monitoring.",
    },
]
