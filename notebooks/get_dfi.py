#packages utilisés
import pandas as pd


def load_dfi():
    from data.load_idf_10_24 import load_base
    data = load_base()

    drop = []

    autre_statutFormalites = [f"autre_{i}_statutFormalites" for i in range(1,11)]
    autre_dateeffetferm = [f"autre_{i}_dateeffetferm" for i in range(1,11)]
    autre_adresse = [f"autre_{i}_adresse" for i in range(1,11)]
    associe_naissance = [f"associe_{i}_naissance" for i in range(1,6)]

    drop.extend([*autre_statutFormalites,*autre_adresse,*autre_dateeffetferm,*associe_naissance])

    drop.extend(["age0","age1","age2","age3","age4","age5","cessation","eirl","formeExerciceActivitePrincipale",
        'dateImmat','nom', 'prenoms','principalAPEPrincipal','dateDissolutionDisparition',
        'indicateurCessationTemporaire', 'indicateurPoursuiteActivite',
        'indicateurMaintienImmatriculationRegistre', 'indicateurDissolution',
        'indicateurDisparitionPM', 'motifDisparition', 'dateMiseEnSommeil',
        'typeDissolution','diffusionINSEE','diffusionCommerciale',
        'annee_tronc','dateClotureLiquidation','dateEffet','dateDebutAct']) 

    data = data.drop(columns=drop)

    data["micro"] = data["micro"].apply(lambda x : False if (x == "None") or (x == "False") else True)
    data["micro"] = data["micro"].astype(int)

    data["etranger"] = data["etranger"].apply(lambda x : False if (x == "None") or (x == "False") else True)
    data["etranger"] = data["etranger"].astype(int)

    data["agricole"] = data["agricole"].apply(lambda x : False if (x == "None") or (x == "False") else True)
    data["agricole"] = data["agricole"].astype(int)

    data["nb_autres"] = data["nb_autres"].astype(int)

    data["dateRadiation"] = pd.to_datetime(data["dateRadiation"],errors = "coerce")

    data = data.loc[~data["mean_age"].isna()]

    data = data.loc[~data["pop_commune"].isna()]

    #Suppression des lignes pour lesquelles indicateurDecesEntrepreneur est True
    data = data.loc[data["indicateurDecesEntrepreneur"]!="True"]

    #Suppression des lignes pour lesquelles principalDateTransPrincipal est disponible 
    data = data.loc[data["principalDateTransPrincipal"].isin(("non-disp","pincipal_false_transfert"))]

    #Création de la variable T
    data["T"] = data["dateRadiation"] - data["date_creation"]


    #Suppresion des lignes pour lesquelles la différence entre la date de création et la date de radiation (T) est inférieur à 60 jours
    data = data.loc[~(data["T"].dt.days < 60)]

    #Suppression des lignes pour lesquelles date_creation > dateRadiation
    data = data.loc[~(data["T"].dt.days < 0)]

    data["T"] = data["T"].dt.days

    data["radié1"] = data.loc[~(data["T"] > 365)]["dateRadiation"].notna().astype(int)
    data["radié1"] = data["radié1"].fillna(0)

    data["radié2"] = data.loc[~(data["T"] <= 365) & ~(data["T"] > 365*2)]["dateRadiation"].notna().astype(int)
    data["radié2"] = data["radié2"].fillna(0)

    data["radié3"] = data.loc[~(data["T"] <= 365*2) & ~(data["T"] > 365*3)]["dateRadiation"].notna().astype(int)
    data["radié3"] = data["radié3"].fillna(0)

    data["radié4"] = data.loc[~(data["T"] <= 365*3) & ~(data["T"] > 365*4)]["dateRadiation"].notna().astype(int)
    data["radié4"] = data["radié4"].fillna(0)

    data["radié5"] = data.loc[~(data["T"] <= 365*4) & ~(data["T"] > 365*5)]["dateRadiation"].notna().astype(int)
    data["radié5"] = data["radié5"].fillna(0)

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

    df_list = [df1,df2,df3,df4,df5]
    for df in df_list:
        print(df.shape)
    print("Chargement effectué")

    return df_list