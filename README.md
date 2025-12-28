# JeMeLance 🤔 🚀🚀🚀
<p align="center">
  <img src="logo.png" alt="Logo 1" width="250">
  &nbsp;&nbsp;&nbsp;
  <img src="logoENSAE.png" alt="Logo 2" width="250">
</p>

Guillaume Roustan | Emmanuel Akoun

`Version 1.1`

JeMeLance est un projet réalisé dans le cadre du cours Python 2A à l'ENSAE.

Accéder à l'application Streamlit développée : https://jemelance-now.streamlit.app/

-------

### Le contexte et le but :
Souvent, les individus ayant un projet de création d'entreprise peuvent douter — doute qui freine souvent les ambitions.  
JeMeLance est un projet qui se donne la tâche, sans grandes ambitions et de manière perfectible, de lever une petite partie de ces doutes.  

En utilisant comme base principale le Registre National des Entreprises (RNE) rendu accessible librement par l'INPI, le but est de prédire, pour les 5 années suivant la création d’une entreprise, si celle-ci sera radiée du RNE au cours de ces années. Le projet se focalise sur la région Île-de-France.

-------

### Les données utilisées :

La plupart des données utilisées pour ce projet ont été téléchargées et stockées sur le SSP Cloud afin d’en faciliter les appels successifs.  
Ci-dessous, vous trouverez chaque base de données utilisée, sa source, et son lien de téléchargement.

- **Données du RNE de 1980 à 2024** (source : https://data.inpi.fr/content/editorial/Serveur_ftp_entreprises)  
  → Liens SSP Cloud (13 fichiers .parquet) :
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

- **Niveau de vie par commune en France (2013)** (source : INSEE)  
  → Lien direct (1 fichier .xlsx) :  
    - https://www.data.gouv.fr/api/1/datasets/r/d3ce0107-416f-42cf-a335-d71f89b00b21

- **Recensement des communes de France jusqu’en 2022** (source : INSEE)  
  → Lien SSP Cloud (1 fichier .csv) :
    - https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_supp/DS_RP_SERIE_HISTORIQUE_2022_data.csv

- **API Base Adresse Nationale (BAN)**  
  (source : https://api.gouv.fr/les-api/base-adresse-nationale)

- **Communes et villes de France**  
  (source : https://www.data.gouv.fr/datasets/communes-et-villes-de-france-en-csv-excel-json-parquet-et-feather)  
  → Lien direct (1 fichier .parquet) :
    - https://object.files.data.gouv.fr/hydra-parquet/hydra-parquet/1f4841ac6cc0313803cabfa2c7ca4d37.parquet

------

### L’arborescence du projet (hors application `jemelance.py`) :
Le projet suit la logique suivante :

## I) Dossier `notebooks`
Il contient les notebooks principaux constituant le rendu final. Ils servent à la création des bases de données utiles au projet, mais également à l’analyse de données et à la modélisation.

- `Get_RNE_FromScratch.ipynb` : récupération du RNE depuis le serveur FTP fourni par l’INPI. Les données sont téléchargées et stockées sur le SSP Cloud.
- `Get_RNE_More.ipynb` : récupération de données supplémentaires. Il constitue la partie “data engineering” du projet.
- `Analyse_RNE.ipynb` : analyse de données (relations entre variables explicatives et variables cibles).
- `Modélisation_RNE.ipynb` : entraînement, évaluation et sauvegarde d’un modèle de classification.
- Dossier `notebooks.data` version 1.1 :
    - `load_base` : récupère sur le SSP Cloud la base obtenue dans la partie récupération (entreprises d’IDF créées entre 2010 et 2024).
    - `get_df_i` : gère les 5 dataframes correspondant aux 5 variables cibles `radiéi`.
    - `load_base_model` : charge la base affinée dédiée à la modélisation.

## II) Dossier `src`
Il contient les modules principaux pour réutiliser le projet rapidement, et sert aussi à l’application Streamlit.

- `src.data` version 1.1 : contient `load_base`, `get_df_i`, `load_base_model`, ainsi que :
    - `load_base_nlp` : renvoie la base RNE dont les textes ont été nettoyés (depuis `clean_nlp.ipynb`).
    - `load_base_ville` : renvoie la base "Communes et villes de France".

- Fichiers des modèles sauvegardés :  
  `seuils_proba_xgb.json`, `xgb_radié1.pkl`, …, `xgb_radié5.pkl`.

- `load_xgb.py` :  
  - `load_model` : charge un modèle XGBoost.  
  - `load_threshold` : charge les seuils de probabilité.

- `nlp.py` : permet de récupérer un code APE et un SIREN correspondant à une saisie utilisateur.

## III) Dossier `docs`
Il fournit notamment :
- de la documentation sur les données du RNE,
- la nomenclature NAF, utile pour comprendre la logique des codes APE.

-------

### L’application JeMeLance :
Développée avec Streamlit et hébergée gratuitement sur le cloud Streamlit, cette application vise à déployer le modèle de manière ludique et fluide.  
Le script `jemelance.py` contient le code nécessaire à l’application.  
L’application constitue un objet à part entière du rendu final.

------

JeMeLance | version 1.1
