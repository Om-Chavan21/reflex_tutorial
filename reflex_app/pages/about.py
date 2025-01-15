import reflex as rx
from ..ui.base import base_page


def about_page() -> rx.Component:
    my_child = (
        rx.vstack(
            rx.heading("ABOUT US", size="9"),
            rx.text(
                "Something cool about us",
                size="5",
            ),
            spacing="5",
            justify="center",
            align_items="center",
            min_height="85vh",
            id="my-child",
        ),
    )

    return base_page(my_child)
