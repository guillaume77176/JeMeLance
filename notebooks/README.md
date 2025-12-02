Ce dossier est constitué des principaux notebooks du projet et sont destinés à l'évaluation du projet.

Le premier `RapportJeMeLance.ipynb` explique de manière synthétique le projet et son déroulement, en rejouant les "grandes phases" du projet, sans rentrer dans les détails des fonctions utilisées. Il reprend la trame 1) Récupération des données , 2) Analyse et visualisation , 3) Modélisation, liée à l'évaluation du projet.

Les autres notebooks fournis sont plus détaillés, où des explications plus riches sont données sur les différentes fonctions crées, les choix effectués, etc.

Notenooks détaillés : 

Partie "Récupération des données" : - `getRNE.ipynb` et `get_RNE_More`

Pour récupérer le data frame de travail brute après cette partie : 

```` python
from data.load_idf_10_24 import load_base

df = load_base()

````

Partie "Analyse et visualition" : - `analyse_RNE`

Partie "Modélisation" : - `classification_RNE`
