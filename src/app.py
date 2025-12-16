"""App-moduuli ohjelman toiminnoille"""
from repositories.viite_repository import ReferenceManager
import json
from entities.refobj import Reference

class App:
    """App luokka, jossa ohjelman metodit"""
    def __init__(self):
        self.reference_manager = ReferenceManager()

    def run(self):
        """Metodi joka kysyy käyttäjältä haluttua toimintoa"""
        while True:
            print("\n=== Valitse toiminto ===")
            print("1) Lisää uusi viite")
            print("2) Listaa viitteet")
            print("3) Vie BibTeX-tiedosto")
            print("4) Muokkaa viitettä")
            print("5) Poista viite")
            print("6) Lopeta\n")



            choice = input("Valinta: ").strip()

            if choice == "1":
                self.add_reference_menu()
            elif choice == "2":
                self.list_references()
            elif choice == "3":
                self.reference_manager.export_bibtex("references.bib")
                print("BibTeX-tiedosto references.bib luotu")
            elif choice == "4":
                self.edit_reference()
            elif choice == "5":
                self.delete_reference()
            elif choice == "6":
                break
            else:
                print("Virheellinen valinta")


    def add_reference_menu(self):
        """Alavalikko viitteen lisäämiseen"""
        print("\n=== Lisää uusi viite ===")
        print("1) Manuaalisesti")
        print("2) DOI:lla")
        print("3) URL:lla")
        print("4) Takaisin\n")

        value = input("Valinta: ").strip()

        if value == "1":
            self.add_reference()
        elif value == "2":
            self.add_reference_by_doi()
        elif value == "3":
            self.add_reference_by_url()
        elif value == "4":
            return
        else:
            print("Virheellinen valinta")

    def list_references(self):
        """Metodi viitteiden listaamiseen"""
        print("\n1) Listaa tagin perusteella")
        print("2) Listaa kaikki")
        print("3) Filtteri\n")

        value = input("Valinta: ").strip()

        if value == "1":
            tag = input("Anna tagi: ").strip()
            results = self.reference_manager.get_references_by_tag(tag)

            if not results:
                print("Ei löytyny viitteitä tälle tagille.")
                return

            for ref_id, ref_type, key, raw_fields in results:
                fields = json.loads(raw_fields) if raw_fields else {}
                ref_obj = Reference(ref_type, key, fields)

                tags = self.reference_manager.get_reference_tags(ref_id)
                print(f"---\n\n{ref_obj}\ntags: {tags}")

        elif value == "2":
            for reference in self.reference_manager.listaa():
                reference_tags = self.reference_manager.get_reference_tags(reference[0])
                print(f"---\n\n{reference[1]}\ntags: {reference_tags}")
        elif value == "3":
            print("Anna kenttä ja arvo jonka mukaan filtteröidä esim. year,2008 tai type,book")
            givenvalue = input("Syötä kenttä ja arvo erotettuna pilkulla: ").strip()

            if givenvalue == "":
                return

            print("=== Tulokset: ===")
            for reference in self.reference_manager.filter_references(givenvalue):
                reference_tags = self.reference_manager.get_reference_tags(reference[0])
                print(f"---\n\n{reference[1]}\ntags: {reference_tags}")
        else:
            print("Virheellinen valinta")

    def delete_reference(self):
        """Metodi lähteen poistamiseen"""

        key_editing = input("Anna poistettavan viitteen BibTeX-avain: ").strip()
        poistettava = self.reference_manager.entry_info(str(key_editing))

        if not poistettava:
            print("Viitettä ei löydy.")
            return
        print("\n"+str(poistettava)+"\n")

        print("Haluatko varmasti poistaa viitteen? (K/E)")
        choice = input("Valinta: ").strip().upper()

        if choice == "K":
            self.reference_manager.delete_entry(key_editing)
            print("Viite poistettu!")
        elif choice == "E":
            return

    def edit_reference(self):
        """Metodi lähteen muokkaamiseen"""
        key_editing = input("Anna muokattavan viitteen BibTeX-avain: ").strip()

        ref_obj = self.reference_manager.entry_info(key_editing)

        if not ref_obj:
            print("Viitettä ei löydy.")
            return

        print("\n"+str(ref_obj)+"\n")

        fields = input("Anna kentät, joita haluat muokata erotettuna pilkulla: ").strip()
        allowed_fields = ref_obj.other_fields.keys()

        new_values = {}
        for field in fields.split(","):
            field = field.strip()
            if field not in allowed_fields:
                print(f"'{field}' ei ole sallittu.")
                return
            new_value = input(f"Anna uusi arvo kentälle '{field}': ").strip()
            new_values[field] = new_value

        self.reference_manager.edit_entry(ref_obj.ref_type, key_editing, **new_values)
        print("Viite päivitetty!")

    def add_reference(self):
        """Metodi lähteen lisäämiseen"""
        ref_type = input("Viitetyyppi: ")

        key = input("BibTeX-avain: ").strip()

        print("Mitä muita tietoja viitteelle annetaan?")
        other_element_names = input("Muut kentät (erottele pilkulla): ")
        other_element_names = other_element_names.strip().split(",")

        other_element_values = {}
        if other_element_names:
            for element in other_element_names:
                element = element.strip()
                element_value = input(f"Arvo {element} kentälle: ")
                other_element_values[element] = element_value

        tags = input("Tagit (valinnainen, erottele pilkulla): ").strip()
        tags = tags.strip().split(",")

        if self.reference_manager.add_entry(ref_type, key, other_element_values, tags):
            print(f"{ref_type}-viite lisätty!")
        else:
            print("Virhe lisättäessä, varmista että BibTex-avain on uniikki.")

    def ask_type(self):
        """Metodi lähteen tyypin valintaan"""
        print("\n=== Valitse viitetyyppi ===")
        print("1) Inproceedings")
        print("2) Article")
        print("3) Book\n")

        type_choice = input("Tyyppi: ").strip()

        if type_choice == "1":
            return "inproceeding"
        if type_choice == "2":
            return "article"
        if type_choice == "3":
            return "book"
        print("Virheellinen valinta")
        return None

    def add_reference_by_doi(self):
        """Lisää viite DOI-tunnisteen avulla artikkeliksi"""
        doi = input("Anna DOI(esimerkiksi: doi.org/10.1080/10509585.2015.1092083): ").strip()

        if not doi:
            return

        key = input("BibTeX-avain: ").strip()
        tags = input("Tagit (valinnainen, erottele pilkulla): ").strip().split(",")
        if not key:
            print("Virheellinen BibTex avain")
            return
        article = self.reference_manager.fetch_reference_by_doi(doi)

        if not article:
            print("DOI-haku epäonnistui tai viite puutteellinen.")
            return


        # Viitteen lisäys tietokantaan
        #print("DEBUG Article:", vars(article))
        if self.reference_manager.add_entry(
            "article",  # entry_type
            key,        # key
            {
                "author": article.other_fields.get("author", "-"),
                "title": article.other_fields.get("title", "-"),
                "journal": article.other_fields.get("journal", "-"),
                "year": article.other_fields.get("year", 0),
                "volume": article.other_fields.get("volume", "-"),
                "pages": article.other_fields.get("pages", "-"),
            },
            tags
        ):
            print(f"Viite DOI:sta {doi} lisätty tietokantaan.")
        else:
            print("Virhe lisättäessä, varmista että BibTeX-avain on uniikki.")

    def add_reference_by_url(self):
        """Lisää viite URL-osoitteen avulla"""

        url = input("Anna URL: ").strip()
        if not url:
            return

        key = input("BibTeX-avain: ").strip()
        tags = input("Tagit (valinnainen, erottele pilkulla): ").strip().split(",")

        if not key:
            print("Virheellinen BibTeX avain")
            return

        article = self.reference_manager.fetch_reference_by_url(url)

        if not article:
            print("URL-haku epäonnistui tai DOI ei löytynyt sivulta.")
            return

        ok = self.reference_manager.add_entry(
            "article",
            key,
            {
                "author": article.other_fields.get("author", "-"),
                "title": article.other_fields.get("title", "-"),
                "journal": article.other_fields.get("journal", "-"),
                "year": article.other_fields.get("year", 0),
                "volume": article.other_fields.get("volume", "-"),
                "pages": article.other_fields.get("pages", "-"),
            },
            tags
        )

        if ok:
            print("Viite lisätty URL:n kautta.")
        else:
            print("Virhe lisättäessä, varmista että BibTeX-avain on uniikki.")
