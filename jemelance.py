import streamlit as st
from src.load_xgb import load_model, load_threshold
from src.data.load_idf_10_24 import load_base, load_base_ville
from src.nlp import predict_ape
import time
import requests
import pandas as pd


#Sélections des variables candiates : 
var_cand = ["taille_ville","nb_local_concurrents",
"revCommune","revDep"]


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

st.image("logo.png", width=300)

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
        time.sleep(0.15)
        progress.progress(i + 1)

    # --- PRÉDICTION ---
    objet_predict = predict_ape(objet)

    progress.empty()

    ape_pred = objet_predict[0]
    ex_text = objet_predict[2][0]

    st.write("Description chargée. Vous pouvez continuer.")
    st.write(f"Code APE correspondant : {ape_pred}")
    st.write(f"Activités en lien avec : {ex_text}")


capital = st.text_input("Montant du capital social initial prévu :", "")

try:
    test_capital = float(capital)
    montantCapital = float(capital)
    st.write("Votre capital social initial :", capital)
except ValueError:
    st.write("Veuillez entrer un nombre valide.")


personneMorale_in = st.radio(
    "Vous souhaitez :",
    ["Ouvrir une micro-entreprise", "Ouvrir une activité en tant qu'entrepreneur individuel", "Ouvrir une entreprise de type SARL, SAS, EIRL"]
)
sumxp = 0
mean_age = 0

