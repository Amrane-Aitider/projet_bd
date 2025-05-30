import streamlit as st
import sqlite3
from datetime import date

# Connexion à la base de données
def connect_db():
    return sqlite3.connect("hotel.db")

# Récupérer les clients pour les menus déroulants
def get_clients():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom FROM Client")
    return cursor.fetchall()

# Titre de l’application
st.set_page_config(page_title="Gestion Hôtelière", layout="wide")
st.title("🏨 Application de Gestion Hôtelière")

menu = ["📋 Réservations", "👥 Clients", "🔍 Chambres disponibles", "➕ Ajouter un client", "📆 Ajouter une réservation"]
choice = st.sidebar.radio("Navigation", menu)

conn = connect_db()
cursor = conn.cursor()

# --------------------------
# 📋 Liste des Réservations
# --------------------------
if choice == "📋 Réservations":
    st.header("📋 Liste des Réservations")
    rows = cursor.execute('''
        SELECT R.id, C.nom, R.date_debut, R.date_fin
        FROM Reservation R
        JOIN Client C ON R.id_client = C.id
        ORDER BY R.date_debut
    ''').fetchall()

    if rows:
        for row in rows:
            st.markdown(f"🔹 **{row[1]}** a réservé du **{row[2]}** au **{row[3]}** (ID réservation : {row[0]})")
    else:
        st.info("Aucune réservation trouvée.")

# --------------------------
# 👥 Liste des Clients
# --------------------------
elif choice == "👥 Clients":
    st.header("👥 Liste des Clients")
    rows = cursor.execute('SELECT id, nom, email, ville FROM Client').fetchall()

    if rows:
        for row in rows:
            st.write(f"🧍 ID: {row[0]} - {row[1]} ({row[2]}) - Ville : {row[3]}")
    else:
        st.info("Aucun client enregistré.")

# --------------------------
# 🔍 Recherche de chambres
# --------------------------
elif choice == "🔍 Chambres disponibles":
    st.header("🔍 Rechercher des chambres disponibles")
    col1, col2 = st.columns(2)
    with col1:
        date_debut = st.date_input("📅 Date de début", value=date.today())
    with col2:
        date_fin = st.date_input("📅 Date de fin", value=date.today())

    if st.button("🔎 Rechercher"):
        query = '''
        SELECT id, numero, etage, fumeur FROM Chambre WHERE id NOT IN (
            SELECT id FROM Chambre
            WHERE id IN (
                SELECT id FROM Reservation
                WHERE NOT (date_fin < ? OR date_debut > ?)
            )
        )
        '''
        rows = cursor.execute(query, (date_debut, date_fin)).fetchall()
        if rows:
            for row in rows:
                fumeur = "🚬" if row[3] else "🚭"
                st.success(f"Chambre {row[1]} (Étage {row[2]}) - ID: {row[0]} {fumeur}")
        else:
            st.warning("Aucune chambre disponible pour cette période.")

# --------------------------
# ➕ Ajouter un client
# --------------------------
elif choice == "➕ Ajouter un client":
    st.header("➕ Ajout d’un nouveau client")
    with st.form("form_client"):
        nom = st.text_input("Nom complet")
        email = st.text_input("Email")
        adresse = st.text_input("Adresse")
        ville = st.text_input("Ville")
        code_postal = st.number_input("Code postal", step=1)
        telephone = st.text_input("Téléphone")

        submitted = st.form_submit_button("Ajouter")
        if submitted:
            cursor.execute('''
                INSERT INTO Client (adresse, ville, code_postal, email, telephone, nom)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (adresse, ville, code_postal, email, telephone, nom))
            conn.commit()
            st.success(f"✅ Client {nom} ajouté avec succès.")

# --------------------------
# 📆 Ajouter une réservation
# --------------------------
elif choice == "📆 Ajouter une réservation":
    st.header("📆 Nouvelle Réservation")
    clients = get_clients()
    client_dict = {nom: id for id, nom in clients}
    nom_client = st.selectbox("Choisir un client", list(client_dict.keys()))
    id_client = client_dict[nom_client]

    date_debut = st.date_input("📅 Date de début", value=date.today())
    date_fin = st.date_input("📅 Date de fin", value=date.today())

    if st.button("Valider la réservation"):
        cursor.execute('''
            INSERT INTO Reservation (date_debut, date_fin, id_client)
            VALUES (?, ?, ?)
        ''', (date_debut, date_fin, id_client))
        conn.commit()
        st.success(f"✅ Réservation ajoutée pour {nom_client} du {date_debut} au {date_fin}")

conn.close()
