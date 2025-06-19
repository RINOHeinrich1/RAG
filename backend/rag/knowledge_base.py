from datasets import Dataset
import pandas as pd

def load_knowledge_base():
    data = {
        "texte": [
            "la capitale de la france est paris.",
            "la tour eiffel se trouve à paris.",
            "le mont everest est la plus haute montagne du monde. il mesure 8 849 mètres.",
            "la grande muraille de chine est visible depuis l'espace. elle se trouve en chine.",
            "python est un langage de programmation populaire."
        ]
    }
    df = pd.DataFrame(data)
    return Dataset.from_pandas(df)
