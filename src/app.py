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
            self.io.write("\n=== Valiste toiminto ===")
            self.io.write("1) Lisää uusi viite")
            self.io.write("2) Listaa kaikki viitteet")
            self.io.write("3) Vie BibTeX-tiedosto")
            self.io.write("4) Muokkaa viitettä")
            self.io.write("5) Lopeta\n")

            choice = self.io.read("Valinta: ").strip()

            if choice == "1":
                self.add_reference()
            elif choice == "2":
                self.reference_manager.listaa()
            elif choice == "3":
                self.io.write("Coming soon...")
                #self.reference_manager.export_bibtex()
            elif choice == "4":
                self.edit_reference()
            elif choice == "5":
                break
            else:
                self.io.write("Virheellinen valinta")

    def edit_reference(self):
        """Metodi lähteen muokkaamiseen"""
        ref_type = self.ask_type()
        if not ref_type:
            return

        key_editing = self.io.read("Anna muokattavan viitteen BibTeX-avain: ").strip()
        muokattava = self.reference_manager.entry_info(ref_type, str(key_editing))

        if not muokattava:
            self.io.write("Viitettä ei löydy.")
            return
        self.io.write("\n"+str(muokattava)+"\n")

        fields = self.io.read("Anna kentät, joita haluat muokata erotettuna pilkulla: ").strip()
        allowed_fields = vars(muokattava).keys()

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

        if ref_type == "inproceeding":
            author = self.io.read("Author: ").strip()
            title = self.io.read("Title: ").strip()
            year = self.io.read("Year: ").strip()
            booktitle = self.io.read("Booktitle: ").strip()
            self.reference_manager.add_inproceeding(key, author, title, year, booktitle)

        elif ref_type == "article":
            author = self.io.read("Author: ").strip()
            title = self.io.read("Title: ").strip()
            journal = self.io.read("Journal: ").strip()
            year = self.io.read("Year: ").strip()
            volume = self.io.read("Volume: ").strip()
            pages = self.io.read("Pages: ").strip()
            self.reference_manager.add_article(key, author, title, journal, year, volume, pages)

        elif ref_type == "book":
            author = self.io.read("Author: ").strip()
            title = self.io.read("Title: ").strip()
            year = self.io.read("Year: ").strip()
            publisher = self.io.read("Publisher: ").strip()
            self.reference_manager.add_book(key, author, title, year, publisher)

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
        else:
            self.io.write("Virheellinen valinta")
            return None
