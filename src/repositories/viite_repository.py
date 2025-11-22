from entities.refobj import Article, Inproceeding, Book

VPL11 = Inproceeding(
    key="VPL11",
    author="Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti",
    title="Extreme Apprenticeship Method in Teaching Programming for Beginners.",
    year=2011,
    booktitle="SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium on Computer science education"
)

CBH91 = Article(
    key="CBH91",
    author="Allan Collins and John Seely Brown and Ann Holum",
    title="Cognitive apprenticeship: making thinking visible",
    journal="American Educator",
    year=1991,
    volume=6,
    pages="38--46"
)

Martin09 = Book(
    key="Martin09",
    author="Martin, Robert",
    title="Clean Code: A Handbook of Agile Software Craftsmanship",
    year=2008,
    publisher="Prentice Hall"
)

entries = [VPL11, CBH91, Martin09]

class Reference_manager:
    def __init__(self, references=None):
        if references is None:
            references = entries.copy() #[] testi data
        self.references = references

    def listaa(self):
        for index, ref in enumerate(self.references, start=1):
            print(f"{index}) avain: {ref.key}\nauthor: {ref.author}\n")


    def add_book(self, key, author, title, year, publisher):
        return self.add_reference(Book(key, author, title, year, publisher))
    
    def add_article(self, key, author, title, journal, year, booktitle):
        return self.add_reference(Article(key, author, title, journal, year, booktitle))
    
    def add_inproceeding(self, key, author, title, year, booktitle):
        return self.add_reference(Inproceeding(key, author, title, year, booktitle))

    def add_reference(self, ref):
        if ref:
            self.references.append(ref)
        


def main():
    reference = Reference_manager()
    print(reference)

if __name__ == "__main__":
    main()
