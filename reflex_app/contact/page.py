import reflex as rx
from ..ui.base import base_page
from . import form, state, model


def contact_entry_list_item(contact: model.ContactEntryModel) -> rx.Component:
    return rx.box(
        rx.heading(contact.first_name, " ", contact.last_name),
        rx.text(contact.email),
        padding="1em",
    )


def foreach_callback(text) -> rx.Component:
    return rx.box(rx.text(text))


def contact_entries_list_page() -> rx.Component:
    print(state.ContactState.entries)
    return base_page(
        rx.vstack(
            rx.heading("Contact Entries", size="7"),
            rx.foreach(
                state.ContactState.entries,
                contact_entry_list_item,
            ),
            spacing="5",
            align_items="center",
            min_height="85vh",
            id="my-child",
        )
    )


def contact_us_page() -> rx.Component:
    my_child = (
        rx.vstack(
            rx.heading("Contact Details", size="9"),
            rx.cond(state.ContactState.did_submit, state.ContactState.thank_you, ""),
            rx.desktop_only(
                rx.box(form.contact_us_form(), id="my-form-box", width="50vw")
            ),
            rx.mobile_and_tablet(
                form.contact_us_form(), id="my-form-box", width="85vw"
            ),
            spacing="5",
            justify="center",
            align_items="center",
            min_height="85vh",
            id="my-child",
        ),
    )

    return base_page(my_child)
