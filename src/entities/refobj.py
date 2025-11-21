class Article:
    def __init__(self, key, author, title, journal, year, volume, pages):
        self.key = key
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.volume = volume
        self.pages = pages

class Book:
    def __init__(self, key, author, title, year, publisher):
        self.key = key
        self.author = author
        self.title = title
        self.year = year
        self.publisher = publisher

class Inproceeding:
    def __init__(self, key, author, title, year, booktitle):
        self.key = key
        self.author = author
        self.title = title
        self.year = year
        self.booktitle = booktitle

## Pystyy siistiä perinnällä