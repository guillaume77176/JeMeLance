import streamlit as st


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

st.markdown(f"""
<style>
#logo {{
    position: fixed;
    top: 30px;
    left: 3px;
    width: 300px;
    z-index: 100;
}}
</style>

<img id="logo" src="{logo_url}">
""", unsafe_allow_html=True)

st.title("Je me lance ? 🤔 🚀🚀🚀")

st.markdown(
    "<h1 style='font-family:Arial; font-size:20px; color:White;'>Avec JeMeLance, n'ayez plus de doutes sur votre projet d'entreprise ! Envie de démarrer une activité dans les secteurs du commerce et de l'artisanat ? Entrer vos informations personnelles et une description brève de votre projet pour connaitre vos chances de réusssir !</h1>",
    unsafe_allow_html=True
)

# Une seule ligne de texte
objet = st.text_input("Votre projet brièvement (Exemple : Food truck burger) :")


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



