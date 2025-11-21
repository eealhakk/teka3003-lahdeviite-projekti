data = """@inproceedings{VPL11,
            author = {Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti},
            title = {Extreme Apprenticeship Method in Teaching Programming for Beginners.},
            year = {2011},
            booktitle = {SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium on Computer science education},
        }
        
        @article{CBH91,
            author = {Allan Collins and John Seely Brown and Ann Holum},
            title = {Cognitive apprenticeship: making thinking visible},
            journal = {American Educator},
            year = {1991},
            volume = {6},
            pages = {38--46}
        }
        
        @book{Martin09,
            author = {Martin, Robert},
            title = {Clean Code: A Handbook of Agile Software Craftsmanship},
            year = {2008},
            publisher = {Prentice Hall},
        }
        """


keywords = ["VPL11", "TST2023"]
authors = ["kissa", "koira"]
titles = ["title1", "title2"]
yers = [2012, 2015, 2025]
booktitles = []

class Reference:
    def __init__(self, type, place):
        self.type = type
        self.place = place


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
