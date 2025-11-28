"""Tietokannan hallinta"""

# pylint: disable=too-many-arguments,too-many-positional-arguments
import sqlite3
from entities.refobj import Article, Inproceeding, Book

VPL11 = Inproceeding(
    key="VPL11",
    author="Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti",
    title="Extreme Apprenticeship Method in Teaching Programming for Beginners.",
    year=2011,
    booktitle=(
        "SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium on "
        "Computer science education"
    )
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

MARTIN09 = Book(
    key="Martin09",
    author="Martin, Robert",
    title="Clean Code: A Handbook of Agile Software Craftsmanship",
    year=2008,
    publisher="Prentice Hall"
)

entries = [VPL11, CBH91, MARTIN09]


class DatabaseManager:
    """Vastaa SQLite-tietokannan hallinnasta."""
    def __init__(self, db_name="references.db"):
        self.db_name = db_name
        self.create_database()

        #testidata
        #if self.connect().execute("SELECT COUNT(*) FROM inproceeding;").fetchone()[0] == 0:
        #    self.insert_inproceeding(VPL11)
        #    self.insert_article(CBH91)
        #    self.insert_book(MARTIN09)

    def connect(self):
        """Yhdistää tietokantaan."""
        return sqlite3.connect(self.db_name)

    def create_database(self):
        """Luo tarvittavat taulut tietokantaan, jos niitä ei ole."""
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

    # lisäykset tietokantaan
    def insert_inproceeding(self, inproceeding):
        """Lisää inproceeding tietokantaan."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO inproceeding (key, author, title, year, booktitle)
            VALUES (?, ?, ?, ?, ?);
            """,
            (
                inproceeding.key,
                inproceeding.author,
                inproceeding.title,
                inproceeding.year,
                inproceeding.booktitle,
            ),
        )
        connection.commit()
        connection.close()

    def insert_article(self, article):
        """Lisää article tietokantaan."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO article (key, author, title, journal, year, volume, pages)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (
                article.key,
                article.author,
                article.title,
                article.journal,
                article.year,
                article.volume,
                article.pages,
            ),
        )
        connection.commit()
        connection.close()

    def insert_book(self, book):
        """Lisää book tietokantaan."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute("""
        INSERT INTO book (key, author, title, year, publisher)
        VALUES (?, ?, ?, ?, ?);
        """, (book.key, book.author, book.title, book.year, book.publisher))
        connection.commit()
        connection.close()

    # haut tietokannasta
    def get_inproceedings(self, key=None):
        """Hakee inproceedingin tai kaikki inproceedingit tietokannasta"""
        connection = self.connect()
        cursor = connection.cursor()
        if key:
            cursor.execute("SELECT * FROM inproceeding WHERE key = ?;", (key,))
        else:
            cursor.execute("SELECT * FROM inproceeding;")
        rows = cursor.fetchall()
        connection.close()
        return rows

    def get_articles(self, key=None):
        """Hakee articlen tai kaikki articlet tietokannasta"""
        connection = self.connect()
        cursor = connection.cursor()
        if key:
            cursor.execute("SELECT * FROM article WHERE key = ?;", (key,))
        else:
            cursor.execute("SELECT * FROM article;")
        rows = cursor.fetchall()
        connection.close()
        return rows

    def get_books(self, key=None):
        """Hakee bookin tai kaikki bookit tietokannasta"""
        connection = self.connect()
        cursor = connection.cursor()
        if key:
            cursor.execute("SELECT * FROM book WHERE key = ?;", (key,))
        else:
            cursor.execute("SELECT * FROM book;")
        rows = cursor.fetchall()
        connection.close()
        return rows

    # muokkaus tietokannassa
    def edit_entry(self, entry_type, target_key, **kwargs):
        """Muokkaa tietokannan merkintää."""
        connection = self.connect()
        cursor = connection.cursor()

        fields = ', '.join([f"{k} = ?" for k in kwargs])
        values = list(kwargs.values())
        values.append(target_key)

        query = f"UPDATE {entry_type} SET {fields} WHERE key = ?;"
        cursor.execute(query, values)

        connection.commit()
        connection.close()

    def delete_entry(self, entry_type, target_key):
        """Poistaa tietokannan merkinnän."""
        connection = self.connect()
        cursor = connection.cursor()

        poistettava = [target_key]

        query = f"DELETE FROM {entry_type} WHERE key = ?;"
        cursor.execute(query, poistettava)

        connection.commit()
        connection.close()
