"""Testit ReferenceManager-luokalle"""
import unittest
import os
from repositories.viite_repository import ReferenceManager

class TestReferenceManager(unittest.TestCase):
    """Testaa ReferenceManager-luokan toiminnallisuuksia."""
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
        self.ref.add_book(
            key="TEST1",
            author="Test author1",
            title="Test title1",
            year=2021,
            publisher="Test publisher1"
        )

        # Lisättävä artikkeli
        self.ref.add_article(
            key="TEST2",
            author="Test author2",
            title="Test title2",
            journal="Test journal2",
            year=2022,
            volume="2",
            pages="2"
        )

        # Lisättävä konferenssijulkaisu
        self.ref.add_inproceeding(
            key="TEST3",
            author="Test author3",
            title="Test title3",
            year=2023,
            booktitle="Test booktitle3"
        )


    def tearDown(self):
        if os.path.exists("test.db"):
            os.remove("test.db")


    def test_add_entries(self):
        """Tarkistetaan että setUpissa luodut lisättävät päätyivät tietokantaan"""
        self.assertEqual(str(self.ref.listaa()), "Inproceedings:\n"+
        "(1, 'TEST3', 'Test author3', 'Test title3', 2023, 'Test booktitle3')\n" +
        "tagit: \n\n\n" +
        "Articles:\n" +
        "(1, 'TEST2', 'Test author2', 'Test title2', 'Test journal2', 2022, 2, '2')\n\n"
        "Books:\n" +
        "(1, 'TEST1', 'Test author1', 'Test title1', 2021, 'Test publisher1')\n" +
        "tagit: \n\n")


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
        self.assertIn("@inproceedings{TEST3,", content)
        self.assertIn("author = {Test author3}", content)
        self.assertIn("booktitle = {Test booktitle3}", content)

        self.assertIn("@article{TEST2,", content)
        self.assertIn("journal = {Test journal2}", content)

        self.assertIn("@book{TEST1,", content)
        self.assertIn("publisher = {Test publisher1}", content)


    def test_delete_entry_finds_thing(self):
        """Testataan viite_repositoryn delete_entry-metodia niin että poistettava löytyy."""
        self.ref.delete_entry("book", "TEST1")
        self.assertEqual(str(self.ref.listaa()), "Inproceedings:\n" +
        "(1, 'TEST3', 'Test author3', 'Test title3', 2023, 'Test booktitle3')\n" +
        "tagit: \n\n\n" +
        "Articles:\n" +
        "(1, 'TEST2', 'Test author2', 'Test title2', 'Test journal2', 2022, 2, '2')\n\n" +
        "Books:\n")


    def test_delete_entry_doesnt_find(self):
        """Testataan viite_repositoryn delete_entry-metodia että poistettava ei löydy."""
        self.ref.delete_entry("book", "TEST2")
        self.assertEqual(str(self.ref.listaa()), "Inproceedings:\n" +
        "(1, 'TEST3', 'Test author3', 'Test title3', 2023, 'Test booktitle3')\n" +
        "tagit: \n\n\n" +
        "Articles:\n" +
        "(1, 'TEST2', 'Test author2', 'Test title2', 'Test journal2', 2022, 2, '2')\n\n" +
        "Books:\n" +
        "(1, 'TEST1', 'Test author1', 'Test title1', 2021, 'Test publisher1')\n" +
        "tagit: \n\n")


    def test_edit_entry(self):
        """Testataan viite_repositoryn edit_entry-metodia, että osaa muokata."""
        self.ref.edit_entry("article", "TEST2", author="Pyyttoni", year=1899)
        self.assertEqual(str(self.ref.listaa()), "Inproceedings:\n" +
        "(1, 'TEST3', 'Test author3', 'Test title3', 2023, 'Test booktitle3')\n" +
        "tagit: \n\n\n" +
        "Articles:\n" +
        "(1, 'TEST2', 'Pyyttoni', 'Test title2', 'Test journal2', 1899, 2, '2')\n\n" +
        "Books:\n" +
        "(1, 'TEST1', 'Test author1', 'Test title1', 2021, 'Test publisher1')\n" +
        "tagit: \n\n")


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
