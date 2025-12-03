# pylint: disable=invalid-name
"""Robot Framework -kirjasto ReferenceManager-luokan testaamiseen"""
import os
from repositories.viite_repository import ReferenceManager

class ReferenceManagerLibrary:
    """Robot Framework -kirjasto ReferenceManagerille robot testeihin"""

    def __init__(self):
        self.db_file = "robot_test.db"
        self.bib_file = "robot_test_output.bib"
        self.ref = None

    def setup_database(self):
        """Tyhjentää testitietokannan ja luo ReferenceManagerin"""
        if os.path.exists(self.db_file):
            os.remove(self.db_file)
        if os.path.exists(self.bib_file):
            os.remove(self.bib_file)
        self.ref = ReferenceManager(self.db_file)

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def add_book(self, key, author, title, year, publisher, tags=None):
        """kirjan lisääminen"""
        self.ref.add_book(key, author, title, year, publisher, tags)

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def add_article(self, key, author, title, journal, year, volume, pages, tags=None):
        """artikkelin lisääminen"""
        self.ref.add_article(key, author, title, journal, year, volume, pages, tags)

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def add_inproceeding(self, key, author, title, year, booktitle, tags=None):
        """inproceedings lisääminen"""
        self.ref.add_inproceeding(key, author, title, year, booktitle, tags)

    def listaa(self):
        """listaus"""
        return self.ref.listaa()

    def export_bibtex_file(self, filename=None):
        """Vie viitteet BibTeX-tiedostoon"""
        if filename is None:
            filename = self.bib_file
        else:
            self.bib_file = filename  # päivitetään luokan attribuutti, jos annettu
        self.ref.export_bibtex(filename)

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
