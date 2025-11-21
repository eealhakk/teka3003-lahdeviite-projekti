class Inproceeding:
    def __init__(self, key, author = "", title = "", year = 0, booktitle = ""):
        self.key = key
        self.author = author
        self.title = title
        self.year = year
        self.booktitle = booktitle


class Article:
    def __init__(self, key, author = "", title = "", journal = 0, year = 0, volume = 0, pages = 0):
        self.key = key
        self.author = author
        self.title = title
        self.journal = journal
        self.year = year
        self.volume = volume
        self.pages = pages


class Book:
    def __init__(self, key = "", author = "", title = "", year = 0, publisher = ""):
        self.key = key
        self.author = author
        self.title = title
        self.year = year
        self.publisher = publisher


class Reference:
    def __init__(self, type = []):
        self.type = [type]

    def add_reference():
        return
    
        
    



##==========================================================================================
##Data

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

def main():

    uKirja = Book("key1", "Kissan .byb", "Cook book", 2002, "WSOY")
    reference = Reference(Martin09)


if __name__ == "__main__":
    main()
