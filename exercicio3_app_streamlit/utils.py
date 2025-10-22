import pandas as pd
from sklearn.datasets import load_iris, fetch_california_housing
import streamlit as st

@st.cache_data
def carregar_dataset_exemplo(nome):
    if nome == "Iris":
        dados = load_iris()
        df = pd.DataFrame(dados.data, columns=dados.feature_names)
        df['species'] = pd.Categorical.from_codes(dados.target, dados.target_names)
        return df
    elif nome == "California Housing":
        dados = fetch_california_housing()
        df = pd.DataFrame(dados.data, columns=dados.feature_names)
        df['price'] = dados.target
        return df
    return None
