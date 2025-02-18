from click import Group

from pixel_battle.presentation.cli.commands.refresh_chunk import (
    refresh_chunk_command,
)
from pixel_battle.presentation.cli.commands.schedule_pixel_battle import (
    schedule_pixel_battle_command,
)
from pixel_battle.presentation.cli.commands.view_pixel_battle import (
    view_pixel_battle_command,
)


chunk_group = Group(name="chunk")
chunk_group.add_command(refresh_chunk_command, "refresh")

canvas_group = Group(name="canvas")
canvas_group.add_command(chunk_group)

pixel_battle_group = Group("pixel-battle")
pixel_battle_group.add_command(schedule_pixel_battle_command, "schedule")
pixel_battle_group.add_command(view_pixel_battle_command, "state")
pixel_battle_group.add_command(canvas_group)

admin_group = Group()
admin_group.add_command(pixel_battle_group)
