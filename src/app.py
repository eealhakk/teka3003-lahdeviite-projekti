
class App:
    def __init__(self, io):
        self.io = io

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
                print("lisää")
            elif choice == "2":
                print("listaa")
            elif choice == "3":
                print("bibtex")
            elif choice == "4":
                break
            else:
                self.io.write("Virheellinen valinta")