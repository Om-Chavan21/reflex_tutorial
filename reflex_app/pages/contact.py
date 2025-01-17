import reflex as rx
from ..ui.base import base_page


class ContactState(rx.State):
    form_data: dict = {}

    def handle_submit(self, form_data: dict):
        self.form_data = form_data
        print(self.form_data)
        return rx.window_alert("Form submitted!")


def contact_us_page() -> rx.Component:
    my_form = (
        rx.form(
            rx.vstack(
                rx.input(
                    placeholder="First Name",
                    name="first_name",
                ),
                rx.input(
                    placeholder="Last Name",
                    name="last_name",
                ),
                rx.hstack(
                    rx.checkbox("Checked", name="check"),
                    rx.switch("Switched", name="switch"),
                ),
                rx.button("Submit", type="submit"),
            ),
            on_submit=ContactState.handle_submit,
            reset_on_submit=True,
        ),
    )

    my_child = (
        rx.vstack(
            rx.heading("Contact Details", size="9"),
            my_form,
            spacing="5",
            justify="center",
            align_items="center",
            min_height="85vh",
            id="my-child",
        ),
    )

    return base_page(my_child)
