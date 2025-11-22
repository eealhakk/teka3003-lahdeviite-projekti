from repositories.viite_repository import Reference_manager

class App:
    def __init__(self, io):
        self.io = io
        self.reference_manager = Reference_manager()

    def run(self):
        while True:
            print("""
=== OTSIKKO ===
1) Lisää uusi viite
2) Listaa kaikki viitteet
3) Vie BibTeX-tiedosto
4) Lopeta
""")
            choice = self.io.read("Valinta: ").strip()

            if choice == "1":
                self.add_reference()
            elif choice == "2":
                self.reference_manager.listaa()
            elif choice == "3":
                self.reference_manager.export_bibtex()
            elif choice == "4":
                break
            else:
                self.io.write("Virheellinen valinta")

    def add_reference(self):
        print("Valitse viitetyyppi:")
        print("1) Inproceedings")
        print("2) Article")
        print("3) Book")

        type_choice = self.io.read("Tyyppi: ").strip()

        if type_choice == "1":
            ref_type = "inproceedings"
        elif type_choice == "2":
            ref_type = "article"
        elif type_choice == "3":
            ref_type = "book"
        else:
            self.io.write("Virheellinen valinta")
            return

        key = self.io.read("BibTeX-avain: ").strip()

        if ref_type == "inproceedings":
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
