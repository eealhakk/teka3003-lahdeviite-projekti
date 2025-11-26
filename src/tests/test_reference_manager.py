"""Testit ReferenceManager-luokalle"""
import sqlite3
import unittest
from repositories.viite_repository import ReferenceManager

class TestReferenceManager(unittest.TestCase):
    def setUp(self):
        """Luodaan testisetuppi ReferenceManagerin testaamiseksi."""
        # Luodaan väliaikainen tietokantatiedosto
        self.db_file = "test.db"

        # Luodaan ReferenceManager käyttäen tätä tietokantaa
        self.ref = ReferenceManager(self.db_file)


        # Lisättävä kirja
        self.ref.add_book(
            key="TEST1",
            author="Test author2",
            title="Test title2",
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


    def test_add_book(self):
        # Tarkistetaan että kirja päätyi tietokantaan
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute("SELECT key, author, title, year, publisher FROM book WHERE key='TEST1';")
        result = cur.fetchone()

        assert result == ("TEST1", "Test author", "Test title", 2020, "Test publisher")

    def test_add_article(self):

        # Tarkistetaan että artikkeli päätyi tietokantaan
        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()
        cur.execute(
            "SELECT key, author, title, journal, year, volume, pages "
            "FROM article WHERE key='TEST1';"
        )
        result = cur.fetchone()

        assert result == ("TEST1", "Test author", "Test title", "Test journal", 2020, "test", "test")
