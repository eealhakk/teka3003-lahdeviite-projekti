"""Viitteiden hallinta ja käsittely."""

# pylint: disable=too-many-arguments,too-many-positional-arguments
from repositories.database_manager import DatabaseManager
from entities.refobj import Article, Inproceeding, Book

class ReferenceManager:
    """Vastaa viitteiden käsittelystä tietokannassa."""
    def __init__(self, db_name="references.db"):
        self.db_manager = DatabaseManager(db_name)

    def listaa(self):
        """Palauttaa listauksen kaikista viitteistä tietokannassa."""
        inproceedings = self.db_manager.get_inproceedings()
        articles = self.db_manager.get_articles()
        books = self.db_manager.get_books()

        listing = "Inproceedings:\n"
        for row in inproceedings:
            listing += str(row) + "\n"
            listing += (
                "tagit: " 
                + ", ".join(self.get_reference_tags("inproceeding", row[0])) 
                + "\n\n"
            )

        listing += "\nArticles:\n"
        for row in articles:
            listing += str(row) + "\n"

        listing += "\nBooks:\n"
        for row in books:
            listing += str(row) + "\n"
            listing += "tagit: " + ", ".join(self.get_reference_tags("book", row[0])) + "\n\n"

        return listing

    def get_reference_tags(self, ref_type, reference_id):
        """Hakee viitteen tagit tietokannasta."""
        return self.db_manager.get_tags_for_ref(ref_type, reference_id)

    def get_references_by_tag(self, tag_name):
        """Hakee viitteet tietokannasta tagin perusteella."""
        return self.db_manager.get_references_by_tag(tag_name)

    def filter_references(self, arvot):
        """Siistitään filter syötettä ja välitetään filtteröinti"""
        try:
            # Muutetaan syöte listaksi kokonaislukuja
            choices = [int(x.strip()) for x in arvot.split(",")]
        except ValueError:
            print("Virheellinen syöte. Käytä numeroita pilkuilla eroteltuna.")
            return
        print("=====================================")
        print (self.db_manager.filter_references_db(choices))
        print("=====================================")

    def entry_info(self, entry_type, target_key):
        """Hakee tietyn viitteen tiedot tietokannasta."""
        fetch_map = {
            "inproceeding": (self.db_manager.get_inproceedings, Inproceeding),
            "article": (self.db_manager.get_articles, Article),
            "book": (self.db_manager.get_books, Book),
        }

        if entry_type not in fetch_map:
            return None

        fetcher, constructor = fetch_map[entry_type]
        rows = fetcher(target_key)

        if not rows:
            return None

        return constructor(*rows[0][1:])

    def edit_entry(self, entry_type, target_key, **kwargs):
        """Muokkaa tietyn viitteen tietoja tietokannassa."""
        self.db_manager.edit_entry(entry_type, target_key, **kwargs)

    def delete_entry(self, entry_type, target_key):
        """Poistaa tietyn viitteen tietokannassa."""
        self.db_manager.delete_entry(entry_type, target_key)

    def add_book(self, key, author, title, year, publisher, tags=None):
        """lisää kirjan tietokantaan"""
        if tags is None:
            tags = []
        self.db_manager.insert_book(Book(key, author, title, year, publisher), tags)

    def add_article(self, key, author, title, journal, year, volume, pages, tags=None):
        """lisää artikkelin tietokantaan"""
        if tags is None:
            tags = []
        self.db_manager.insert_article(
            Article(key, author, title, journal, year, volume, pages), 
            tags
        )

    def add_inproceeding(self, key, author, title, year, booktitle, tags=None):
        """lisää inproceedingin tietokantaan"""
        if tags is None:
            tags = []
        self.db_manager.insert_inproceeding(Inproceeding(key, author, title, year, booktitle), tags)

    def export_bibtex(self, filename): # pylint: disable=too-many-locals #TODO too many?
        """Vie kaikki viitteet BibTeX-tiedostoon."""
        inproceedings = self.db_manager.get_inproceedings()
        articles = self.db_manager.get_articles()
        books = self.db_manager.get_books()

        with open(filename, "w", encoding="utf-8") as f:
            for row in inproceedings:
                _, key, author, title, year, booktitle = row
                f.write(f"@inproceedings{{{key},\n")
                f.write(f"  author = {{{author}}},\n")
                f.write(f"  title = {{{title}}},\n")
                f.write(f"  booktitle = {{{booktitle}}},\n")
                f.write(f"  year = {{{year}}}\n")
                f.write("}\n\n")

            for row in articles:
                _, key, author, title, journal, year, volume, pages = row
                f.write(f"@article{{{key},\n")
                f.write(f"  author = {{{author}}},\n")
                f.write(f"  title = {{{title}}},\n")
                f.write(f"  journal = {{{journal}}},\n")
                f.write(f"  year = {{{year}}},\n")
                f.write(f"  volume = {{{volume}}},\n")
                f.write(f"  pages = {{{pages}}}\n")
                f.write("}\n\n")

            for row in books:
                _, key, author, title, year, publisher = row
                f.write(f"@book{{{key},\n")
                f.write(f"  author = {{{author}}},\n")
                f.write(f"  title = {{{title}}},\n")
                f.write(f"  year = {{{year}}},\n")
                f.write(f"  publisher = {{{publisher}}}\n")
                f.write("}\n\n")
