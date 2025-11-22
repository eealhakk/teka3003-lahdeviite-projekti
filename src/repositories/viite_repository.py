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


class DatabaseManager:
    def __init__(self, db_name="references.db"):
        self.db_name = db_name
        self.create_database()

        #testidata
        if self.connect().execute("SELECT COUNT(*) FROM inproceeding;").fetchone()[0] == 0:
            self.insert_inproceeding(VPL11)
            self.insert_article(CBH91)
            self.insert_book(Martin09)

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

    # lisäykset tietokantaan
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

    # haut tietokannasta
    def get_inproceedings(self, key=None):
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
        connection = self.connect()
        cursor = connection.cursor()
        if key:
            cursor.execute("SELECT * FROM book WHERE key = ?;", (key,))
        else:
            cursor.execute("SELECT * FROM book;")
        rows = cursor.fetchall()
        connection.close()
        return rows
    

class ReferenceManager:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def listaa(self):
        inproceedings = self.db_manager.get_inproceedings()
        articles = self.db_manager.get_articles()
        books = self.db_manager.get_books()

        print("Inproceedings:")
        for row in inproceedings:
            print(row)

        print("\nArticles:")
        for row in articles:
            print(row)

        print("\nBooks:")
        for row in books:
            print(row)

    def add_book(self, key, author, title, year, publisher):
        return self.db_manager.insert_book(Book(key, author, title, year, publisher))
    
    def add_article(self, key, author, title, journal, year, volume, pages):
        return self.db_manager.insert_article(Article(key, author, title, journal, year, volume, pages))
    
    def add_inproceeding(self, key, author, title, year, booktitle):
        return self.db_manager.insert_inproceeding(Inproceeding(key, author, title, year, booktitle))