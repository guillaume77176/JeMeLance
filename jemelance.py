import streamlit as st
from src.load_xgb import load_model, load_threshold
from src.data.load_idf_10_24 import load_base, load_base_ville
from src.nlp import predict_ape
import time
import requests
import pandas as pd
import json
import joblib
import os
import s3fs
from datetime import datetime

st.markdown('<div id="top"></div>', unsafe_allow_html=True)

# ----------------- Background et logo -----------------
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

st.markdown(f"""
<div style="
    background-color: #fff8e1;  /* fond jaune très clair */
    color: #333333;              /* texte sombre */
    padding: 15px 20px;          /* espace intérieur */
    border-left: 5px solid #f7c948; /* accent coloré à gauche */
    border-radius: 8px;          /* coins arrondis */
    font-size: 14px;             /* texte lisible */
    font-family: 'Segoe UI', Tahoma, sans-serif;
    max-width: 700px;            /* largeur max */
    margin: 15px auto;           /* centrer horizontalement */
    box-shadow: 0 2px 4px rgba(0,0,0,0.1); /* ombre légère */
    line-height: 1.5;
">
<b>A propos de la fiabilité des résultats :</b> Évalué sur plus de dix ans de données cumulées, le modèle prédit correctement en moyenne 70% des entreprises qui ont été effectivement radiées au cours des cinq années suivant la création. Nous mettons en garde l'utilisateur avisé sur le fait que le modèle a tendance à donner de fausses alertes sur les chances d'échouer. Autrement dit, il se montre souvent pessimiste. Il ne doit servir en aucun cas d'outil de décision final, mais est une simple vue globale de la réalité du tissu entrepreneurial d'Île-de-France des 15 dernières années.
</div>
""", unsafe_allow_html=True)



# ----------------- Initialisation session_state -----------------
if "last_objet" not in st.session_state:
    st.session_state.last_objet = ""

if "codeAPE" not in st.session_state:
    st.session_state.codeAPE = ""  

if "montantCapital" not in st.session_state:
    st.session_state.montantCapital = 0

if "prenom" not in st.session_state:
    st.session_state.prenom = ""  

if "nom" not in st.session_state:
    st.session_state.nom = ""


col1,col2 = st.columns(2)

with col1:
    st.session_state.prenom = st.text_input("Votre prénom : ", " ")
with col2:
    st.session_state.nom = st.text_input("Votre nom : ", " ")




# ----------------- Fonction debounce -----------------
def debounce(seconds=0.4):
    time.sleep(seconds)

# ----------------- Input projet -----------------
objet = st.text_input("Votre projet brièvement (Exemple : Food truck burger) :")

if "last_objet" not in st.session_state:
    st.session_state.last_objet = ""

if objet != st.session_state.last_objet and objet != "":
    st.session_state.last_objet = objet
    debounce(0.4)

    # --- BARRE DE CHARGEMENT ---
    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.3)
        progress.progress(i + 1)

    # --- PRÉDICTION APE ---
    objet_predict = predict_ape(objet)
    progress.empty()

    st.session_state.codeAPE = objet_predict[0]
    ex_text = objet_predict[2][0]

    st.write("Description chargée. Vous pouvez continuer.")
    st.write(f"Code APE correspondant : {st.session_state.codeAPE}")
    st.write(f"Activités en lien avec : {ex_text}")

# ----------------- Capital -----------------
capital = st.text_input("Montant du capital social initial prévu :", "")

try:
    montantCapital = float(capital)
    st.session_state.montantCapital = montantCapital
    st.write("Votre capital social initial :", montantCapital)
except ValueError:
    st.write("Veuillez entrer un nombre valide.")

# ----------------- Type de société -----------------
personneMorale_in = st.radio(
    "Vous souhaitez :",
    ["Ouvrir une micro-entreprise", "Ouvrir une activité en tant qu'entrepreneur individuel", "Ouvrir une entreprise de type SARL, SAS, EIRL"]
)

