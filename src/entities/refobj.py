class Article:
    def __init__(self, key, author, title, journal, year, volume, pages):
        self.key = key
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.volume = volume
        self.pages = pages
    
    def __str__(self):
        return f"key={self.key}\nauthor={self.author}\ntitle={self.title}\njournal={self.journal}\nyear={self.year}\nvolume={self.volume}\npages={self.pages}"

class Book:
    def __init__(self, key, author, title, year, publisher):
        self.key = key
        self.author = author
        self.title = title
        self.year = year
        self.publisher = publisher
    
    def __str__(self):
        return f"key={self.key}\nauthor={self.author}\ntitle={self.title}\nyear={self.year}\npublisher={self.publisher}"

class Inproceeding:
    def __init__(self, key, author, title, year, booktitle):
        self.key = key
        self.author = author
        self.title = title
        self.year = year
        self.booktitle = booktitle
    
    def __str__(self):
        return f"key={self.key}\nauthor={self.author}\ntitle={self.title}\nyear={self.year}\nbooktitle={self.booktitle}"

## Pystyy siistiä perinnällä