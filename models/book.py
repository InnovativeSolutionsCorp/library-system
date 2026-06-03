from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Book:
    title: str
    author: str
    isbn: str
    available: bool = True

    def __str__(self) -> str:
        availability = "Available" if self.available else "Not Available"
        return f"{self.title} by {self.author} (ISBN: {self.isbn}) - {availability}"