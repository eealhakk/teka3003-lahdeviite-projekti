"""Viiteluokat: Article, Book ja Inproceeding."""
# pylint: disable=too-many-arguments
# pylint: disable=too-few-public-methods

class Article:
    """Artikkeli-luokka edustaa tieteellistä artikkelia viitetietona."""
    def __init__(self, key, author, title, journal, year, volume, pages):
        self.key = key
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.volume = volume
        self.pages = pages

    def __str__(self):
        return (
            f"key={self.key}\n"
            f"author={self.author}\n"
            f"title={self.title}\n"
            f"journal={self.journal}\n"
            f"year={self.year}\n"
            f"volume={self.volume}\n"
            f"pages={self.pages}"
        )

class Book:
    """Kirja-luokka edustaa kirjaa viitetietona."""
    def __init__(self, key, author, title, year, publisher):
        self.key = key
        self.author = author
        self.title = title
        self.year = year
        self.publisher = publisher

    def __str__(self):
        return (
            f"key={self.key}\n"
            f"author={self.author}\n"
            f"title={self.title}\n"
            f"year={self.year}\n"
            f"publisher={self.publisher}"
        )

class Inproceeding:
    """Inproceeding-luokka edustaa konferenssijulkaisua viitetietona."""
    def __init__(self, key, author, title, year, booktitle):
        self.key = key
        self.author = author
        self.title = title
        self.year = year
        self.booktitle = booktitle

    def __str__(self):
        return (
            f"key={self.key}\n"
            f"author={self.author}\n"
            f"title={self.title}\n"
            f"year={self.year}\n"
            f"booktitle={self.booktitle}"
        )
## Pystyy siistiä perinnällä