if personneMorale_in == "Ouvrir une entreprise de type SARL, SAS, EIRL":
    personneMorale = 1
    micro = 0
    nb_associe = st.slider(
        "Nombre d'associé prévu (max 5, si vous êtes seul selectionnez 1):",
        1, 5, 1
    )
    
    if nb_associe == 1:
        xp1 = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
        sumxp = xp1

        xp1_rad = st.slider("Votre nombre d'entreprises ouvertes dans le passé radiés:", 0, 20, 0)
        sumxp_rad = xp1_rad

        xp1_ape = st.slider("Votre nombre d'entreprises ouvertes dans le passé correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
        sumxp_ape = xp1_ape

        age1 = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
        mean_age = age1

    elif nb_associe == 2:
        col1, col2 = st.columns(2)
        with col1:
            xp1 = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
            
            xp1_rad = st.slider("Votre nombre d'entreprises ouvertes dans le passé radiés:", 0, 20, 0)

            xp1_ape = st.slider("Votre nombre d'entreprises ouvertes dans le passé correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
        with col2:
            xp2 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°2 :", 0, 20, 0)

            xp2_rad = st.slider("Nombre d'entreprises ouvertes dans le passé radiés de n°2:", 0, 20, 0)

            xp2_ape = st.slider("Nombre d'entreprises ouvertes dans le passé par n°2 correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)

        sumxp = xp1 + xp2
        sumxp_rad = xp1_rad + xp2_rad
        sumxp_ape = xp1_ape + xp2_ape

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
            
            xp1_rad = st.slider("Votre nombre d'entreprises ouvertes dans le passé radiés:", 0, 20, 0)

            xp1_ape = st.slider("Votre nombre d'entreprises ouvertes dans le passé correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
        with col2:
            xp2 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°2 :", 0, 20, 0)

            xp2_rad = st.slider("Nombre d'entreprises ouvertes dans le passé radiés de n°2:", 0, 20, 0)

            xp2_ape = st.slider("Nombre d'entreprises ouvertes dans le passé par n°2 correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
        with col3:
            xp3 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°3 :", 0, 20, 0)

            xp3_rad = st.slider("Nombre d'entreprises ouvertes dans le passé radiés de n°3:", 0, 20, 0)

            xp3_ape = st.slider("Nombre d'entreprises ouvertes dans le passé par n°3 correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)

        with col1:
            age1 = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
        with col2:
            age2 = st.number_input("Quel est  l'âge de n°2 ?", min_value=0, max_value=120, value=30, step=1)
        with col3:
            age3 = st.number_input("Quel est  l'âge de n°3 ?", min_value=0, max_value=120, value=30, step=1)
        sumxp = xp1 + xp2 + xp3
        sumxp_rad = xp1_rad + xp2_rad + xp3_rad
        sumxp_ape = xp1_ape + xp2_ape + xp3_ape
        mean_age = (age1 + age2 + age3)/3

    elif nb_associe == 4:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            xp1 = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
            
            xp1_rad = st.slider("Votre nombre d'entreprises ouvertes dans le passé radiés:", 0, 20, 0)

            xp1_ape = st.slider("Votre nombre d'entreprises ouvertes dans le passé correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
        with col2:
            xp2 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°2 :", 0, 20, 0)

            xp2_rad = st.slider("Nombre d'entreprises ouvertes dans le passé radiés de n°2:", 0, 20, 0)

            xp2_ape = st.slider("Nombre d'entreprises ouvertes dans le passé par n°2 correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
        with col3:
            xp3 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°3 :", 0, 20, 0)

            xp3_rad = st.slider("Nombre d'entreprises ouvertes dans le passé radiés de n°3:", 0, 20, 0)

            xp3_ape = st.slider("Nombre d'entreprises ouvertes dans le passé par n°3 correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
        with col4:
            xp4 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°4 :", 0, 20, 0)

            xp4_rad = st.slider("Nombre d'entreprises ouvertes dans le passé radiés de n°4:", 0, 20, 0)

            xp4_ape = st.slider("Nombre d'entreprises ouvertes dans le passé par n°4 correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)

        with col1:
            age1 = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
        with col2:
            age2 = st.number_input("Quel est  l'âge de n°2 ?", min_value=0, max_value=120, value=30, step=1)
        with col3:
            age3 = st.number_input("Quel est  l'âge de n°3 ?", min_value=0, max_value=120, value=30, step=1)
        with col4:
            age4 = st.number_input("Quel est  l'âge de n°4 ?", min_value=0, max_value=120, value=30, step=1)
        sumxp = xp1 + xp2 + xp3 + xp4
        sumxp_rad = xp1_rad + xp2_rad + xp3_rad + xp4_rad
        sumxp_ape = xp1_ape + xp2_ape + xp3_ape + xp4_ape
        mean_age = (age1 + age2 + age3 + age4)/4


    else:  # nb_associe == 5
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            xp1 = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
            
            xp1_rad = st.slider("Votre nombre d'entreprises ouvertes dans le passé radiés:", 0, 20, 0)

            xp1_ape = st.slider("Votre nombre d'entreprises ouvertes dans le passé correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
        with col2:
            xp2 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°2 :", 0, 20, 0)

            xp2_rad = st.slider("Nombre d'entreprises ouvertes dans le passé radiés de n°2:", 0, 20, 0)

            xp2_ape = st.slider("Nombre d'entreprises ouvertes dans le passé par n°2 correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
        with col3:
            xp3 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°3 :", 0, 20, 0)

            xp3_rad = st.slider("Nombre d'entreprises ouvertes dans le passé radiés de n°3:", 0, 20, 0)

            xp3_ape = st.slider("Nombre d'entreprises ouvertes dans le passé par n°3 correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
        with col4:
            xp4 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°4 :", 0, 20, 0)

            xp4_rad = st.slider("Nombre d'entreprises ouvertes dans le passé radiés de n°4:", 0, 20, 0)

            xp4_ape = st.slider("Nombre d'entreprises ouvertes dans le passé par n°4 correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
        with col5:
            xp5 = st.slider("Nombre d'entreprises ouvertes dans le passé par n°5 :", 0, 20, 0)

            xp5_rad = st.slider("Nombre d'entreprises ouvertes dans le passé radiés de n°5:", 0, 20, 0)

            xp5_ape = st.slider("Nombre d'entreprises ouvertes dans le passé par n°5 correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)

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
        sumxp_rad = xp1_rad + xp2_rad + xp3_rad + xp4_rad + xp5_rad
        sumxp_ape = xp1_ape + xp2_ape + xp3_ape + xp4_ape + xp5_ape
        mean_age = (age1 + age2 + age3 + age4 + age5)/5
    st.write(f"Total d'entreprises ouvertes par les associés : {sumxp}")
    st.write(f"Age moyen des associés : {mean_age}")

elif personneMorale_in == "Ouvrir une activité en tant qu'entrepreneur individuel":
    personneMorale = 1
    micro = 0
    nb_associe = 1
    xp1 = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
            
    xp1_rad = st.slider("Votre nombre d'entreprises ouvertes dans le passé radiés:", 0, 20, 0)

    xp1_ape = st.slider("Votre nombre d'entreprises ouvertes dans le passé correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
    age1 = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
    sumxp = xp1
    sumxp_rad = xp1_rad
    sumxp_ape = xp1_ape
    mean_age = age1
    st.write(f"Total d'entreprises ouvertes : {sumxp}")
else:
    personneMorale = 1
    micro = 1
    nb_associe = 1
    xp1 = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
            
    xp1_rad = st.slider("Votre nombre d'entreprises ouvertes dans le passé radiés:", 0, 20, 0)

    xp1_ape = st.slider("Votre nombre d'entreprises ouvertes dans le passé correspondants à l'activité envisagée aujourd'hui:", 0, 20, 0)
    age1 = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
    sumxp = xp1
    sumxp_rad = xp1_rad
    sumxp_ape = xp1_ape
    mean_age = age1
    st.write(f"Total d'entreprises ouvertes : {sumxp}")


# Liste des départements d'Île-de-France
departements_idf = [
    "Paris (75)",
    "Seine-et-Marne (77)",
    "Yvelines (78)",
    "Essonne (91)",
    "Hauts-de-Seine (92)",
    "Seine-Saint-Denis (93)",
    "Val-de-Marne (94)",
    "Val-d’Oise (95)"
]

#Département
dep_selectionne = st.selectbox("Sélectionnez votre département :", departements_idf)

st.write(f"Département choisi : {dep_selectionne}")

if dep_selectionne == "Paris (75)":
    cp = "75"
elif dep_selectionne == "Seine-et-Marne (77)":
    cp = "77"
elif dep_selectionne == "Yvelines (78)":
    cp = "78"
elif dep_selectionne == "Essonne (91)":
    cp = "91"
elif dep_selectionne == "Hauts-de-Seine (92)":
    cp = "92"
elif dep_selectionne == "Seine-Saint-Denis (93)":
    cp = "93"    
elif dep_selectionne == "Val-de-Marne (94)":
    cp = "94"
else:
    cp = "95"



#Import des data frames utiles
@st.cache_data
def import_base():
    data = load_base()
    return data

@st.cache_data
def import_ville():
    data = load_base_ville()
    data["code_postal"] = data["code_postal"].astype(str)
    data["cp"] = data["code_postal"].str[:2]
    return data

def is_adresse(adresse_input):
    # Adresse à rechercher
    query = adresse_input

    # Requête à l'API officielle
    response = requests.get(f"https://api-adresse.data.gouv.fr/search/?q={query}")
    data = response.json()

    # Extraction de l'adresse, latitude et longitude
    results = []
    for feature in data["features"]:
        adresse = feature["properties"]["label"]
        lon, lat = feature["geometry"]["coordinates"]
        results.append({
            "adresse": adresse,
            "latitude": lat,
            "longitude": lon
        })
    return results



codes_postaux_paris = [
    "75001", "75002", "75003", "75004", "75005", "75006", "75007", "75008", "75009", "75010",
    "75011", "75012", "75013", "75014", "75015", "75016", "75017", "75018", "75019", "75020"
]

base_df = import_base()
ville_df = import_ville()

df_select = ville_df.loc[ville_df["cp"] == cp]
nom_ville_maj = df_select["nom_standard_majuscule"]
cp_ville = ville_df.loc[ville_df["cp"] == cp]["code_postal"]
codeInsee_ville = ville_df["code_insee"]

#Ville
ville_selectionne = st.selectbox("La ville dans laquelle vous souhaitez ouvrir votre activité : ", list(nom_ville_maj))

ville = ville_selectionne.upper()

codeInseeCommune = df_select.loc[df_select["nom_standard_majuscule"] == ville]["code_insee"].iloc[0]


st.write(f"Ville selectionnée : {ville_selectionne} | Code Insee : {codeInseeCommune}")

if cp !="75":
    code_postal= st.selectbox("Code postal :", list(cp_ville))
else:
    code_postal= st.selectbox("Code postal :", codes_postaux_paris)


nomvoie_select = st.text_input("Adresse envisagé pour l'ouverture de votre activité :", "Exemple : 64 Mail de la Fontaine Ronde")

if nomvoie_select != "Exemple : 64 Mail de la Fontaine Ronde":
    adresse_tot =  nomvoie_select.lower() + " ," + ville.lower()

    is_adresse_dict = is_adresse(adresse_tot)
    is_adresse_tot = is_adresse_dict[0]["adresse"]

    st.write(f"Votre adresse : {is_adresse_tot}")
