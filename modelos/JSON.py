import json

class JSON:

    def __init__(self) -> None:
        pass

    @staticmethod
    def leerJSON(url):
        with open(url, "r") as j:
            myData = json.load(j)
            return myData