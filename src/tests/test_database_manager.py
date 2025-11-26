"""Testit DatabaseManager-luokan tietokantataulujen luonnille"""
import sqlite3
import unittest
from repositories.database_manager import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    """Luokka jossa unittestit DatabaseManager-luokan funktioille"""

    def test_tables_created(self):
        """Testaa, että DatabaseManager luo kaikki tarvittavat taulut"""
        # Luodaan väliaikainen tietokantatiedosto
        self.db_file = "test.db"

        DatabaseManager(self.db_file)

        conn = sqlite3.connect(self.db_file)
        cur = conn.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        table_names = {row[0] for row in cur.fetchall()}
        conn.close()

        #Varmistetaan, että kaikki odotetut taulut ovat olemassa
        assert "inproceeding" in table_names
        assert "article" in table_names
        assert "book" in table_names