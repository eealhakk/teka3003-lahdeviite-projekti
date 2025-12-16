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
        self.ref.add_entry(
            entry_type="book",
            key=key,
            other_elements={
                "author": author,
                "title": title,
                "year": int(year),
                "publisher": publisher,
                "tags": tags
            }
        )

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def add_article(self, key, author, title, journal, year, volume, pages, tags=None):
        """artikkelin lisääminen"""
        self.ref.add_entry(
            entry_type="article",
            key=key,
            other_elements={
                "author": author,
                "title": title,
                "journal": journal,
                "year": int(year),
                "volume": volume,
                "pages": pages,
                "tags": tags
            }
        )

    # pylint: disable=too-many-arguments, too-many-positional-arguments
    def add_inproceeding(self, key, author, title, year, booktitle, tags=None):
        """inproceedings lisääminen"""
        self.ref.add_entry(
            entry_type="inproceedings",
            key=key,
            other_elements={
                "author": author,
                "title": title,
                "year": int(year),
                "booktitle": booktitle,
                "tags": tags
            }
        )

    def listaa(self):
        """listaus"""
        refs = self.ref.listaa()
        keys = []
        for _, ref in refs:
            keys.append(ref.key)
        return " ".join(keys)

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

    def delete_reference(self, key):
        """Poistaa viitteen avaimen perusteella"""
        self.ref.delete_entry(key)

    def add_article_by_doi(self, doi, key, tags=None):
        """Lisää artikkelin DOI:lla (hakee Crossrefistä ja tallentaa)"""
        if tags is None:
            tags_list = []
        elif isinstance(tags, str):
            tags_list = [t.strip() for t in tags.split(",") if t.strip()]
        else:
            tags_list = list(tags)

        ref = self.ref.fetch_reference_by_doi(doi)
        if not ref:
            raise AssertionError("DOI-haku epäonnistui")

        fields = {
            "author": ref.other_fields.get("author", "-"),
            "title": ref.other_fields.get("title", "-"),
            "journal": ref.other_fields.get("journal", "-"),
            "year": ref.other_fields.get("year", 0),
            "volume": ref.other_fields.get("volume", "-"),
            "pages": ref.other_fields.get("pages", "-"),
        }

        ok = self.ref.add_entry("article", key, fields, tags_list)
        if not ok:
            raise AssertionError("Viitteen lisäys epäonnistui (avaimen pitäs olla uniikki)")


