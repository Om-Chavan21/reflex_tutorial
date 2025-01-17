import reflex as rx
import asyncio
from sqlmodel import select
from .model import ContactEntryModel
from typing import List


class ContactState(rx.State):
    form_data: dict = {}
    entries: List["ContactEntryModel"] = []
    did_submit: bool = False

    @rx.var(cache=False)
    def thank_you(self) -> rx.Component:
        first_name = self.form_data.get("first_name") or ""
        return rx.heading(f"Thank you, {first_name} ".strip() + "!")

    async def handle_submit(self, form_data: dict):
        self.form_data = form_data
        self.did_submit = True
        try:
            with rx.session() as session:
                db_entry = ContactEntryModel(**form_data)
                session.add(db_entry)
                session.commit()
        except Exception as e:
            print(f"Error saving data: {e}")
        await asyncio.sleep(3)
        self.did_submit = False

    def list_entries(self):
        with rx.session() as session:
            entries = session.exec(select(ContactEntryModel)).all()
            print(entries)
            self.entries = entries
