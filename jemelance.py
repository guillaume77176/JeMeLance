import streamlit as st
from src.load_xgb import load_model, load_threshold
from src.nlp import predict_ape
import time

# URL ou chemin local de l'image
background_image = "https://images.unsplash.com/photo-1534841090574-cba2d662b62e?auto=format&fit=max&w=1920&q=80"

st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("{background_image}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)
# URL de ton logo (tu peux uploader ton PNG sur un hébergeur comme Imgur, GitHub, ou Streamlit Cloud)
logo_url = "https://minio.lab.sspcloud.fr/guillaume176/diffusion/logo/logo.png"

st.image("logo.png", use_column_width=True)

st.title("Je me lance ? 🤔 🚀🚀🚀")

st.markdown(
    "<h1 style='font-family:Arial; font-size:20px; color:White;'>Avec JeMeLance, n'ayez plus de doutes sur votre projet d'entreprise ! Envie de démarrer une activité dans les secteurs du commerce et de l'artisanat ? Entrer vos informations personnelles et une description brève de votre projet pour connaitre vos chances de réusssir !</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='font-family:Arial; font-size:20px; color:White;'>Les prédictions sont réalisés à l'aide d'un modèle d'intelligence artificielle. Il donne pour les cinq années suivant la création d'entreprise les chances d'être radié du registre national des entreprises.</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='font-family:Arial; font-size:20px; color:White;'>Régions disponibles : Ile-De-France</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<h1 style='font-family:Arial; font-size:10px; color:Red;'>A propos de la fiabilité des résultats : Evalué sur plus de dix ans de données cumulés, le modèle prédit correctement en moyenne 70% des entreprises qui ont été effectivement radiées au cours des cinq années suivants la création. Nous mettons en garde l'utilisateur avisé sur le fait que le modèle a tendance à donner de fausses alertes sur les chances de réussir. Il ne doit servir en aucun cas d'outils de décision final, mais est une simple vue globale de la réalité du tissu entrepreunarial d'île de France des 15 dernières années.</h1>",
    unsafe_allow_html=True
)


def debounce(seconds=0.4):
    time.sleep(seconds)

objet = st.text_input("Votre projet brièvement (Exemple : Food truck burger) :")

# On mémorise la dernière valeur
if "last_objet" not in st.session_state:
    st.session_state.last_objet = ""

# Si l'utilisateur a changé le texte
if objet != st.session_state.last_objet and objet != "":
    st.session_state.last_objet = objet
    debounce(0.4)

    # --- BARRE DE CHARGEMENT ---
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.05)
        progress.progress(i + 1)

    # --- PRÉDICTION ---
    objet_predict = predict_ape(objet)

    progress.empty()

    ape_pred = objet_predict[0]
    ex_text = objet_predict[2][0]

    st.write(f"Code APE correspondant : {ape_pred}")
    st.write(f"Activités en lien avec : {ex_text}")


personneMorale = st.radio(
    "Vous souhaitez :",
    ["Ouvrir une micro-entreprise", "Ouvrir une activité en tant qu'entrepreneur individuel", "Ouvrir une entreprise de type SARL, SAS, EIRL"]
)
sumxp = 0
mean_age = 0

if personneMorale == "Ouvrir une entreprise de type SARL, SAS, EIRL":
    nb_associe = st.slider(
        "Nombre d'associé prévu (max 5, si vous êtes seul selectionnez 1):",
        1, 5, 1
    )
    
    if nb_associe == 1:
        xp1 = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
        sumxp = xp1

        age1 = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
        mean_age = age1

    elif nb_associe == 2:
        col1, col2 = st.columns(2)
        with col1:
            xp1 = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
        with col2:
            xp2 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°2 :", 0, 20, 0)
        sumxp = xp1 + xp2

        with col1:
            age1 = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
        with col2:
            age2 = st.number_input("Quel est  l'âge de n°2 ?", min_value=0, max_value=120, value=30, step=1)
        sumxp = xp1 + xp2
        mean_age = (age1 + age2)/2

    elif nb_associe == 3:
        col1, col2, col3 = st.columns(3)
        with col1:
            xp1 = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
        with col2:
            xp2 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°2 :", 0, 20, 0)
        with col3:
            xp3 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°3 :", 0, 20, 0)

        with col1:
            age1 = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
        with col2:
            age2 = st.number_input("Quel est  l'âge de n°2 ?", min_value=0, max_value=120, value=30, step=1)
        with col3:
            age3 = st.number_input("Quel est  l'âge de n°3 ?", min_value=0, max_value=120, value=30, step=1)
        sumxp = xp1 + xp2 + xp3
        mean_age = (age1 + age2 + age3)/3

    elif nb_associe == 4:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            xp1 = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
        with col2:
            xp2 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°2 :", 0, 20, 0)
        with col3:
            xp3 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°3 :", 0, 20, 0)
        with col4:
            xp4 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°4 :", 0, 20, 0)

        with col1:
            age1 = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
        with col2:
            age2 = st.number_input("Quel est  l'âge de n°2 ?", min_value=0, max_value=120, value=30, step=1)
        with col3:
            age3 = st.number_input("Quel est  l'âge de n°3 ?", min_value=0, max_value=120, value=30, step=1)
        with col4:
            age4 = st.number_input("Quel est  l'âge de n°4 ?", min_value=0, max_value=120, value=30, step=1)
        sumxp = xp1 + xp2 + xp3 + xp4
        mean_age = (age1 + age2 + age3 + age4)/4


    else:  # nb_associe == 5
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            xp1 = st.slider("Nombre d'entreprises ouvertes dans le passé par vous:", 0, 20, 0)
        with col2:
            xp2 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°2 :", 0, 20, 0)
        with col3:
            xp3 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°3 :", 0, 20, 0)
        with col4:
            xp4 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°4 :", 0, 20, 0)
        with col5:
            xp5 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°5 :", 0, 20, 0)

        with col1:
            age1 = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
        with col2:
            age2 = st.number_input("Quel est  l'âge de n°2 ?", min_value=0, max_value=120, value=30, step=1)
        with col3:
            age3 = st.number_input("Quel est  l'âge de n°3 ?", min_value=0, max_value=120, value=30, step=1)
        with col4:
            age4 = st.number_input("Quel est  l'âge de n°4 ?", min_value=0, max_value=120, value=30, step=1)
        with col5:
            age5 = st.number_input("Quel est  l'âge de n°5 ?", min_value=0, max_value=120, value=30, step=1)
        sumxp = xp1 + xp2 + xp3 + xp4 + xp5
        mean_age = (age1 + age2 + age3 + age4 + age5)/5
    st.write(f"Total d'entreprises ouvertes par les associés : {sumxp}")
    st.write(f"Age moyen des associés : {mean_age}")

else:
    nb_associe = 1
    xp = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
    age1 = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
    sumxp = xp
    mean_age = age1
    st.write(f"Total d'entreprises ouvertes : {sumxp}")



