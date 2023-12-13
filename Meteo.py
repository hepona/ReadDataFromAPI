"""Class Meteoapi"""
class Meteoapi:
    """Attribut de la classe"""
    def __init__(self, temp, hum, wspeed, wdirection, name):
        self.name = name
        self.temp =temp
        self.hum = hum
        self.wspeed = wspeed
        self.wdirection = wdirection


    def temptocels(self):
        """Transformer la température en celsius"""
        return self.temp - 273.15

