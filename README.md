# JeMeLance
### Projet 2A ENSAE Python | Guillaume Roustan, Emmanuel Akoun


Pour Emannuel : 

Pour récup les data avec les radié_i (au total tu récupère une liste de 5 data frames)

```` python
from get_dfi import load_dfi

data = load_dfi()

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


Pour récupérer la variable cible (radié = 1 si entreprise radié 0 si toujours active)

``` python

#Construction de la variable cible "radié"
data["dateRadiation"] = pd.to_datetime(data["dateRadiation"],errors="coerce")
data["radié"] = data["dateRadiation"].notna().astype(int)

```
