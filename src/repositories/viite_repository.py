from entities.refobj import Article, Inproceeding, Book
import sqlite3

VPL11 = Inproceeding(
    key="VPL11",
    author="Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti",
    title="Extreme Apprenticeship Method in Teaching Programming for Beginners.",
    year=2011,
    booktitle="SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium on Computer science education"
)

CBH91 = Article(
    key="CBH91",
    author="Allan Collins and John Seely Brown and Ann Holum",
    title="Cognitive apprenticeship: making thinking visible",
    journal="American Educator",
    year=1991,
    volume=6,
    pages="38--46"
)

Martin09 = Book(
    key="Martin09",
    author="Martin, Robert",
    title="Clean Code: A Handbook of Agile Software Craftsmanship",
    year=2008,
    publisher="Prentice Hall"
)

entries = [VPL11, CBH91, Martin09]

class Database_manager:
    def __init__(self, db_name="references.db"):
        self.db_name = db_name
        self.create_database()

    def connect(self):
        return sqlite3.connect(self.db_name)

    def create_database(self):
        connection = self.connect()
        cursor = connection.cursor()

        #inproceedings
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inproceeding (
            id INTEGER PRIMARY KEY,
            key TEXT NOT NULL UNIQUE,
            author TEXT NOT NULL,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            booktitle TEXT NOT NULL
        );
        """)

        #article
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS article (
            id INTEGER PRIMARY KEY,
            key TEXT NOT NULL UNIQUE,
            author TEXT NOT NULL,
            title TEXT NOT NULL,
            journal TEXT NOT NULL,
            year INTEGER NOT NULL,
            volume INTEGER NOT NULL,
            pages TEXT NOT NULL
        );
        """)

        #book
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS book (
            id INTEGER PRIMARY KEY,
            key TEXT NOT NULL UNIQUE,
            author TEXT NOT NULL,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            publisher TEXT NOT NULL
        );
        """)
        connection.commit()
        connection.close()
    
    def insert_inproceeding(self, inproceeding):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO inproceeding (key, author, title, year, booktitle)
        VALUES (?, ?, ?, ?, ?);
        """, (inproceeding.key, inproceeding.author, inproceeding.title, inproceeding.year, inproceeding.booktitle))
        connection.commit()
        connection.close()
    
    def insert_article(self, article):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO article (key, author, title, journal, year, volume, pages)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        """, (article.key, article.author, article.title, article.journal, article.year, article.volume, article.pages))
        connection.commit()
        connection.close()
    
    def insert_book(self, book):
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO book (key, author, title, year, publisher)
        VALUES (?, ?, ?, ?, ?);
        """, (book.key, book.author, book.title, book.year, book.publisher))
        connection.commit()
        connection.close()


class Reference_manager:
    def __init__(self, references=None):
        if references is None:
            references = entries.copy() #[] testi data
        self.references = references

    def listaa(self):
        for index, ref in enumerate(self.references, start=1):
            print(f"{index}) avain: {ref.key}\nauthor: {ref.author}\n")

    def add_book(self, key, author, title, year, publisher):
        return self.add_reference(Book(key, author, title, year, publisher))
    
    def add_article(self, key, author, title, journal, year, booktitle):
        return self.add_reference(Article(key, author, title, journal, year, booktitle))
    
    def add_inproceeding(self, key, author, title, year, booktitle):
        return self.add_reference(Inproceeding(key, author, title, year, booktitle))

    def add_reference(self, ref):
        if ref:
            self.references.append(ref)


def main():
    reference = Reference_manager()
    print(reference)

if __name__ == "__main__":
    main()
