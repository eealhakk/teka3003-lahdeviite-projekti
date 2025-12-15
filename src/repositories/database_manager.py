"""Tietokannan hallinta"""

# pylint: disable=too-many-arguments,too-many-positional-arguments
import sqlite3
import json
from entities.refobj import Reference

VPL11 = Reference(
    ref_type="inproceeding",
    key="VPL11",
    other_fields={"author": "Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti",
                   "title": "Extreme Apprenticeship Method in Teaching Programming for Beginners.",
                   "year": 2011,
                   "booktitle": ("SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium "
                                 "on Computer science education")}
)

CBH91 = Reference(
    ref_type="article",
    key="CBH91",
    other_fields={"author": "Allan Collins and John Seely Brown and Ann Holum",
                  "title": "Cognitive apprenticeship: making thinking visible",
                  "journal": "American Educator",
                  "year": 1991,
                  "volume": 6,
                  "pages": "38--46"}
)

MARTIN09 = Reference(
    ref_type="book",
    key="Martin09",
    other_fields={"author": "Martin, Robert",
                  "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                  "year": 2008,
                  "publisher": "Prentice Hall"}
)

entries = [VPL11, CBH91, MARTIN09]


class DatabaseManager:
    """Vastaa SQLite-tietokannan hallinnasta."""
    def __init__(self, db_name="references.db"):
        self.db_name = db_name
        self.create_database()

        #testidata
        #if len(self.get_reference()) == 0:
        #    self.insert_reference(VPL11)
        #    self.insert_reference(CBH91)
        #    self.insert_reference(MARTIN09)

    def connect(self):
        """Yhdistää tietokantaan."""
        conn = sqlite3.connect(self.db_name)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    def create_database(self):
        """Luo tarvittavat taulut tietokantaan, jos niitä ei ole."""
        connection = self.connect()
        cursor = connection.cursor()

        #lähdeviite
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS reference (
            id INTEGER PRIMARY KEY,
            type TEXT NOT NULL,
            key TEXT NOT NULL UNIQUE,
            other_fields TEXT
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
        CREATE TABLE IF NOT EXISTS reference_tag (
            reference_id INTEGER NOT NULL,
            tag_id INTEGER NOT NULL,
            FOREIGN KEY (reference_id) REFERENCES reference(id) ON DELETE CASCADE,
            FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE,
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

    def get_tags_for_ref(self, reference_id):
        """Hakee viitteen tagit tietokannasta"""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT t.name
            FROM tags t
            JOIN reference_tag rt ON t.id = rt.tag_id
            WHERE rt.reference_id = ?;
        """, (reference_id,))
        tags = [row[0] for row in cur.fetchall()]
        conn.close()
        return tags

    def get_references_by_tag(self, tag_name):
        """Hakee viitteet tagin perusteella tietokannasta"""
        tag_id = self.get_tag_id(tag_name)
        if not tag_id:
            return []

        conn = self.connect()
        cur = conn.cursor()
        cur.execute("""
            SELECT r.*
            FROM reference r
            JOIN reference_tag rt ON r.id = rt.reference_id
            WHERE rt.tag_id = ?;
        """, (tag_id,))
        rows = cur.fetchall()
        conn.close()
        return rows

    def add_tag_to_ref(self, reference_id, tag_name):
        """Liittää tagin viitteeseen"""
        tag_id = self.get_or_create_tag(tag_name)

        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            "INSERT OR IGNORE INTO reference_tag (reference_id, tag_id) VALUES (?, ?);",
            (reference_id, tag_id),
        )
        conn.commit()
        conn.close()

    # lisäykset tietokantaan
    def insert_reference(self, reference, tags=None):
        """Lisää viitteen tietokantaan."""
        if tags is None:
            tags = []

        other_fields = reference.other_fields
        if not isinstance(other_fields, str):
            other_fields = json.dumps(other_fields)

        try:
            connection = self.connect()
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO reference (type, key, other_fields)
                VALUES (?, ?, ?);
                """,
                (
                    reference.ref_type,
                    reference.key,
                    other_fields
                ),
            )
            new_id = cursor.lastrowid
            connection.commit()
            connection.close()

            for tag in tags:
                self.add_tag_to_ref(new_id, tag)
            return new_id
        except sqlite3.IntegrityError:
            return False

    # haut tietokannasta
    def get_reference(self, key=None, ref_type=None):
        """
        Hakee yhden viitteen avaimen perusteella,
        viitteen perusteella, molempien perusteella,
        tai kaikki viitteet tietokannasta
        """
        connection = self.connect()
        cursor = connection.cursor()
        if ref_type and key:
            cursor.execute("SELECT * FROM reference WHERE type = ? AND key = ?;", (ref_type, key,))
        elif ref_type:
            cursor.execute("SELECT * FROM reference WHERE type = ?;", (ref_type,))
        elif key:
            cursor.execute("SELECT * FROM reference WHERE key = ?;", (key,))
        else:
            cursor.execute("SELECT * FROM reference;")
        rows = cursor.fetchall()
        connection.close()
        return rows


    # muokkaus tietokannassa
    def edit_entry(self, entry_type, target_key, **kwargs):
        """Muokkaa tietokannan merkintää."""
        conn = self.connect()
        cur = conn.cursor()

        # Haetaan nykyiset other_fields
        cur.execute('SELECT other_fields FROM reference WHERE "key" = ? AND type = ?;',
                    (target_key, entry_type))
        row = cur.fetchone()
        if not row:
            conn.close()
            return False

        raw = row[0] or "{}"
        try:
            other_fields = json.loads(raw)
            if not isinstance(other_fields, dict):
                other_fields = {}
        except json.JSONDecodeError:
            other_fields = {}

        # Jos tyyppi tai avain on annettu, käsitellään ne erikseen
        update_cols = {}
        if "type" in kwargs:
            update_cols["type"] = kwargs.pop("type")

        new_key = kwargs.pop("key", None)

        # Päivitetään muut kentät other_fieldsiin
        for field, value in kwargs.items():
            other_fields[field] = value

        update_cols["other_fields"] = json.dumps(other_fields, ensure_ascii=False)

        if new_key is not None:
            update_cols["key"] = new_key

        fields_sql = ", ".join([f'{col} = ?' for col in update_cols.keys()])
        values = list(update_cols.values()) + [target_key]

        cur.execute(f'UPDATE reference SET {fields_sql} WHERE "key" = ?;', values)

        changed = cur.rowcount > 0
        conn.commit()
        conn.close()
        return changed

    def delete_entry(self, target_key):
        """Poistaa tietokannan merkinnän ja siihen liitetyt tagit"""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute('DELETE FROM reference WHERE key = ?;', (target_key,))
        deleted = cur.rowcount > 0
        conn.commit()
        conn.close()
        return deleted

    def filter_references_db(self, conditions): # pylint: disable=too-many-locals
        """Hakee tietokannasta avaimilla oikeat tiedot"""

        field = conditions[0]
        if len(conditions) >= 2:
            field_value = conditions[1]
        else: field_value = ''

        connection = self.connect()
        cursor = connection.cursor()

        if field == "type":
            cursor.execute("SELECT * FROM reference WHERE type LIKE ?;",(field_value,))
        elif field == "id":
            cursor.execute("SELECT * FROM reference WHERE id LIKE ?;",(field_value,))
        elif field == "key":
            cursor.execute("SELECT * FROM reference WHERE key LIKE ?;",(field_value,))
        else:
            cursor.execute("""
                           SELECT * FROM reference
                           WHERE other_fields LIKE ?
                           OR other_fields LIKE ?;
                           """,
                           (
                               '%'+field+'____'+field_value+'%', # jos muodossa "year": "2008"
                               '%'+field+'___'+field_value+'%' # jos muodossa "year": 2008
                            ))
        rows = cursor.fetchall()
        connection.close()
        return rows