# Initialisation
st.session_state.sumxp = 0
st.session_state.mean_age = 0
st.session_state.sumxp_rad = 0
st.session_state.sumxp_ape = 0
st.session_state.nb_associe = 1
st.session_state.micro = 0
st.session_state.personneMorale = 1

# ----------------- Sliders et inputs associés -----------------
if personneMorale_in == "Ouvrir une entreprise de type SARL, SAS, EIRL":
    st.session_state.personneMorale = 1
    st.session_state.micro = 0
    st.session_state.nb_associe = st.slider(
        "Nombre d'associé prévu (max 5, si vous êtes seul selectionnez 1):", 1, 5, 1
    )

    nb_associe = st.session_state.nb_associe

    # Génération des sliders et ages
    age_list = []
    xp_list = []
    xp_rad_list = []
    xp_ape_list = []

    cols = st.columns(nb_associe)
    for i in range(nb_associe):
        with cols[i]:
            xp = st.slider(f"Nombre d'entreprises ouvertes dans le passé par n°{i+1} :", 0, 20, 0)
            xp_rad = st.slider(f"Nombre d'entreprises ouvertes dans le passé radiés de n°{i+1}:", 0, 20, 0)
            xp_ape = st.slider(f"Nombre d'entreprises ouvertes dans le passé correspondants à l'activité envisagée aujourd'hui par n°{i+1}:", 0, 20, 0)
            age = st.number_input(f"Quel est l'âge de n°{i+1} ?", min_value=0, max_value=120, value=30, step=1)
            xp_list.append(xp)
            xp_rad_list.append(xp_rad)
            xp_ape_list.append(xp_ape)
            age_list.append(age)

    st.session_state.sumxp = sum(xp_list)
    st.session_state.sumxp_rad = sum(xp_rad_list)
    st.session_state.sumxp_ape = sum(xp_ape_list)
    st.session_state.mean_age = sum(age_list)/len(age_list)

    st.write(f"Total d'entreprises ouvertes par les associés : {st.session_state.sumxp}")
    st.write(f"Age moyen des associés : {st.session_state.mean_age}")

elif personneMorale_in == "Ouvrir une activité en tant qu'entrepreneur individuel":
    st.session_state.personneMorale = 0
    st.session_state.micro = 0
    st.session_state.nb_associe = 1

    st.session_state.sumxp = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
    st.session_state.sumxp_rad = st.slider("Nombre d'entreprises ouvertes dans le passé radiés :", 0, 20, 0)
    st.session_state.sumxp_ape = st.slider("Correspondant à l'activité envisagée :", 0, 20, 0)
    st.session_state.mean_age = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
    st.write(f"Total d'entreprises ouvertes : {st.session_state.sumxp}")

else:
    st.session_state.personneMorale = 0
    st.session_state.micro = 1
    st.session_state.nb_associe = 1
    st.session_state.sumxp = st.slider("Votre nombre d'entreprises ouvertes dans le passé :", 0, 20, 0)
    st.session_state.sumxp_rad = st.slider("Nombre d'entreprises ouvertes dans le passé radiés :", 0, 20, 0)
    st.session_state.sumxp_ape = st.slider("Correspondant à l'activité envisagée :", 0, 20, 0)
    st.session_state.mean_age = st.number_input("Quel est votre âge ?", min_value=0, max_value=120, value=30, step=1)
    st.write(f"Total d'entreprises ouvertes : {st.session_state.sumxp}")

# ----------------- Département -----------------
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

dep_selectionne = st.selectbox("Sélectionnez votre département :", departements_idf)
st.session_state.cp = dep_selectionne.split("(")[1].replace(")", "")
st.write(f"Département choisi : {dep_selectionne}")

# ----------------- Import data -----------------
@st.cache_data
def import_base():
    data = load_base()
    data["taille_ville"] = data["pop_commune"].apply(
        lambda x: "village" if x < 5000
        else "little" if x < 25000
        else "middle" if x < 50000
        else "big"
    )
    data["cp"] = data["code_postal"].str[:2]
    return data

