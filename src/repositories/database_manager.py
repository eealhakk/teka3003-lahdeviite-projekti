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
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

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

        # tagit
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        );
        """)

        # tag yhdistetaulut
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS inproceeding_tag (
            reference_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            FOREIGN KEY (reference_id) REFERENCES inproceeding(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id),
            PRIMARY KEY (reference_id, tag_id)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS article_tag (
            reference_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            FOREIGN KEY (reference_id) REFERENCES article(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id),
            PRIMARY KEY (reference_id, tag_id)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS book_tag (
            reference_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            FOREIGN KEY (reference_id) REFERENCES book(id),
            FOREIGN KEY (tag_id) REFERENCES tags(id),
            PRIMARY KEY (reference_id, tag_id)
        );
        """)

        connection.commit()
        connection.close()

    def get_tag_id(self, name):
        """Hakee tagin id:n tagin nimen perusteella."""
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("SELECT id FROM tags WHERE name = ?;", (name,))
        row = cur.fetchone()
        conn.close()

        if row:
            return row[0]
        return None

    def get_or_create_tag(self, name):
        """Palauttaa tagin id:n tai luo uuden"""
        #jos tagi löytyy, palautetaan sen id
        tag_id = self.get_tag_id(name)
        if tag_id:
            return tag_id

        #muuten luodaan uusi tagi
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("INSERT INTO tags (name) VALUES (?);", (name,))
        tag_id = cur.lastrowid
        conn.commit()
        conn.close()
        return tag_id

    def get_tags_for_ref(self, ref_type, reference_id):
        """Hakee viitteen tagit tietokannasta"""
        table_map = {
            "inproceeding": "inproceeding_tag",
            "article": "article_tag",
            "book": "book_tag",
        }
        link_table = table_map[ref_type]

        conn = self.connect()
        cur = conn.cursor()
        cur.execute(f"""
            SELECT t.name
            FROM tags t
            JOIN {link_table} lt ON t.id = lt.tag_id
            WHERE lt.reference_id = ?;
        """, (reference_id,))
        tags = [row[0] for row in cur.fetchall()]
        conn.close()

        return tags

    def get_references_by_tag(self, tag_name):
        """Hakee viitteet tagin perusteella"""
        tag_id = self.get_tag_id(tag_name)
        if not tag_id:
            return []

        conn = self.connect()
        cur = conn.cursor()

        results = []

        table_map = {
            "inproceeding": "inproceeding_tag",
            "article": "article_tag",
            "book": "book_tag",
        }

        for ref_type, link_table in table_map.items():
            cur.execute(f"""
                SELECT r.*
                FROM {ref_type} r
                JOIN {link_table} lt ON r.id = lt.reference_id
                WHERE lt.tag_id = ?;
            """, (tag_id,))
            rows = cur.fetchall()
            results.extend((ref_type, row) for row in rows)

        conn.close()
        return results

    def add_tag_to_ref(self, ref_type, reference_id, tag_name):
        """Liittää tagin viitteeseen"""
        table_map = {
            "inproceeding": "inproceeding_tag",
            "article": "article_tag",
            "book": "book_tag",
        }
        if ref_type not in table_map:
            raise ValueError(f"Tuntematon tyyppi: {ref_type}")

        tag_id = self.get_or_create_tag(tag_name)
        link_table = table_map[ref_type]

        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            f"INSERT OR IGNORE INTO {link_table} (reference_id, tag_id) VALUES (?, ?);",
            (reference_id, tag_id),
        )
        conn.commit()
        conn.close()

    # lisäykset tietokantaan
    def insert_inproceeding(self, inproceeding, tags=[]):
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
        new_id = cursor.lastrowid
        connection.commit()
        connection.close()

        for tag in tags:
            self.add_tag_to_ref("inproceeding", new_id, tag)
        return new_id

    def insert_article(self, article, tags=[]):
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
        new_id = cursor.lastrowid
        connection.commit()
        connection.close()

        for tag in tags:
            self.add_tag_to_ref("article", new_id, tag)
        return new_id

    def insert_book(self, book, tags=[]):
        """Lisää book tietokantaan."""
        connection = self.connect()
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO book (key, author, title, year, publisher)
            VALUES (?, ?, ?, ?, ?);
            """,
            (
                book.key,
                book.author,
                book.title,
                book.year,
                book.publisher
            )
        )
        new_id = cursor.lastrowid
        connection.commit()
        connection.close()
        for tag in tags:
            self.add_tag_to_ref("book", new_id, tag)
        return new_id

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

    def filter_references_db(self, conditions): # pylint: disable=too-many-locals
        """Hakee tietokannasta avaimilla oikeat tiedot"""
        # TODO: Tämän voi toteuttaa hakuna tietokannasta # pylint: disable=W0511
        # jos kantaan tulee uusia tauluja
        # Mapit pääluokille ja attribuuteille
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

        # Jos listataan kaikki, valitaan kaikki luokat ja tyhjennetään
        # attribuutit (kaikki tulostetaan)
        if list_all:
            selected_classes = ["inproceeding", "article", "book"]
            selected_attributes = []  # tyhjä lista = kaikki attribuutit tulostetaan

        fetch_map = {
            "inproceeding": (self.get_inproceedings, Inproceeding),
            "article": (self.get_articles, Article),
            "book": (self.get_books, Book),
        }

        # Käydään valitut luokat läpi TODO Logiikka alla kesken
        for cls_name in selected_classes:

            fetch_func, cls_type = fetch_map[cls_name]

            # Haetaan kaikki tietueet tietokannasta
            rows = fetch_func()

            # Käydään tietueet läpi
            for row in rows:
                # Luodaan objekti rivin tiedoista
                obj = cls_type(*row[1:])

                # Jos listataan kaikki tai attribuuteja ei ole erikseen valittu,
                # tulostetaan koko objekti
                if list_all or not selected_attributes:
                    print(obj.__class__.__name__)
                    #print(obj)
                    for attr, value in obj.__dict__.items():
                        if not attr.startswith("_"):
                            print(f"{attr}: {value}")
                else:
                    # Tulostetaan vain valitut attribuutit
                    print(obj.__class__.__name__)
                    output = []
                    for attr in selected_attributes:
                        if hasattr(obj, attr):
                            output.append(f"{attr}: {getattr(obj, attr)}")
                    print(",\n".join(output))

                print("-"*40)
