from datasets import Dataset
import pandas as pd

from datasets import Dataset
import pandas as pd

def load_knowledge_base():
    data = {
        "texte": [
            "L'ESTI se trouve à Antananarivo, Madagascar.",
            "L'ESTI propose des formations dans les domaines de l'informatique, du développement logiciel, des réseaux, de la cybersécurité et du management des systèmes d'information.",
            "Les diplômes délivrés par l'ESTI sont homologués et reconnus par l'État malgache.",
            "L'ESTI offre un programme de formation initiale de deux ans appelé MSI (Maintenance des Systèmes Informatiques), qui mène à un DTS agréé par l'État.",
            "En plus des formations initiales, l'ESTI propose aussi des formations modulaires qui débouchent sur des certificats professionnels.",
            "L'ESTI accompagne ses étudiants vers des carrières en freelancing ou dans des entreprises du secteur numérique.",
            "Le contact téléphonique de l'ESTI est 0330828086, 0340220452 ou 0320420452."
        ]
    }
    return Dataset.from_pandas(pd.DataFrame(data))