@st.cache_data
def import_ville():
    data = load_base_ville()
    data["code_postal"] = data["code_postal"].astype(str)
    data["cp"] = data["code_postal"].str[:2]
    return data

def is_adresse(adresse_input):
    response = requests.get(f"https://api-adresse.data.gouv.fr/search/?q={adresse_input}")
    data = response.json()
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

def get_info_local(base_df, code_insee, code_ape):
    code_ape = str(code_ape)
    code_insee = str(code_insee)
    base_df["codeInseeCommune"] = base_df["codeInseeCommune"].astype(str)

    if code_insee != "75056":
        info_df = base_df.loc[base_df["codeInseeCommune"] == code_insee]
        concu_df = base_df.loc[(base_df["codeInseeCommune"] == code_insee) & (base_df["codeAPE"] == code_ape)]
    else:
        info_df = base_df.loc[base_df["cp"] == "75"]
        concu_df = base_df.loc[(base_df["cp"] == "75") & (base_df["codeAPE"] == code_ape)]

    nb_local_concurrents = concu_df["nb_local_concurrents"].iloc[0] if not concu_df.empty else 0
    revCommune = info_df["revCommune"].iloc[0]
    revDep = info_df["revDep"].iloc[0]
    taille_ville = info_df["taille_ville"].iloc[0]

    return revCommune, revDep, taille_ville, nb_local_concurrents

# ----------------- Ville -----------------

codes_postaux_paris = [f"750{i:02}" for i in range(1, 21)]
base_df = import_base()
ville_df = import_ville()
df_select = ville_df.loc[ville_df["cp"] == st.session_state.cp]
nom_ville_maj = df_select["nom_standard_majuscule"]
cp_ville = df_select["code_postal"]

ville_selectionne = st.selectbox("La ville dans laquelle vous souhaitez ouvrir votre activité : ", list(nom_ville_maj))
ville = ville_selectionne.upper()
codeInseeCommune = df_select.loc[df_select["nom_standard_majuscule"] == ville]["code_insee"].iloc[0]
st.session_state.codeInseeCommune = codeInseeCommune
st.write(f"Ville selectionnée : {ville_selectionne} | Code Insee : {codeInseeCommune}")

if st.session_state.cp != "75":
    code_postal = st.selectbox("Code postal :", list(cp_ville))
else:
    code_postal = st.selectbox("Code postal :", codes_postaux_paris)
st.session_state.code_postal = code_postal

nomvoie_select = st.text_input("Adresse envisagé pour l'ouverture de votre activité :", "Exemple : 64 Mail de la Fontaine Ronde")

if nomvoie_select != "Exemple : 64 Mail de la Fontaine Ronde":
    adresse_tot =  nomvoie_select.lower() + " ," + ville.lower()
    try:
        is_adresse_dict = is_adresse(adresse_tot)
        is_adresse_tot = is_adresse_dict[0]["adresse"]
        st.write(f"Votre adresse : {is_adresse_tot}")
    except IndexError:
        st.write("Veuillez rentrer une adresse valide.")


# ----------------- Info locale -----------------
try:
    info_local = get_info_local(base_df, st.session_state.codeInseeCommune, st.session_state.codeAPE)
    st.session_state.revCommune = info_local[0]
    st.session_state.revDep = info_local[1]
    st.session_state.taille_ville = info_local[2]
    st.session_state.nb_local_concurrents = info_local[3]
except NameError as e:
    st.write("Nous sommes désoler, votre adresse n'est pas encore disponible.")
except IndexError:
    st.write("Nous sommes désoler, votre adresse n'est pas encore disponible.")

                            ####################################################
                            #################### PREDICTION ####################
                            ####################################################

try:
    var_cand = [
        st.session_state.cp,
        st.session_state.taille_ville,
        st.session_state.mean_age,
        st.session_state.nb_associe,
        st.session_state.nb_local_concurrents,
        st.session_state.revCommune,
        st.session_state.sumxp,
        st.session_state.sumxp_rad,
        st.session_state.sumxp_ape,
        st.session_state.codeAPE,
        st.session_state.montantCapital,
        st.session_state.personneMorale,
        st.session_state.micro,
        st.session_state.revDep
    ]

