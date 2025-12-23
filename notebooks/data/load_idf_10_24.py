import pandas as pd

#Récupération idf_10_24 depuis le cloud S3
def load_base():
    url = "https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_final/idf_10_24.parquet"
    data = pd.read_parquet(url,engine="pyarrow")
    print("Data Frame idf_10_24 récupéré depuis S3")
    return data


def load_base_model():
    url = "https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_model/idf_10_24MODEL.parquet"
    data = pd.read_parquet(url,engine="pyarrow")
    print("Data Frame idf_10_24MODEL récupéré depuis S3")
    return data


