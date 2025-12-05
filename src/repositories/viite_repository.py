"""Viitteiden hallinta ja käsittely."""

# pylint: disable=too-many-arguments,too-many-positional-arguments
import json
from repositories.database_manager import DatabaseManager
from entities.refobj import Reference

class ReferenceManager:
    """Vastaa viitteiden käsittelystä tietokannassa."""
    def __init__(self, db_name="references.db"):
        self.db_manager = DatabaseManager(db_name)
    
    def _row_to_reference(self, row):
        """
        Palauttaa tuplen, jossa id ja 
        tietokannasta haettu refi oliona
        """
        ref_id, ref_type, key, other_fields_json = row
        other_fields = json.loads(other_fields_json) if other_fields_json else {}
        return (ref_id, Reference(ref_type, key, other_fields))

    def listaa(self):
        """Palauttaa listauksen kaikista viitteistä tietokannassa."""
        rows = self.db_manager.get_reference()
        return [self._row_to_reference(r) for r in rows]

    def entry_info(self, target_key=None):
        """Hakee tietyn viitteen tiedot tietokannasta."""
        row = self.db_manager.get_reference(target_key)
        if not row:
            return None
        return self._row_to_reference(row)
    
    def get_reference_tags(self, reference_id):
        """Hakee viitteen tagit tietokannasta."""
        return self.db_manager.get_tags_for_ref(reference_id)

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
            return "Virheellinen syöte. Käytä numeroita pilkuilla eroteltuna.\n"
        print("=====================================")
        #print (self.db_manager.filter_references_db(choices))
        result = self.db_manager.filter_references_db(choices)
        print(result)
        return(str(self.db_manager.filter_references_db(choices)))

    def edit_entry(self, entry_type, target_key, **kwargs):
        """Muokkaa tietyn viitteen tietoja tietokannassa."""
        self.db_manager.edit_entry(entry_type, target_key, **kwargs)

    def delete_entry(self, entry_type, target_key):
        """Poistaa tietyn viitteen tietokannassa."""
        self.db_manager.delete_entry(entry_type, target_key)

    def add_entry(self, entry_type, key, other_elements = {}, tags=[]):
        """Lisää uuden viitteen tietokantaan."""
        entry = Reference(entry_type, key, other_elements)
        return self.db_manager.insert_reference(entry, tags)

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
