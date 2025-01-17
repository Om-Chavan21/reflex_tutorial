"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from rxconfig import config
from .ui.base import base_page
from . import pages, navigation


class State(rx.State):
    """The app state."""

    original_name = "Om"
    label = f"My name is {original_name}"

    def set_label(self, name: str):
        self.label = f"My name is {name}"

    def did_click(self):
        print("clicked")

    ...


def index() -> rx.Component:
    my_child = (
        rx.vstack(
            rx.heading(State.label, size="9"),
            rx.text(
                "Get started by editing ",
                rx.code(f"{config.app_name}/{config.app_name}.py"),
                size="5",
            ),
            rx.input(on_change=State.set_label, placeholder="Enter your name"),
            rx.link(rx.button("about page"), href="/about"),
            spacing="5",
            justify="center",
            min_height="85vh",
            align_items="center",
            text_align="center",
            id="my-child",
        ),
    )

    return base_page(my_child)


app = rx.App()
app.add_page(index)
app.add_page(pages.about_page, route=navigation.routes.ABOUT_US_ROUTE)
app.add_page(pages.pricing_page, route=navigation.routes.PRICING_ROUTE)
app.add_page(pages.contact_us_page, route=navigation.routes.CONTACT_US_ROUTE)
