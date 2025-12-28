# JeMeLance
<img src="logo.png" alt="Logo" width="150">

`Version 1.1`

Acceder à l'application streamlit developpée : https://jemelance.streamlit.app/ .

-------
JeMeLance est un projet réalisé dans le cadre du cours Python 2A à l'ENSAE. 

### Le contexte et le but : 
Souvent, les individus ayant un projet de création d'entreprise peuvent douter, doute qui freine souvent les ambitions. JeMeLance est un projet qui se donne la tâche, sans grandes ambitions et de manière perfectible, de lever une petite partie de ces doutes. En utilisant comme base principale celle du Registre Nationale des Entreprises (RNE) rendue accessible de manière libre par L'INPI, le but est de prédire pour les 5 années suivants la création d'entreprise, si une entreprise sera radiée du RNE au cours de ces années. Le projet se focalise sur la région Ile-de-France.

-------

### Les données utilisées :

La plupart des données utilisées pour ce projet ont été téléchargées et stockées sur le SSP cloud afin d'en faciliter les appels successifs. Ci-dessous, vous trouverez chaque base de données utilisés, sa source, et son lien de téléchargement.

- Données du RNE depuis 1980 jusqu'en 2024 (source https://data.inpi.fr/content/editorial/Serveur_ftp_entreprises) -> Liens SSP cloud (13 fichiers .parquet) :
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_1980_1990.parquet
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_1990_2000.parquet
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_2000_2005.parquet
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_2005_2010.parquet
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_2010_2015.parquet
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_2015_2017.parquet
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_2017_2018.parquet
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_2018_2019.parquet
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_2019_2020.parquet
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_2020_2021.parquet
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_2021_2022.parquet
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_2022_2023.parquet
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_RNE/RNE_2023_2024.parquet

- Niveau de vie par commune en France (2013) (source : INSEE) -> Lien direct : (1 fichier .xlsx) :
    - https://www.data.gouv.fr/api/1/datasets/r/d3ce0107-416f-42cf-a335-d71f89b00b21

- Recenssement commune de France jusqu'en 2022 (source : INSEE) -> Lien SSP cloud (1 fichier .csv) :
  - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_supp/DS_RP_SERIE_HISTORIQUE_2022_data.csv

- API Base Adresse Nationale (BAN) (source : https://api.gouv.fr/les-api/base-adresse-nationale)

- Communes et villes de France (source : https://www.data.gouv.fr/datasets/communes-et-villes-de-france-en-csv-excel-json-parquet-et-feather) -> Lien direct : (1 fichier .parquet):
  - https://object.files.data.gouv.fr/hydra-parquet/hydra-parquet/1f4841ac6cc0313803cabfa2c7ca4d37.parquet

------


### L'arboressance du projet (hors application jemelance.py) : 
Le projet suit la logique suivante :

I) Le dossier `notebooks` contient les notebooks principaux qui consistues le rendu final. Par la même occasion, ils sont la base des créations des bases de données utiles au projet, mais également de l'analyse de données et de la modélisation. 

- `Get_RNE_FromScratch.ipynb` retrace la récupération du RNE depuis un serveur ftp fournit par l'INPI. Les données sont téléchargées et stockées directement sur le SSP cloud.
- `Get_RNE_More.ipynb` retrace quant à lui la récupération de données supplémentaires. Il constitue la partie "data engeenering" du projet. La base de données obtenue est également stockée sur le SSP cloud.
- `Analyse_RNE.ipynb` se consacre à l'analyse de données. Il permet d'étudier (de manière non-exhaustive certes) les relations entre les variables explicatives retenues à ce stade et les variables cibles construit et définies d'une manière spécifique.
- `Modélisation_RNE.ipynb` est le notebook qui propose l'utilisation d'un modèle de classfication pour réaliser les prédictions. Le modèle est entrainé, évalué et enregistré.
- Dossier `notebooks.data` version 1.1 contenant le module principale de récupération des données pour la partie analyse.
    - Contient la fonction `load_base`, servant à récupérer depuis le SSP cloud la base de donnée brute issue de la partie récupération, et donnant accès aux entreprises d'Ile-de-France créées entre 2010 et 2024.
    - Contient la fonction `get_df_i` servant à gérer simultanément les 5 data frames de travail issues de la création des 5 variables cibles, les `radiéi`, avec i compris entre 1 et 5, où `radiéi` est une variable indicatrice du fait qu'une entreprise soit radiée du RNE au cours de l'année i suivant sa création.
    - Contient la fonction `load_base_model` servant à récupérer depuis le SSP cloud la base donnée affinée de l'analyse qui sert à la modélisation.

II) Le dossier `src` contient les principaux modules utiles pour une réutilisation du projet rapide, et sert par la mêle occasion à l'application streamlit développée.

- `src.data` version 1.1 contient `load_base`, `get_df_i`, `load_base_model`, ainsi que les autres modules fonctions suivantes servant à l'application streamlit :

    - `load_base_nlp` renvoie la base RNE obtenue dans la partie récupération dont les textes de renseignements des activités de chaque entreprise ont été néttoyés depuis le notebook `clean_nlp.ipynb`.
    - `load_base_ville` renvoie la base de donnée Communes et villes de France fournit par https://www.data.gouv.fr/datasets/communes-et-villes-de-france-en-csv-excel-json-parquet-et-feather.

- Les fichiers `seuils_proba_xgb.json`, `xgb_radié1.pkl`, `xgb_radié2.pkl`, `xgb_radié3.pkl`, `xgb_radié4.pkl`, `xgb_radié5.pk` correspondent aux sauvegardes des 5 modèles retenues dans la partie modélisation, ainsi que des seuils de probabilité optimaux pour la classification.
- Le module `load_xgb.py` permet de récupérer le modèle entrainé sur les données grâce à la fonction `load_model`. La fonction `load_threshold` récupère les seuils optimaux pour la classification.
- Le module `nlp.py` permet quant à lui de récupérer un code APE ainsi les textes type "objet" et siren pouvant correspondre depuis une saisie utilisateur renseignant brièvement sur l'activité projetée. 

III) Le dossier `docs` fournit lui de la documentation sur les données du RNE, ainsi que sur la nomenclature NAF, permettant de comprendre la logique des code APE.

-------
### L'application JeMeLance : 
Dévoloppée à l'aide de l'api streamlit et hébergée gratuitement sur le cloud streamlit, cette application vise à déployer le modèle mis en place de manière ludique et fluide. 
Le script `jemelance.py` fournit le code nécéssaire à faire tourner l'application.
L'application constitue un objet à part entière du rendu final.

------
JeMeLance | version 1.1










