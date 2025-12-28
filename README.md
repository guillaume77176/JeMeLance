# JeMeLance
### Projet 2A ENSAE Python | Guillaume Roustan, Emmanuel Akoun

Acceder à l'application streamlit developpée : https://jemelance.streamlit.app/ .

-------
JeMeLance est un projet réalisé dans le cadre du cours Python 2A à l'ENSAE. 

### Le contexte et le but : 
Souvent, les individus ayant un projet de création d'entreprise peuvent douter, doute qui freine souvent les ambitions. JeMeLance est un projet qui se donne la tâche, sans grandes ambitions et de manière perfectible, de lever une petite partie de ces doutes. En utilisant comme base principale celle du Registre Nationale des Entreprises (RNE) rendue accessible de manière libre par L'INPI, le but est de prédire pour les 5 années suivants la création d'entreprise, si une entreprise sera radiée du RNE au cours de ces années. Le projet se focalise sur la région Ile-de-France.

### L'arboressance du projet : 
Le projet suit la logique suivante :

Le dossier `notebooks` contient les notebooks principaux qui serviront au rendue final. Par la même occasion, ils sont la base des créations des bases de données utiles au projet, mais également de l'analyse de données et de la modélisation. 

- `Get_RNE_FromScratch.ipynb` retrace la récupération du RNE depuis un serveur ftp fournit par l'INPI. Les données sont téléchargées et stockées directement sur le SSP cloud.
- `Get_RNE_More.ipynb` retrace quant à lui la récupération de données supplémentaires. Il constitue la partie "data engeenering" du projet. La base de données obtenue est également stockée sur le SSP cloud.
- `Analyse_RNE.ipynb` se consacre à l'analyse de données. Il permet d'étudier (de manière non-exhaustive certes) les relations entre les variables explicatives retenues à ce stade et les variables cibles construit et définies d'une manière spécifique.
- `Modélisation_RNE.ipynb` est le notebook qui propose l'utilisation d'un modèle de classfication pour réaliser les prédictions. Le modèle est entrainé, évalué et enregistré.
- Dossier `data` version 1.1 contenant le module principale de récupération des données pour la partie analyse.
    - Contient la fonction `load_base`, servant à récupérer depuis le SSP cloud la base de donnée brute issue de la partie récupération, et donnant accès aux entreprises d'Ile-de-France créées entre 2010 et 2024.
    - Contient la fonction `get_df_i` servant à gérer simultanément les 5 data frames de travail issues de la création des 5 variables cibles, les `radiéi`, avec i compris entre 1 et 5, où `radiéi` est une variable indicatrice du fait qu'une entreprise soit radiée du RNE au cours de l'année i suivant sa création.
    - Contient la fonction `load_base_model` servant à récupérer depuis le SSP cloud la base donnée affinée de l'analyse qui sert à la modélisation.
      


