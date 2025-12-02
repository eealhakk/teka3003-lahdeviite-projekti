"""Robot Framework -kirjasto ReferenceManager-luokan testaamiseen"""
import os
from repositories.viite_repository import ReferenceManager

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

    def export_bibtex_file(self, filename="robot_test_output.bib"):
        """Vie viitteet BibTeX-tiedostoon"""
        self.ref.export_bibtex(filename)
        self.bib_file = filename

    def bib_file_should_exist(self):
        """Tarkistaa että BibTeX-tiedosto on luotu"""
        if not os.path.exists(self.bib_file):
            raise AssertionError("BibTeX file was not created")

    def bib_file_should_contain(self, text):
        """Tarkistaa että teksti löytyy BibTeX-tiedostosta"""
        with open(self.bib_file, encoding="utf-8") as f:
            content = f.read()
        if text not in content:
            raise AssertionError(f"'{text}' not found in BibTeX file")

