"""Viiteluokka reference."""
# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
# pylint: disable=too-few-public-methods

class Reference:
    """reference-luokka edustaa viitettä yleisellä tasolla."""
    def __init__(self, ref_type, key, other_fields):
        self.ref_type = ref_type
        self.key = key
        self.other_fields = dict(other_fields)


    def __str__(self):
        fields_str = "\n".join(
            f"  {field}: {value}" for field, value in self.other_fields.items()
        )
        return f"Type: {self.ref_type}\nKey: {self.key}\n{fields_str}"