except NameError as e:
    st.markdown(
        f"<span style='color:red'>Erreur : {e}. Veuillez renseigner l'ensemble des informations pour effectuer une prédiction.</span>",
        unsafe_allow_html=True
    )

st.write("Récapitualtif de vos saisis : ")
df_predict = pd.DataFrame([var_cand],columns = ["cp","taille_ville","mean_age","nb_associe","nb_local_concurrents",
"revCommune","sumxp","sumxp_rad","sumxp_ape","codeAPE","montantCapital","personneMorale","micro","revDep"])


df_recap = pd.DataFrame([var_cand],columns = ["code_postal","Taille moyenne de votre ville","Moyenne d'âge des associés","Nombre d'associés","Nombre estimé de vos concurents locaux",
"Revenue moyen des habitants locaux","Total des expériences","Total des expériences radiées","Total des expériences cohérentes avec votre projet","APE de votre activité","Capital social envisagé","Vous êtes une personne morale (1)","Micro (1)","Revenue moyen des habitants département"])


st.dataframe(df_recap)

# ----------------- Bouton prédiction -----------------
bouton = st.button("Lancer la prédiction : Vais-je me lancer ?")

if bouton == True:
    # ----------------- Fonctions de récupération des modèles et des seuils -----------------
    @st.cache_resource
    def load_model():
        
        model1 = joblib.load("src/xgb_radié1.pkl")
        model2 = joblib.load("src/xgb_radié2.pkl")
        model3 = joblib.load("src/xgb_radié3.pkl")
        model4 = joblib.load("src/xgb_radié4.pkl")
        model5 = joblib.load("src/xgb_radié5.pkl")

        return model1,model2,model3,model4,model5

    @st.cache_data
    def load_threshold():

        with open("src/seuils_proba_xgb.json", "r") as f:
            liste_th = json.load(f)
            
        return liste_th

    models_list = load_model()
    seuils_list = load_threshold()

    # ----------------- Prédiction selon les années i après la création -----------------

    model1 = models_list[0]
    model2 = models_list[1]
    model3 = models_list[2]
    model4 = models_list[3]
    model5 = models_list[4]

    th1 = seuils_list[0]
    th2 = seuils_list[1]
    th3 = seuils_list[2]
    th4 = seuils_list[3]
    th5 = seuils_list[4]

    prob1 = model1.predict_proba(df_predict)[:,1]
    prob2 = model2.predict_proba(df_predict)[:,1]
    prob3 = model3.predict_proba(df_predict)[:,1]
    prob4 = model4.predict_proba(df_predict)[:,1]
    prob5 = model5.predict_proba(df_predict)[:,1]


    radié1_pred = [1 if p >= th1 else 0 for p in prob1][0]
    radié2_pred = [1 if p >= th2 else 0 for p in prob2][0]
    radié3_pred = [1 if p >= th3 else 0 for p in prob3][0]
    radié4_pred = [1 if p >= th4 else 0 for p in prob4][0]
    radié5_pred = [1 if p >= th5 else 0 for p in prob5][0]

    radié_list = [radié1_pred,radié2_pred,radié3_pred,radié4_pred,radié5_pred]

    st.markdown("""
        <style>
            .pred-container {
                text-align: center;
                margin-top: 30px;
                font-family: 'Inter', sans-serif;
            }
            .pred-title {
                font-size: 28px;
                font-weight: 600;
                margin-bottom: 25px;
                color: #333333;
            }
            .pred-card {
                background: #ffffff;
                padding: 25px;
                margin: 20px auto;
                width: 75%;
                border-radius: 14px;
                box-shadow: 0px 4px 16px rgba(0,0,0,0.10);
                font-size: 18px;
                line-height: 1.6;
                text-align: center;
            }
            .pred-ok {
                color: #117A65;
                font-weight: 600;
            }
            .pred-risk {
                color: #C0392B;
                font-weight: 600;
            }
        </style>
    """, unsafe_allow_html=True)




    radié_list = [radié1_pred, radié2_pred, radié3_pred, radié4_pred, radié5_pred]
    messages_pred = []

    for i in range(5):
        pred = radié_list[i]

        if pred == 0:
            messages_pred.append({
                "annee": i+1,
                "msg": f"A priori, il y a peu de chances pour que votre activité soit radiée au cours de l'année {i} après sa création. Feu vert pour l'instant.",
                "type": "ok"
            })
        else:
            messages_pred.append({
                "annee": i+1,
                "msg": f"Cependant, il semblerait qu'il y ait de fortes chances que votre activité soit radiée au cours de l'année {i}. Penchez-vous davantage sur l'évaluation du projet !",
                "type": "risk"
            })
            break

    #si pas de radiation jusqu'à l'année 5
    if len(messages_pred) == 5 and radié_list[-1] == 0:
        messages_pred.append({
            "annee": 5,
            "msg": "A priori, il y a peu de chances pour que votre activité soit radiée dans les 5 ans suivant sa création. LANCEZ-VOUS !!!",
            "type": "ok"
        })



    st.markdown("""
    <div class="pred-container">
        <div class="pred-title" style="color:#F1C40F;">📊 Résultats de la prédiction</div>
    </div>
    """, unsafe_allow_html=True)

    for item in messages_pred:
        classe = "pred-ok" if item["type"] == "ok" else "pred-risk"
        st.markdown(
            f"""
            <div class="pred-card">
                <strong style="color: black;">Année {item['annee']} après la création — Feu vert ? </strong><br><br>
                <span class="{classe}">{item['msg']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )


    #bouton pour retourner en haut"
    st.markdown("""
    <div style="text-align:center; margin-top:20px;">
        <a href="#top" style="
            text-decoration:none;
            background-color:#f7c948;
            color:#111;
            padding:10px 20px;
            border-radius:5px;
            font-weight:bold;
            font-family:'Segoe UI', Tahoma, sans-serif;
        ">🔝 Nouvelles idées ?</a>
    </div>
    """, unsafe_allow_html=True)

    now = datetime.now()

    list_log = var_cand + radié_list + [st.session_state.prenom, st.session_state.nom, now]

    data_log = pd.DataFrame([list_log],columns = ["cp","taille_ville","mean_age","nb_associe","nb_local_concurrents",
    "revCommune","sumxp","sumxp_rad","sumxp_ape","codeAPE","montantCapital","personneMorale","micro","revDep","radié1",
    "radié2","radié3","radié4","radié5","prenom","nom","date"])

    url_log = "https://minio.lab.sspcloud.fr/guillaume176/diffusion/data_app/log.parquet"
    past_log = pd.read_parquet(url_log)

    data_log = pd.concat([past_log,data_log])



    t1 = st.secrets["DB_1"]
    t2 = st.secrets["DB_1_1"]
    t3 = st.secrets["DB_1_2"]

    os.environ["AWS_ACCESS_KEY_ID"] = t1
    os.environ["AWS_SECRET_ACCESS_KEY"] = t2
    os.environ["AWS_SESSION_TOKEN"] = t3
    os.environ["AWS_DEFAULT_REGION"] = 'us-east-1'
    fs = s3fs.S3FileSystem(
        client_kwargs={'endpoint_url': 'https://'+'minio.lab.sspcloud.fr'},
        key = os.environ["AWS_ACCESS_KEY_ID"], 
        secret = os.environ["AWS_SECRET_ACCESS_KEY"], 
        token = os.environ["AWS_SESSION_TOKEN"])

    #Stockage sur S3
    MY_BUCKET = "guillaume176"

    FILE_PATH_OUT_S3 = f"{MY_BUCKET}/diffusion/data_app/log.parquet"

    with fs.open(FILE_PATH_OUT_S3,"wb") as file_out:
        data_log.to_parquet(file_out, index=False)

    print(f"Donnés chargés dans {FILE_PATH_OUT_S3}")