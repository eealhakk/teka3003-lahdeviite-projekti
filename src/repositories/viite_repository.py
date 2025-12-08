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

    def entry_info(self, ref_type=None, key=None):
        """Hakee tietyn viitteen tiedot tietokannasta."""
        row = self.db_manager.get_reference(key=key, ref_type=ref_type)
        if not row:
            return None
        _, ref_obj = self._row_to_reference(row[0])
        return ref_obj
    
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

    def delete_entry(self, ref_type, target_key):
        """Poistaa tietyn viitteen tietokannassa."""
        self.db_manager.delete_entry(target_key, ref_type)

    def add_entry(self, entry_type, key, other_elements = {}, tags=[]):
        """Lisää uuden viitteen tietokantaan."""
        entry = Reference(entry_type, key, other_elements)
        return self.db_manager.insert_reference(entry, tags)

    def export_bibtex(self, filename): # pylint: disable=too-many-locals #TODO too many?
        """Vie kaikki viitteet BibTeX-tiedostoon."""
        references = self.db_manager.get_reference()

        with open(filename, "w", encoding="utf-8") as f:
            for row in references:
                ref_id, ref_type, key, raw_fields = row

                fields = json.loads(raw_fields) if raw_fields else {}

                f.write(f"@{ref_type}{{{key},\n")

                for name, value in fields.items():
                    f.write(f"  {name} = {{{value}}},\n")

                f.write("}\n\n")