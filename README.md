# JeMeLance
### Projet 2A ENSAE Python | Guillaume Roustan, Emmanuel Akoun


Pour Emannuel : 

Pour récupérer le data frame de travail brute faisant suite à la récupération RNE tu peux soit depuis le "main" ou bien "main/notebooks"
lancer le code suivant (attention à ne pas commit dans le main, cela compromettrait tout le projet, utilise une autre branche pour cela): 

```` python
from data.load_idf_10_24 import load_base

df = load_base()

````

Ou bien tu peux copier coller le code suivant depuis n'importe quelle ide, sans forcément cloner le repo github :

``` python 
import pandas as pd 

url  = "https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_final/idf_10_24.parquet"

data = pd.read_parquet(url, engine = "pyarrow") #enlève engine = "pyarrow" si erreur sur pyarrow dans ton ide
````


Token pour projet : 

``` text
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
````
