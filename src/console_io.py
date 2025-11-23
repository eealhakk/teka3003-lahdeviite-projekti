"""ConsoleIO luokka"""
class ConsoleIO:
    """Luokka, joka hoitaa konsolilta lukemisen ja konsoliin tulostamisen"""
    def read(self, prompt):
        """Lukee käyttäjän antaman tekstin"""
        return input(prompt)

    def write(self, message):
        """Tulostaa viestin konsoliin"""
        print(message)
