from repositories.viite_repository import ReferenceManager
import os

class ReferenceManagerLibrary:
    """Robot Framework -kirjasto ReferenceManagerille robot testeihin"""

    def __init__(self):
        self.db_file = "robot_test.db"
        self.ref = None

    def setup_database(self):
        """Tyhjentää testitietokannan ja luo ReferenceManagerin"""
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
        self.ref = ReferenceManager(self.db_file)

    def add_book(self, key, author, title, year, publisher, tags=None):
        """kirjan lisääminen"""
        self.ref.add_book(key, author, title, year, publisher, tags)

    def add_article(self, key, author, title, journal, year, volume, pages, tags=None):
        """artikkelin lisääminen"""
        self.ref.add_article(key, author, title, journal, year, volume, pages, tags)

    def add_inproceeding(self, key, author, title, year, booktitle, tags=None):
        """inproceedings lisääminen"""
        self.ref.add_inproceeding(key, author, title, year, booktitle, tags)

    def listaa(self):
        """listaus"""
        return self.ref.listaa()
