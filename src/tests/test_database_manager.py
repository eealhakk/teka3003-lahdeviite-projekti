"""Testit DatabaseManager-luokan tietokantataulujen luonnille"""
import sqlite3
from repositories.viite_repository import DatabaseManager

def test_tables_created(tmp_path):
    """Testaa, että DatabaseManager luo kaikki tarvittavat taulut"""

    #Luodaan väliaikaisen kansion sisään uusi tyhjä tietokantatiedosto
    db_file = tmp_path / "test.db"

    #Alustetaan DatabaseManager, joka luo taulut automaattisesti
    DatabaseManager(db_name=str(db_file))

    #Avataan yhteys tietokantaan, jotta voidaan tarkistaa taulujen olemassaolo
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    #Haetaan kaikki tietokantaan luodut taulut sqlite_master-metataulusta
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    table_names = {row[0] for row in cur.fetchall()}

    #Varmistetaan, että kaikki odotetut taulut ovat olemassa
    assert "inproceeding" in table_names
    assert "article" in table_names
    assert "book" in table_names
