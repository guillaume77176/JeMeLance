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


def load_base_nlp():
    url = "https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_nlp/data_text.parquet"
    data = pd.read_parquet(url,engine="pyarrow")
    print("Data Frame data_text récupéré depuis S3")
    return data

def load_base_ville():
    url = "https://object.files.data.gouv.fr/hydra-parquet/hydra-parquet/1f4841ac6cc0313803cabfa2c7ca4d37.parquet"
    data = pd.read_parquet(url,engine="pyarrow")
    return data

def get_df_i(data : pd.DataFrame) -> list:
    
    df1 = data.copy()
    df2 = data.loc[(data["radié1"] == 0)].copy()
    df3 = data.loc[(data["radié1"] == 0) & (data["radié2"] == 0)].copy()
    df4 = data.loc[(data["radié1"] == 0) & (data["radié2"] == 0) & (data["radié3"] == 0)].copy()
    df5 = data.loc[(data["radié1"] == 0) & (data["radié2"] == 0) & (data["radié3"] == 0) & (data["radié4"] == 0)].copy()

    df1 = df1
    df2 = df2.loc[df2["date_creation"].dt.year < 2023]
    df3 = df3.loc[df3["date_creation"].dt.year < 2022]
    df4 = df4.loc[df4["date_creation"].dt.year < 2021]
    df5 = df5.loc[df5["date_creation"].dt.year < 2020]

    return [df1,df2,df3,df4,df5]