"""Testit ReferenceManager-luokalle"""
import sqlite3
from repositories.viite_repository import ReferenceManager

def test_add_book(tmp_path):
    """Testaa kirjan lisäämisen"""
    # Luodaan väliaikainen tietokantatiedosto
    db_file = tmp_path / "test.db"

    # Luodaan ReferenceManager käyttäen tätä tietokantaa
    ref = ReferenceManager()
    ref.db_manager.db_name = str(db_file)  # vaihdetaan tietokanta testiin
    ref.db_manager.create_database()       # luodaan taulut

    # Lisättävä kirja
    ref.add_book(
        key="TEST1",
        author="Test author",
        title="Test title",
        year=2020,
        publisher="Test publisher"
    )

    # Tarkistetaan että kirja päätyi tietokantaan
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute("SELECT key, author, title, year, publisher FROM book WHERE key='TEST1';")
    result = cur.fetchone()

    assert result == ("TEST1", "Test author", "Test title", 2020, "Test publisher")

def test_add_article(tmp_path):
    """Testaa artikkelin lisäämisen"""
    # Luodaan väliaikainen tietokantatiedosto
    db_file = tmp_path / "test.db"

    # Luodaan ReferenceManager käyttäen tätä tietokantaa
    ref = ReferenceManager()
    ref.db_manager.db_name = str(db_file)  # vaihdetaan tietokanta testiin
    ref.db_manager.create_database()       # luodaan taulut

    # Lisättävä artikkeli
    ref.add_article(
        key="TEST1",
        author="Test author",
        title="Test title",
        journal="Test journal",
        year=2020,
        volume="test",
        pages="test"
    )

    # Tarkistetaan että artikkeli päätyi tietokantaan
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    cur.execute(
        "SELECT key, author, title, journal, year, volume, pages "
        "FROM article WHERE key='TEST1';"
    )
    result = cur.fetchone()

    assert result == ("TEST1", "Test author", "Test title", "Test journal", 2020, "test", "test")
