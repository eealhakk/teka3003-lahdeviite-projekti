"""Testit ReferenceManager-luokalle"""
import sqlite3
import unittest
import os
from repositories.viite_repository import ReferenceManager

class TestReferenceManager(unittest.TestCase):
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
        self.assertEqual(str(self.ref.listaa()), "Inproceedings:\n" +
        "(1, 'TEST3', 'Test author3', 'Test title3', 2023, 'Test booktitle3')\n\n" +
        "Articles:\n" +
        "(1, 'TEST2', 'Test author2', 'Test title2', 'Test journal2', 2022, 2, '2')\n\n" +
        "Books:\n" +
        "(1, 'TEST1', 'Test author1', 'Test title1', 2021, 'Test publisher1')\n")

    
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
