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
                print("lisää(kirja)")
                #Lisää vain kirjan
                try:
                    key = self.io.read("Lisää key(String): ").strip()
                    author = self.io.read("Lisää author(String): ").strip()
                    title = self.io.read("Lisää title(String): ").strip()
                    year = self.io.read("Lisää year(Int): ").strip()
                    publisher = self.io.read("Lisää publisher(String): ").strip()
                    self.reference_manager.add_book(key, author, title, year, publisher)
                    print("Lisäys onnistunut")
                except Exception as error:
                    self.io.write(str(error)) #TODO: Ei todennäköisesti toimi?

            elif choice == "2":
                print("listaa")
                self.reference_manager.listaa()
            elif choice == "3":
                print("bibtex")
            elif choice == "4":
                break
            else:
                self.io.write("Virheellinen valinta")