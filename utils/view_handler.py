from discord import ui


def to_unavailable(view: ui.View) -> ui.View:
    for c in view.children:
        if isinstance(c, (ui.Button, ui.Select)):
            c.disabled = True
        else:
            continue
    return view
