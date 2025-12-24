import streamlit as st

st.title("Ma nouvelle app Streamlit")
st.write("Bienvenue dans ma nouvelle application !")

# Exemple simple
name = st.text_input("Quel est ton nom ?")
if name:
    st.success(f"Salut, {name} !")
