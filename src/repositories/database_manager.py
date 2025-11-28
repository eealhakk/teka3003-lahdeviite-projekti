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

    
    #filter_references_db(author, year)
    def filter_references_db(self, conditions):
        # Mapit pääluokille ja attribuuteille TODO: Tämän voi toteuttaa hakuna tietokannasta jos kantaan tulee uusia tauluja
        classes_map = {1: "inproceeding", 2: "article", 3: "book"}
        attributes_map = {
            4: "key", 5: "author", 6: "title", 7: "year",
            8: "publisher", 9: "volume", 10: "pages", 11: "booktitle"
        }
    
        # Tarkistetaan, löytyykö 0 listasta
        list_all = 0 in conditions
    
        # Valitut luokat ja attribuutit
        selected_classes = [classes_map[c] for c in conditions if c in classes_map]
        selected_attributes = [attributes_map[c] for c in conditions if c in attributes_map]
    
        # Jos listataan kaikki, valitaan kaikki luokat ja tyhjennetään attribuutit (kaikki tulostetaan)
        if list_all:
            selected_classes = ["inproceeding", "article", "book"]
            selected_attributes = []  # tyhjä lista = kaikki attribuutit tulostetaan
    
        # Kartoitus luokkien ja tietokantahakufunktioiden välillä
        fetch_map = {
            "inproceeding": (self.get_inproceedings, Inproceeding),
            "article": (self.get_articles, Article),
            "book": (self.get_books, Book),
        }
    
        #TODO Logiikka alla kesken
        # Käydään valitut luokat läpi
        for cls_name in selected_classes:
            # Hakee tuple-muodossa: (fetch-funktio, Python-luokka)
            fetch_func, cls_type = fetch_map[cls_name]
    
            # Haetaan kaikki tietueet tietokannasta
            rows = fetch_func()  # palauttaa listan tupleja
    
            # Käydään jokainen tietue läpi
            for row in rows:
                # Luodaan objekti rivin tiedoista
                # row[0] oletetaan olevan tietokannan sisäinen id, joten käytetään row[1:]
                obj = cls_type(*row[1:])
    
                # Jos listataan kaikki tai attribuuteja ei ole erikseen valittu, tulostetaan koko objekti
                if list_all or not selected_attributes:
                    print(obj)
                else:
                    # Muuten tulostetaan vain valitut attribuutit
                    print (obj.__class__.__name__)
                    output = []
                    for attr in selected_attributes:
                        if hasattr(obj, attr):  # Tarkistetaan, että attribuutti löytyy objektista
                            output.append(f"{attr}={getattr(obj, attr)}")
                    print(", ".join(output))
    
                print("-" * 40)
    
    
    
    
    
    
    
    