class Card:
    def __init__(self, value):
        self.value = value
        self.heads = self._calculate_heads(value)

    def _calculate_heads(self, value):
        result = 1
        if value % 5 == 0:
            result = 2
        if value % 10 == 0:
            result = 3
        if value % 11 == 0:
            result = 5
        if value == 55:
            result = 7
        return result

    def __gt__(self, other):
        return self.value > other.value

    def __str__(self) -> str:
        return f"{self.value}"
