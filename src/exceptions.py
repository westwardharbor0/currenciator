
class UnknownCurrency(Exception):
    """
    If currency is not known to us (obviously)
    """
    def __init__(self, currency):
        self.message = "Currency {} is unknown".format(currency)

    def __str__(self):
        return self.message
