"""Roda o gh-space-shooter com as cores do tema Dracula."""

from gh_space_shooter.game.render_context import RenderContext
from gh_space_shooter.cli import app


def dracula() -> RenderContext:
    return RenderContext(
        cell_size=12,
        cell_spacing=3,
        padding=40,
        background_color=(40, 42, 54),    # #282a36
        grid_color=(52, 55, 70),          # #343746
        enemy_colors={
            1: (98, 114, 164),            # #6272a4
            2: (189, 147, 249),           # #bd93f9
            3: (255, 121, 198),           # #ff79c6
            4: (255, 85, 85),             # #ff5555
        },
        ship_color=(139, 233, 253),       # #8be9fd
        bullet_color=(241, 250, 140),     # #f1fa8c
    )


RenderContext.darkmode = staticmethod(dracula)

if __name__ == "__main__":
    app()
