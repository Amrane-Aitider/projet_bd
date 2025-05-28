import streamlit as st
import sqlite3
from datetime import date

# Connexion
def connect_db():
    return sqlite3.connect("hotel.db")

st.title("Gestion Hôtelière")

menu = ["Liste des réservations", "Liste des clients", "Chambres disponibles", "Ajouter un client", "Ajouter une réservation"]
choice = st.sidebar.selectbox("Menu", menu)

conn = connect_db()
cursor = conn.cursor()

# 1. Liste des réservations
if choice == "Liste des réservations":
    st.header("Réservations")
    rows = cursor.execute('''
        SELECT R.id, C.nom, R.date_debut, R.date_fin
        FROM Reservation R JOIN Client C ON R.id_client = C.id
    ''').fetchall()
    for row in rows:
        st.write(f"ID: {row[0]} - Client: {row[1]} - Du {row[2]} au {row[3]}")

# 2. Liste des clients
elif choice == "Liste des clients":
    st.header("Clients")
    rows = cursor.execute('SELECT id, nom, email FROM Client').fetchall()
    for row in rows:
        st.write(f"ID: {row[0]} - {row[1]} ({row[2]})")

# 3. Chambres disponibles
elif choice == "Chambres disponibles":
    st.header("Chambres disponibles")
    start = st.date_input("Date de début", date.today())
    end = st.date_input("Date de fin", date.today())
    if st.button("Rechercher"):
        query = '''
            SELECT * FROM Chambre WHERE id NOT IN (
                SELECT id FROM Chambre
                WHERE id IN (
                    SELECT id FROM Reservation
                    WHERE NOT (date_fin < ? OR date_debut > ?)
                )
            )
        '''
        rows = cursor.execute(query, (start, end)).fetchall()
        for row in rows:
            st.write(f"Chambre ID: {row[0]}, Numéro: {row[1]}")

# 4. Ajouter un client
elif choice == "Ajouter un client":
    st.header("Ajout d’un client")
    nom = st.text_input("Nom")
    email = st.text_input("Email")
    adresse = st.text_input("Adresse")
    ville = st.text_input("Ville")
    code_postal = st.number_input("Code postal", step=1)
    telephone = st.text_input("Téléphone")

    if st.button("Ajouter"):
        cursor.execute('''
            INSERT INTO Client (adresse, ville, code_postal, email, telephone, nom)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (adresse, ville, code_postal, email, telephone, nom))
        conn.commit()
        st.success("Client ajouté")

# 5. Ajouter une réservation
elif choice == "Ajouter une réservation":
    st.header("Nouvelle réservation")
    client_id = st.number_input("ID client", step=1)
    date_debut = st.date_input("Date début")
    date_fin = st.date_input("Date fin")
    if st.button("Réserver"):
        cursor.execute('''
            INSERT INTO Reservation (date_debut, date_fin, id_client)
            VALUES (?, ?, ?)
        ''', (date_debut, date_fin, client_id))
        conn.commit()
        st.success("Réservation ajoutée")

conn.close()
