class Item:
    def __init__(self, name, price, autobuyPrice):
        self.name = name
        self.price = price
        self.autobuyPrice = autobuyPrice

    def __str__(self):
        return f"{self.name}  {self.price} {self.autobuyPrice}"


class SteamItem(Item):
    def __init__(self, id, name, price, autobuyPrice):
        super().__init__(name, price, autobuyPrice)
        self.id = id

    def __repr__(self):
        return f'SteamItem(id={self.id}, name={self.name} price={self.price}, autobuyPrice={self.autobuyPrice})'


class BitskinsItem(Item):
    def __init__(self, name, price, autobuyPrice):
        super().__init__(name, price, autobuyPrice)

    def __repr__(self):
        return f'BitskinsItem(name={self.name}, price={self.price}, autobuyPrice={self.autobuyPrice})'
