from src.data.load_idf_10_24 import load_base_nlp
import pandas as pd
from langchain_community.retrievers import TFIDFRetriever
from langchain_community.document_loaders import DataFrameLoader

data_text = load_base_nlp()

#(Cette fonction est inspiré fortement du cours de Lino Galiana)
def predict_ape(des : str) -> list:

    loader = DataFrameLoader(data_text, page_content_column="text_clean")

    retriever = TFIDFRetriever.from_documents(
        loader.load()
    )

    documents = []
    for best_echoes in retriever.invoke(des):
        documents += [{**best_echoes.metadata, **{"text_clean": best_echoes.page_content}}]

    documents = pd.DataFrame(documents)

    ape_pred = str(documents.iloc[0,0])
    siren_ex = list(documents["siren"])
    text_ex = list(documents["text_clean"])

    return ape_pred, siren_ex, text_ex