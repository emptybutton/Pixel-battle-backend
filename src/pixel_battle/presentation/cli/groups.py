from click import Group

from pixel_battle.presentation.cli.commands.refresh_chunk_image import (
    refresh_chunk_image_command,
)
from pixel_battle.presentation.cli.commands.schedule_pixel_battle import (
    schedule_pixel_battle_command,
)


pixel_battle_group = Group("pixel-battle")
pixel_battle_group.add_command(schedule_pixel_battle_command)

chunk_group = Group(name="chunk")
chunk_group.add_command(refresh_chunk_image_command)

admin_group = Group()
admin_group.add_command(pixel_battle_group)
admin_group.add_command(chunk_group)
