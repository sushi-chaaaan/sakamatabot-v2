from __future__ import annotations

from discord import ui


class View(ui.View):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def disable_all(self) -> View:
        for c in self.children:
            if isinstance(
                c,
                (
                    ui.Button,
                    ui.Select,
                    ui.ChannelSelect,
                    ui.RoleSelect,
                    ui.UserSelect,
                    ui.MentionableSelect,
                ),
            ):
                c.disabled = True
            else:
                continue
        return self
