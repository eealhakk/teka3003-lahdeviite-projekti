"""Testit ReferenceManager-luokalle"""
import unittest
import os
from repositories.viite_repository import ReferenceManager

class TestReferenceManager(unittest.TestCase):
    """Testaa ReferenceManager-luokan toiminnallisuuksia."""

    maxDiff = None

    def setUp(self):
        """Luodaan testisetuppi ReferenceManagerin testaamiseksi."""
        # Poistetaan väliaikainen tietokantatiedosto, jos sellainen on jääny
        # edeltävistä testeistä
        if os.path.exists("test.db"):
            os.remove("test.db")

        # Luodaan väliaikainen tietokantatiedosto
        self.db_file = "test.db"

        # Luodaan ReferenceManager käyttäen tätä tietokantaa
        self.ref = ReferenceManager(self.db_file)


        # Lisättävä kirja
        self.ref.add_entry(
            entry_type="book",
            key="Martin09",
            other_elements={"author": "Martin, Robert",
                    "title": "Clean Code: A Handbook of Agile Software Craftsmanship",
                    "year": 2008,
                    "publisher": "Prentice Hall"}
        )

        # Lisättävä artikkeli
        self.ref.add_entry(
            entry_type="article",
            key="CBH91",
            other_elements={"author": "Allan Collins and John Seely Brown and Ann Holum",
                    "title": "Cognitive apprenticeship: making thinking visible",
                    "journal": "American Educator",
                    "year": 1991,
                    "volume": 6,
                    "pages": "38--46"}
        )


    def tearDown(self):
        if os.path.exists("test.db"):
            os.remove("test.db")


    def test_add_entries(self):
        """Tarkistetaan että setUpissa luodut lisättävät päätyivät tietokantaan"""
        refs = self.ref.listaa()
        self.assertEqual(len(refs), 2)
        #Pistin tarkistamaan vaan avaimet, kun tuntui turhalta kirjoittaa kaikki tiedot
        keys = [r[1].key for r in refs]
        self.assertEqual(keys, ["Martin09", "CBH91"])


    def test_add_entries_with_and_without_tags(self):
        """Luodaan tageilla ja tageitta olevia entryjä, että tulee testattua
        koodin 'if tags is None' -rivien haarautumiset."""

        # Lisättävä luentomuistiinpano
        self.ref.add_entry(
            entry_type="lecturenote",
            key="Lappalainen2022",
            other_elements={"author": "Lappalainen, Vesa",
                    "title": "Ohjelmointi 2 -kurssin luentomuistiinpanot",
                    "year": 2022,
                    "publisher": "Jyväskylän yliopistopaino",
                    "course": "Ohjelmointi 2"}
        )

        # Lisättävä konferenssijulkaisu
        self.ref.add_entry(
            entry_type="inproceeding",
            key="VPL11",
            other_elements={"author": "Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti",
                    "title": "Extreme Apprenticeship Method in Teaching Programming for Beginners.",
                    "year": 2011,
                    "booktitle": ("SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium "
                                 "on Computer science education")},
            tags=["Vesamainen", "Eeppinen", "klassikko"]
        )

        refs = self.ref.listaa()
        self.assertEqual(len(refs), 4)

        # Tarkistetaan että uudet keyt löytyvät
        keys = [ref[1].key for ref in refs]
        # Laitoin nämä nyt tarkistamaan pelkät avaimet
        self.assertIn("Lappalainen2022", keys)
        self.assertIn("VPL11", keys)


    def test_export_bibtex(self):
        """Testaa export_bibtex-metodia"""
        bib_file = "test_bibtex.bib"
        self.ref.export_bibtex(bib_file)

        # Tarkistetaan, että tiedosto luotiin
        self.assertTrue(os.path.exists(bib_file))

        # Luetaan tiedoston sisältö
        with open(bib_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Tarkistetaan, että BibTeX-merkinnät löytyvät
        self.assertIn("@book{Martin09,", content)
        self.assertIn("author = {Martin, Robert}", content)
        self.assertIn("title = {Clean Code: A Handbook of Agile Software Craftsmanship}", content)

        self.assertIn("@article{CBH91,", content)
        self.assertIn("journal = {American Educator}", content)


    def test_delete_entry_finds_thing(self):
        """Testataan viite_repositoryn delete_entry-metodia niin että poistettava löytyy."""
        self.ref.delete_entry("book", "TEST1")
        self.assertEqual(str(self.ref.listaa()), "Inproceedings:\n" +
        "(1, 'TEST3', 'Test author3', 'Test title3', 2023, 'Test booktitle3')\n" +
        "tagit: \n\n\n" +
        "Articles:\n" +
        "(1, 'TEST2', 'Test author2', 'Test title2', 'Test journal2', 2022, 2, '2')\n" +
        "tagit: mahtava\n\n\n"
        "Books:\n")


    def test_delete_entry_doesnt_find(self):
        """Testataan viite_repositoryn delete_entry-metodia että poistettava ei löydy."""
        self.ref.delete_entry("book", "TEST2")
        self.assertEqual(str(self.ref.listaa()), "Inproceedings:\n" +
        "(1, 'TEST3', 'Test author3', 'Test title3', 2023, 'Test booktitle3')\n" +
        "tagit: \n\n\n" +
        "Articles:\n" +
        "(1, 'TEST2', 'Test author2', 'Test title2', 'Test journal2', 2022, 2, '2')\n" +
        "tagit: mahtava\n\n\n"
        "Books:\n" +
        "(1, 'TEST1', 'Test author1', 'Test title1', 2021, 'Test publisher1')\n" +
        "tagit: hieno, mahtava\n\n")


    def test_edit_entry(self):
        """Testataan viite_repositoryn edit_entry-metodia, että osaa muokata."""
        self.ref.edit_entry("article", "TEST2", author="Pyyttoni", year=1899)
        self.assertEqual(str(self.ref.listaa()), "Inproceedings:\n" +
        "(1, 'TEST3', 'Test author3', 'Test title3', 2023, 'Test booktitle3')\n" +
        "tagit: \n\n\n" +
        "Articles:\n" +
        "(1, 'TEST2', 'Pyyttoni', 'Test title2', 'Test journal2', 1899, 2, '2')\n" +
        "tagit: mahtava\n\n\n"
        "Books:\n" +
        "(1, 'TEST1', 'Test author1', 'Test title1', 2021, 'Test publisher1')\n" +
        "tagit: hieno, mahtava\n\n")


    def test_entry_info_finds(self):
        """Testataan viite_repositoryn yksittäisen kohteen tiedot palauttavaa entry_info-metodia"""
        self.assertEqual(str(self.ref.entry_info("inproceeding", "TEST3")), "key=TEST3\n" +
                         "author=Test author3\n" +
                         "title=Test title3\n" +
                         "year=2023\n" +
                         "booktitle=Test booktitle3")


    def test_entry_info_doesnt_find_entry_type(self):
        """Testataan viite_repositoryn yksittäisen kohteen tiedot palauttavaa entry_info-metodia
        niin, ettei löydy haluttua kohdetta."""
        self.assertEqual(str(self.ref.entry_info("inproceedingdong", "TEST3")), "None")


    def test_entry_info_doesnt_find_key(self):
        """Testataan viite_repositoryn yksittäisen kohteen tiedot palauttavaa entry_info-metodia
        niin, ettei löydy haluttua kohdetta."""
        self.assertEqual(str(self.ref.entry_info("inproceeding", "TEST2")), "None")


    def test_get_references_by_tag(self):
        """Testataan kaikki halutun tagin omaavien viitteiden hakeminen"""
        self.assertEqual(str(self.ref.get_references_by_tag("mahtava")),
                         "[('article', (1, 'TEST2', 'Test author2', 'Test title2', " +
                         "'Test journal2', 2022, 2, '2')), ('book', (1, 'TEST1', " +
                         "'Test author1', 'Test title1', 2021, 'Test publisher1'))]")


    def test_filter_references(self):
        """Testaa että filter_references_db palauttaa oikean stringin (Book + key + author)."""

        # 3 = Book, 4 = key, 5 = author
        result = self.ref.db_manager.filter_references_db([3, 4, 5])

        self.assertIn("Book", result)

        self.assertIn("key: TEST1", result)
        self.assertIn("author: Test author1", result)

        self.assertNotIn("year:", result)
        self.assertNotIn("publisher:", result)


    def test_filter_references_bad_input(self):
        """Testataan palauttaako virheen yritettäessä laittaa huonoa syötettä."""
        self.assertEqual(self.ref.filter_references("lol"),
                         "Virheellinen syöte. Käytä numeroita pilkuilla eroteltuna.\n")
