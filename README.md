# JeMeLance
### Projet 2A ENSAE Python | Guillaume Roustan, Emmanuel Akoun

Acceder à l'application streamlit developpée : https://jemelance.streamlit.app/ .

-------
JeMeLance est un projet réalisé dans le cadre du cours Python 2A à l'ENSAE. 

### Le contexte et le but : 
Souvent, les individus ayant un projet de création d'entreprise peuvent douter, doute qui freine souvent les ambitions. JeMeLance est un projet qui se donne la tâche, sans grandes ambitions et de manière perfectible, de lever une petite partie de ces doutes. En utilisant comme base principale celle du Registre Nationale des Entreprises (RNE) rendue accessible de manière libre par L'INPI, le but est de prédire pour les 5 années suivants la création d'entreprise, si une entreprise sera radiée du RNE au cours de ces années. 

### L'arboressance du projet : 
Le projet suit la logique suivante :

Le dossier `notebooks` contient les notebooks principaux qui serviront au rendue final. Par la même occasion, ils sont la base des créations des bases de données utiles au projet, mais également de l'analyse de données et de la modélisation. 

- `Get_RNE_FromScratch.ipynb` retrace la récupération du RNE depuis un serveur ftp fournit par l'INPI. Les données sont téléchargées et stockées directement sur le SSP cloud.
- `Get_RNE_More.ipynb` retrace quant à lui la récupération de données supplémentaires. Il constitue la partie "data engeenering" du projet. La base de données obtenue est également stockée sur le SSP cloud.
- `Analyse_RNE.ipynb` se consacre à l'analyse de données. Il permet d'étudier (de manière non-exhaustive certes) les relations entre les variables explicatives retenues à ce stade et les variables cibles construit et définies d'une manière spécifique.
- `Modélisation_RNE.ipynb` est le notebook qui propose l'utilisation d'un modèle de classfication pour réaliser les prédictions. Le modèle est entrainé, évalué et enregistrer.



