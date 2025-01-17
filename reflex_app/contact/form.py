import reflex as rx
from .state import ContactState


def contact_us_form() -> rx.Component:
    return (
        rx.form(
            rx.vstack(
                rx.hstack(
                    rx.input(
                        placeholder="First Name",
                        name="first_name",
                        type="text",
                        required=True,
                        width="100%",
                    ),
                    rx.input(
                        placeholder="Last Name",
                        name="last_name",
                        type="text",
                        # required=True,
                        width="100%",
                    ),
                    width="100%",
                ),
                rx.input(
                    placeholder="Email",
                    name="email",
                    type="email",
                    width="100%",
                    # required=True,
                ),
                rx.text_area(
                    placeholder="Message",
                    name="message",
                    # required=True,
                    width="100%",
                    height="200px",
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=ContactState.handle_submit,
            reset_on_submit=False,
        ),
    )
