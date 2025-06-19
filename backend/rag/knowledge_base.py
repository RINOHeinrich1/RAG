from datasets import Dataset
import pandas as pd

def load_knowledge_base():
    data = {
        "texte": [
            "La capitale de la France est Paris.",
            "Le Mont Everest est la plus haute montagne du monde.",
            "Le Mont Everest mesure 8,849 m",
            "La Tour Eiffel se trouve à Paris.",
            "La Grande Muraille de Chine est visible depuis l'espace.",
            "La grande muraille se trouve en chine",
            "Python est un langage de programmation populaire."
        ]
    }
    return Dataset.from_pandas(pd.DataFrame(data))
