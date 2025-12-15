"""Viitteiden hallinta ja käsittely."""

# pylint: disable=too-many-arguments,too-many-positional-arguments
import json
import re
import requests
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

    def entry_info(self, key=None):
        """Hakee tietyn viitteen tiedot tietokannasta."""
        row = self.db_manager.get_reference(key=key)
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

        # Muutetaan syöte listaksi
        choices = [x.strip() for x in arvot.split(",")]

        rows = self.db_manager.filter_references_db(choices)
        return [self._row_to_reference(r) for r in rows]

    def edit_entry(self, entry_type, target_key, **kwargs):
        """Muokkaa tietyn viitteen tietoja tietokannassa."""
        self.db_manager.edit_entry(entry_type, target_key, **kwargs)

    def delete_entry(self, target_key):
        """Poistaa tietyn viitteen tietokannassa."""
        self.db_manager.delete_entry(target_key)

    def add_entry(self, entry_type, key, other_elements = None, tags=None):
        """Lisää uuden viitteen tietokantaan."""
        if other_elements is None:
            other_elements = {}
        if tags is None:
            tags = []
        entry = Reference(entry_type, key, other_elements)
        return self.db_manager.insert_reference(entry, tags)

    def export_bibtex(self, filename): # pylint: disable=too-many-locals #TODO too many?
        """Vie kaikki viitteet BibTeX-tiedostoon."""
        references = self.db_manager.get_reference()

        with open(filename, "w", encoding="utf-8") as f:
            for row in references:
                _, ref_type, key, raw_fields = row

                fields = json.loads(raw_fields) if raw_fields else {}

                f.write(f"@{ref_type}{{{key},\n")

                for name, value in fields.items():
                    f.write(f"  {name} = {{{value}}},\n")

                f.write("}\n\n")

    def fetch_reference_by_doi(self, doi):
        """Hakee viitteen Crossrefistä ja palauttaa Reference-oliona."""
        url = f"https://api.crossref.org/works/{doi}"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"DOI-haku epäonnistui: {e}")
            return None
        except Exception as e:
            print(f"Odottamaton virhe DOI-haussa: {e}")
            return None

        data = response.json().get("message", {})

        # Authors
        author_list = data.get("author", [])
        if author_list:
            authors = " and ".join(
                f"{a.get('family','')}, {a.get('given','')}"
                for a in author_list
            )
        else:
            authors = "-"  # oletusarvo
        title = data.get("title", ["-"])[0]
        year = data.get("issued", {}).get("date-parts", [[0]])[0][0]
        journal = data.get("container-title", ["-"])[0]
        volume = data.get("volume", "-")
        pages = data.get("page", "-")

        # Rakennetaan other_fields-dict
        other_fields = {
            "author": authors,
            "title": title,
            "journal": journal,
            "year": year,
            "volume": volume,
            "pages": pages
        }

        return Reference(
            ref_type="article",
            key=doi,
            other_fields=other_fields
        )

    def fetch_reference_by_url(self, url):
        """Hakee URL:n ja yrittää löytää DOI:n sivulta."""

        try:
            response = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            response.raise_for_status()
        except requests.RequestException:
            return None

        html = response.text

        # 1) Etsi doi.org linkki sivulta
        match = re.search(
            r"doi\.org/(10\.\d{4,9}/[^\s\"\'<>]+)",
            html,
            re.IGNORECASE
        )
        if match:
            doi = match.group(1).rstrip(").,;")
            return self.fetch_reference_by_doi(doi)

        # 2) Fallback: etsitään DOI tekstinä
        match = re.search(
            r"\b(10\.\d{4,9}/[^\s\"\'<>]+)\b",
            html
        )
        if match:
            doi = match.group(1).rstrip(").,;")
            return self.fetch_reference_by_doi(doi)

        return None
