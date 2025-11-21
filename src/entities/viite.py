class Reference:
    def __init__(self, type, key, fields=None):
        self.type = type
        self.key = key
        self.fields = fields if fields else {}