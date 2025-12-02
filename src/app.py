"""App-moduuli ohjelman toiminnoille"""
from repositories.viite_repository import ReferenceManager

class App:
    """App luokka, jossa ohjelman metodit"""
    def __init__(self, io):
        self.io = io
        self.reference_manager = ReferenceManager()

    def run(self):
        """Metodi joka kysyy käyttäjältä haluttua toimintoa"""
        while True:
            self.io.write("\n=== Valitse toiminto ===")
            self.io.write("1) Lisää uusi viite")
            self.io.write("2) Listaa viitteet")
            self.io.write("3) Vie BibTeX-tiedosto")
            self.io.write("4) Muokkaa viitettä")
            self.io.write("5) Poista viite")
            self.io.write("6) Lopeta\n")

            choice = self.io.read("Valinta: ").strip()

            if choice == "1":
                self.add_reference()
            elif choice == "2":
                self.list_references()
            elif choice == "3":
                self.reference_manager.export_bibtex("references.bib")
                self.io.write("BibTeX-tiedosto references.bib luotu")
            elif choice == "4":
                self.edit_reference()
            elif choice == "5":
                self.delete_reference()
            elif choice == "6":
                break
            else:
                self.io.write("Virheellinen valinta")

    def list_references(self):
        """Metodi viitteiden listaamiseen"""
        self.io.write("\n1) Listaa tagin perusteella")
        self.io.write("2) Listaa kaikki\n")
        value = self.io.read("Valinta: ").strip()

        if value == "1":
            search_tag = str(self.io.read("Anna tagi: ").strip())
            found_references = self.reference_manager.get_references_by_tag(search_tag)

            if not found_references:
                self.io.write("Ei löytyneitä viitteitä tälle tagille.")
                return

            listing = f"Löydetyt viitteet tagille '{search_tag}':\n\n"
            for ref in found_references:
                ref_object = self.reference_manager.entry_info(ref[0], str(ref[1][1]))
                listing += str(ref_object) + "\n\n"
            self.io.write("\n"+listing)
        elif value == "2":
            print(self.reference_manager.listaa())
        else:
            self.io.write("Virheellinen valinta")

    def delete_reference(self):
        """Metodi lähteen poistamiseen"""

        ref_type = self.ask_type()
        if not ref_type:
            return

        key_editing = self.io.read("Anna poistettavan viitteen BibTeX-avain: ").strip()
        poistettava = self.reference_manager.entry_info(ref_type, str(key_editing))

        if not poistettava:
            self.io.write("Viitettä ei löydy.")
            return
        self.io.write("\n"+str(poistettava)+"\n")

        self.io.write("Haluatko varmasti poistaa viitteen? (K/E)")
        choice = self.io.read("Valinta: ").strip().upper()

        if choice == "K":
            self.reference_manager.delete_entry(ref_type, key_editing)
            self.io.write("Viite poistettu!")
        elif choice == "E":
            return

    def edit_reference(self):
        """Metodi lähteen muokkaamiseen"""
        ref_type = self.ask_type()
        if not ref_type:
            return

        key_editing = self.io.read("Anna muokattavan viitteen BibTeX-avain: ").strip()
        ref_editing = self.reference_manager.entry_info(ref_type, str(key_editing))

        if not ref_editing:
            self.io.write("Viitettä ei löydy.")
            return
        self.io.write("\n"+str(ref_editing)+"\n")

        fields = self.io.read("Anna kentät, joita haluat muokata erotettuna pilkulla: ").strip()
        allowed_fields = vars(ref_editing).keys()

        for field in fields.split(","):
            field = field.strip()
            if field not in allowed_fields:
                self.io.write(f"'{field}' ei ole sallittu.")
                return

        new_values = {}
        for field in fields.split(","):
            field = field.strip()
            new_value = self.io.read(f"Anna uusi arvo kentälle '{field}': ").strip()
            new_values[field] = new_value

        self.reference_manager.edit_entry(ref_type, key_editing, **new_values)
        self.io.write("Viite päivitetty!")

    def add_reference(self):
        """Metodi lähteen lisäämiseen"""
        ref_type = self.ask_type()
        if not ref_type:
            return

        key = self.io.read("BibTeX-avain: ").strip()

        if self.reference_manager.entry_info(ref_type, str(key)):
            self.io.write("Bibtex-koodi on jo käytössä!")
            return

        def ask_tags():
            tags_input = self.io.read("Tagit (valinnainen, erottele pilkulla): ").strip()
            return [tag.strip() for tag in tags_input.split(",")] if tags_input else []

        if ref_type == "inproceeding":
            author = self.io.read("Author: ").strip()
            title = self.io.read("Title: ").strip()
            year = self.io.read("Year: ").strip()
            booktitle = self.io.read("Booktitle: ").strip()
            tags = ask_tags()
            self.reference_manager.add_inproceeding(key, author, title, year, booktitle, tags)

        elif ref_type == "article":
            author = self.io.read("Author: ").strip()
            title = self.io.read("Title: ").strip()
            journal = self.io.read("Journal: ").strip()
            year = self.io.read("Year: ").strip()
            volume = self.io.read("Volume: ").strip()
            pages = self.io.read("Pages: ").strip()
            tags = ask_tags()
            self.reference_manager.add_article(
                key, author, title, journal, year, volume, pages, tags
            )

        elif ref_type == "book":
            author = self.io.read("Author: ").strip()
            title = self.io.read("Title: ").strip()
            year = self.io.read("Year: ").strip()
            publisher = self.io.read("Publisher: ").strip()
            tags = ask_tags()
            self.reference_manager.add_book(key, author, title, year, publisher, tags)

        self.io.write(f"{ref_type}-viite lisätty!")

    def ask_type(self):
        """Metodi lähteen tyypin valintaan"""
        self.io.write("\n=== Valitse viitetyyppi ===")
        self.io.write("1) Inproceedings")
        self.io.write("2) Article")
        self.io.write("3) Book\n")

        type_choice = self.io.read("Tyyppi: ").strip()

        if type_choice == "1":
            return "inproceeding"
        if type_choice == "2":
            return "article"
        if type_choice == "3":
            return "book"
        self.io.write("Virheellinen valinta")
        return None
