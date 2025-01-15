import reflex as rx
from .nav import navbar


def base_page(child: rx.Component, hide_navbar=False, *args, **kwargs) -> rx.Component:
    # print([f"{type(x)}\n" for x in args]),
    # if not isinstance(child, rx.Component):
    #     child = rx.heading("Not a valid rx component")

    # if hide_navbar:
    #     return rx.container(
    #         child,
    #         rx.logo(),
    #         rx.color_mode.button(
    #             position="bottom-right",
    #         ),
    #     )

    return rx.fragment(
        navbar(),
        rx.box(
            child,
            id="base-content-area",
            # bg=rx.color("accent", 3),
            padding="1em",
            # position="fixed",
            # top="0px",
            # z_index="5",
            width="100%",
        ),
        rx.logo(),
        rx.color_mode.button(position="bottom-left"),
        id="base-page",
    )
