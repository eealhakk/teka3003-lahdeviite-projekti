"""Testit ReferenceManager-luokalle"""
import unittest
import os
from unittest.mock import patch, Mock
from requests import RequestException
from repositories.viite_repository import ReferenceManager

from entities.refobj import Reference

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
                    "publisher": "Prentice Hall"},
            tags=["Agile", "Development"]
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
        testipaluuarvo = ''
        for reference in self.ref.listaa():
            reference_tags = self.ref.get_reference_tags(reference[0])
            testipaluuarvo += (f"---\n\n{reference[1]}\ntags: {reference_tags}")
        self.assertEqual(testipaluuarvo,
                         "---\n\n" +
                         "Type: book\n" +
                        "Key: Martin09\n" +
                        "author: Martin, Robert\n" +
                        "title: Clean Code: A Handbook of Agile Software Craftsmanship\n" +
                        "year: 2008\n" +
                        "publisher: Prentice Hall\n" +
                        "tags: ['Agile', 'Development']---\n\n" +
                        "Type: article\n" +
                        "Key: CBH91\n" +
                        "author: Allan Collins and John Seely Brown and Ann Holum\n" +
                        "title: Cognitive apprenticeship: making thinking visible\n" +
                        "journal: American Educator\n" +
                        "year: 1991\n" +
                        "volume: 6\n" +
                        "pages: 38--46\n" +
                        "tags: []")


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

        testipaluuarvo = ''
        for reference in self.ref.listaa():
            reference_tags = self.ref.get_reference_tags(reference[0])
            testipaluuarvo += (f"---\n\n{reference[1]}\ntags: {reference_tags}")
        self.assertEqual(testipaluuarvo,
                         "---\n\n" +
                         "Type: book\n" +
                        "Key: Martin09\n" +
                        "author: Martin, Robert\n" +
                        "title: Clean Code: A Handbook of Agile Software Craftsmanship\n" +
                        "year: 2008\n" +
                        "publisher: Prentice Hall\n" +
                        "tags: ['Agile', 'Development']---\n\n" +
                        "Type: article\n" +
                        "Key: CBH91\n" +
                        "author: Allan Collins and John Seely Brown and Ann Holum\n" +
                        "title: Cognitive apprenticeship: making thinking visible\n" +
                        "journal: American Educator\n" +
                        "year: 1991\n" +
                        "volume: 6\n" +
                        "pages: 38--46\n" +
                        "tags: []---\n\n" +
                        "Type: lecturenote\n" +
                        "Key: Lappalainen2022\n" +
                        "author: Lappalainen, Vesa\n" +
                        "title: Ohjelmointi 2 -kurssin luentomuistiinpanot\n" +
                        "year: 2022\n" +
                        "publisher: Jyväskylän yliopistopaino\n" +
                        "course: Ohjelmointi 2\n" +
                        "tags: []---\n\n" +
                        "Type: inproceeding\n" +
                        "Key: VPL11\n" +
                        "author: Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti\n" +
                        "title: Extreme Apprenticeship Method in " +
                        "Teaching Programming for Beginners.\n" +
                        "year: 2011\n" +
                        "booktitle: SIGCSE '11: Proceedings of the 42nd SIGCSE technical " +
                        "symposium on Computer science education\n" +
                        "tags: ['Vesamainen', 'Eeppinen', 'klassikko']")


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
        self.ref.delete_entry("book", "Martin09")
        testipaluuarvo = ''
        for reference in self.ref.listaa():
            reference_tags = self.ref.get_reference_tags(reference[0])
            testipaluuarvo += (f"---\n\n{reference[1]}\ntags: {reference_tags}")
        self.assertEqual(testipaluuarvo,
                         "---\n\n" +
                        "Type: article\n" +
                        "Key: CBH91\n" +
                        "author: Allan Collins and John Seely Brown and Ann Holum\n" +
                        "title: Cognitive apprenticeship: making thinking visible\n" +
                        "journal: American Educator\n" +
                        "year: 1991\n" +
                        "volume: 6\n" +
                        "pages: 38--46\n" +
                        "tags: []")


    def test_delete_entry_doesnt_find(self):
        """Testataan viite_repositoryn delete_entry-metodia että poistettava ei löydy."""
        self.ref.delete_entry("book", "OhjTest")
        testipaluuarvo = ''
        for reference in self.ref.listaa():
            reference_tags = self.ref.get_reference_tags(reference[0])
            testipaluuarvo += (f"---\n\n{reference[1]}\ntags: {reference_tags}")
        self.assertEqual(testipaluuarvo,
                         "---\n\n" +
                         "Type: book\n" +
                        "Key: Martin09\n" +
                        "author: Martin, Robert\n" +
                        "title: Clean Code: A Handbook of Agile Software Craftsmanship\n" +
                        "year: 2008\n" +
                        "publisher: Prentice Hall\n" +
                        "tags: ['Agile', 'Development']---\n\n" +
                        "Type: article\n" +
                        "Key: CBH91\n" +
                        "author: Allan Collins and John Seely Brown and Ann Holum\n" +
                        "title: Cognitive apprenticeship: making thinking visible\n" +
                        "journal: American Educator\n" +
                        "year: 1991\n" +
                        "volume: 6\n" +
                        "pages: 38--46\n" +
                        "tags: []")


    def test_edit_entry(self):
        """Testataan viite_repositoryn edit_entry-metodia, että osaa muokata."""
        self.ref.edit_entry("article", "CBH91", author="Seely, Brown; Holum, Ann", year=2019)
        testipaluuarvo = ''
        for reference in self.ref.listaa():
            reference_tags = self.ref.get_reference_tags(reference[0])
            testipaluuarvo += (f"---\n\n{reference[1]}\ntags: {reference_tags}")
        self.assertEqual(testipaluuarvo,
                         "---\n\n" +
                         "Type: book\n" +
                        "Key: Martin09\n" +
                        "author: Martin, Robert\n" +
                        "title: Clean Code: A Handbook of Agile Software Craftsmanship\n" +
                        "year: 2008\n" +
                        "publisher: Prentice Hall\n" +
                        "tags: ['Agile', 'Development']---\n\n" +
                        "Type: article\n" +
                        "Key: CBH91\n" +
                        "author: Seely, Brown; Holum, Ann\n" +
                        "title: Cognitive apprenticeship: making thinking visible\n" +
                        "journal: American Educator\n" +
                        "year: 2019\n" +
                        "volume: 6\n" +
                        "pages: 38--46\n" +
                        "tags: []")



    def test_entry_info_finds(self):
        """Testataan viite_repositoryn yksittäisen kohteen tiedot palauttavaa entry_info-metodia"""
        self.assertEqual(str(self.ref.entry_info("book", "Martin09")),
                         "Type: book\n" +
                        "Key: Martin09\n" +
                        "author: Martin, Robert\n" +
                        "title: Clean Code: A Handbook of Agile Software Craftsmanship\n" +
                        "year: 2008\n" +
                        "publisher: Prentice Hall")


    def test_entry_info_doesnt_find_entry_type(self):
        """Testataan viite_repositoryn yksittäisen kohteen tiedot palauttavaa entry_info-metodia
        niin, ettei löydy haluttua kohdetta."""
        self.assertEqual(str(self.ref.entry_info("inproceeding", "Martin09")), "None")


    def test_entry_info_doesnt_find_key(self):
        """Testataan viite_repositoryn yksittäisen kohteen tiedot palauttavaa entry_info-metodia
        niin, ettei löydy haluttua kohdetta."""
        self.assertEqual(str(self.ref.entry_info("book", "CBH91")), "None")


    def test_get_references_by_tag(self):
        """Testataan kaikki halutun tagin omaavien viitteiden hakeminen"""
        self.assertEqual(str(self.ref.get_references_by_tag("Agile")),
                         "[(1, 'book', 'Martin09', '{\"author\": \"Martin, Robert\", \"title\": " +
                         "\"Clean Code: A Handbook of Agile Software Craftsmanship\", \"year\": " +
                         "2008, \"publisher\": \"Prentice Hall\"}')]")


    def test_get_references_by_tag_multiple(self):
        """Testataan kaikki halutun tagin omaavien viitteiden hakeminen (useampi tulos)"""
        self.ref.add_entry(
            entry_type="inproceeding",
            key="VPL11",
            other_elements={"author": "Vihavainen, Arto and Paksula, Matti and Luukkainen, Matti",
                    "title": "Extreme Apprenticeship Method in Teaching Programming for Beginners.",
                    "year": 2011,
                    "booktitle": ("SIGCSE '11: Proceedings of the 42nd SIGCSE technical symposium "
                                 "on Computer science education")},
            tags=["Vesamainen", "Eeppinen", "klassikko", "Development"]
        )

        self.assertEqual(str(self.ref.get_references_by_tag("Development")),
                         "[(1, 'book', 'Martin09', '{\"author\": \"Martin, Robert\", \"title\": " +
                         "\"Clean Code: A Handbook of Agile Software Craftsmanship\", \"year\": " +
                         "2008, \"publisher\": \"Prentice Hall\"}'), " +
                         "(3, 'inproceeding', 'VPL11', '{\"author\": \"Vihavainen, Arto and " +
                         "Paksula, Matti and Luukkainen, Matti\", \"title\": \"Extreme " +
                         "Apprenticeship Method in Teaching Programming for Beginners.\", \"" +
                         "year\": 2011, \"booktitle\": \"SIGCSE \\'11: Proceedings of the 42nd " +
                         "SIGCSE technical symposium on Computer science education\"}')]")


    def test_filter_references(self):
        """Testaa että filter_references_db palauttaa oikean stringin (Book + key + author)."""
        result = ''
        for reference in self.ref.filter_references("author,Martin, Robert"):
            reference_tags = self.ref.get_reference_tags(reference[0])
            result += (f"---\n\n{reference[1]}\ntags: {reference_tags}")
        self.assertEqual(result,
                         "---\n\n" +
                         "Type: book\n" +
                        "Key: Martin09\n" +
                        "author: Martin, Robert\n" +
                        "title: Clean Code: A Handbook of Agile Software Craftsmanship\n" +
                        "year: 2008\n" +
                        "publisher: Prentice Hall\n" +
                        "tags: ['Agile', 'Development']")


    def test_filter_references_bad_input(self):
        """Testataan palauttaako tyhjän yritettäessä laittaa huonoa syötettä."""
        self.assertEqual(str(self.ref.filter_references("lol")),
                         "[]")


    @patch("repositories.viite_repository.requests.get")
    def test_fetch_reference_by_doi_success(self, mock_get):
        """Testaa onnistuneen DOI-haun ja Reference-olion palautuksen"""

        fake_response = {
            "message": {
                "author": [
                    {"family": "Mallory-Kani", "given": "Amy"}
                ],
                "title": ["Example Article"],
                "issued": {"date-parts": [[2015]]},
                "container-title": ["European Romantic Review"],
                "volume": "26",
                "page": "699-717"
            }
        }

        mock_resp = Mock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = fake_response
        mock_get.return_value = mock_resp

        doi = "10.1080/10509585.2015.1092083"
        ref = self.ref.fetch_reference_by_doi(doi)

        self.assertIsInstance(ref, Reference)
        self.assertEqual(ref.ref_type, "article")
        self.assertEqual(ref.key, doi)

        self.assertEqual(ref.other_fields["author"], "Mallory-Kani, Amy")
        self.assertEqual(ref.other_fields["title"], "Example Article")
        self.assertEqual(ref.other_fields["journal"], "European Romantic Review")
        self.assertEqual(ref.other_fields["year"], 2015)
        self.assertEqual(ref.other_fields["volume"], "26")
        self.assertEqual(ref.other_fields["pages"], "699-717")


    @patch("repositories.viite_repository.requests.get")
    def test_fetch_reference_by_doi_missing_author(self, mock_get):
        """Testaa että puuttuva author asetetaan oletusarvoon '-'"""

        fake_response = {
            "message": {
                "title": ["No Author Article"],
                "issued": {"date-parts": [[2020]]},
                "container-title": ["Test Journal"]
            }
        }

        mock_resp = Mock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = fake_response
        mock_get.return_value = mock_resp

        ref = self.ref.fetch_reference_by_doi("10.0000/noauthor")

        self.assertEqual(ref.other_fields["author"], "-")
        self.assertEqual(ref.other_fields["title"], "No Author Article")
        self.assertEqual(ref.other_fields["year"], 2020)
        self.assertEqual(ref.other_fields["journal"], "Test Journal")


    @patch("repositories.viite_repository.requests.get")
    def test_fetch_reference_by_doi_request_exception(self, mock_get):
        """Testaa että DOI-haun HTTP-virhe palauttaa None"""

        # Mockataan että requests.get heittää RequestException
        mock_get.side_effect = RequestException("HTTP error")

        ref_manager = ReferenceManager("test.db")
        result = ref_manager.fetch_reference_by_doi("10.1234/virhe")
        self.assertIsNone(result)

    @patch("repositories.viite_repository.requests.get")
    def test_fetch_reference_by_doi_general_exception(self, mock_get):
        """Testaa että DOI-haun odottamaton virhe palauttaa None"""

        # Mockataan että requests.get heittää yleisen exceptionin
        mock_get.side_effect = Exception("Unexpected error")

        ref_manager = ReferenceManager("test.db")
        result = ref_manager.fetch_reference_by_doi("10.1234/virhe")
        self.assertIsNone(result)


    # URL-tests
    @patch("repositories.viite_repository.requests.get")
    @patch.object(ReferenceManager, "fetch_reference_by_doi")
    def test_fetch_reference_by_url_success(self, mock_fetch_doi, mock_get):
        """URL-haku: sivulta löytyy DOI ja DOI-haku palauttaa viitteen."""
        html = "random text doi:10.1097/01.ACM.0000524672.21238.b6 more text"

        mock_resp = Mock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.text = html
        mock_get.return_value = mock_resp

        expected = Reference("article", "x", {"title": "dummy"})
        mock_fetch_doi.return_value = expected

        ref = self.ref.fetch_reference_by_url("https://example.com/page")

        self.assertIs(ref, expected)
        mock_fetch_doi.assert_called_once_with("10.1097/01.ACM.0000524672.21238.b6")


    @patch("repositories.viite_repository.requests.get")
    def test_fetch_reference_by_url_no_doi_returns_none(self, mock_get):
        """URL-haku: jos DOI:tä ei löydy sivulta, palautetaan None."""
        mock_resp = Mock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.text = "<html>No doi here</html>"
        mock_get.return_value = mock_resp

        ref = self.ref.fetch_reference_by_url("https://example.com/page")

        self.assertIsNone(ref)


    @patch("repositories.viite_repository.requests.get")
    def test_fetch_reference_by_url_request_exception(self, mock_get):
        """URL-haku: jos requests.get kaatuu, palautetaan None."""
        mock_get.side_effect = RequestException("HTTP error")

        ref = self.ref.fetch_reference_by_url("https://example.com/page")

        self.assertIsNone(ref)
