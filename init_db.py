import sqlite3

conn = sqlite3.connect('hotel.db')
cursor = conn.cursor()

# Création des tables
cursor.execute('''
CREATE TABLE Hotel (
    id INTEGER PRIMARY KEY,
    ville TEXT,
    pays TEXT,
    code_postal INTEGER
)
''')

cursor.execute('''
CREATE TABLE Client (
    id INTEGER PRIMARY KEY,
    adresse TEXT,
    ville TEXT,
    code_postal INTEGER,
    email TEXT,
    telephone TEXT,
    nom TEXT
)
''')

cursor.execute('''
CREATE TABLE Prestation (
    id INTEGER PRIMARY KEY,
    prix INTEGER,
    description TEXT
)
''')

cursor.execute('''
CREATE TABLE TypeChambre (
    id INTEGER PRIMARY KEY,
    nom TEXT,
    prix REAL
)
''')

cursor.execute('''
CREATE TABLE Chambre (
    id INTEGER PRIMARY KEY,
    numero INTEGER,
    etage INTEGER,
    fumeur INTEGER,
    id_type INTEGER,
    id_hotel INTEGER,
    FOREIGN KEY(id_type) REFERENCES TypeChambre(id),
    FOREIGN KEY(id_hotel) REFERENCES Hotel(id)
)
''')

cursor.execute('''
CREATE TABLE Reservation (
    id INTEGER PRIMARY KEY,
    date_debut TEXT,
    date_fin TEXT,
    id_client INTEGER,
    FOREIGN KEY(id_client) REFERENCES Client(id)
)
''')

cursor.execute('''
CREATE TABLE Evaluation (
    id INTEGER PRIMARY KEY,
    date TEXT,
    note INTEGER,
    commentaire TEXT,
    id_client INTEGER,
    FOREIGN KEY(id_client) REFERENCES Client(id)
)
''')

# Insertion des données (exemples)
hotels = [
    (1, 'Paris', 'France', 75001),
    (2, 'Lyon', 'France', 69002)
]

clients = [
    (1, '12 Rue de Paris', 'Paris', 75001, 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
    (2, '5 Avenue Victor Hugo', 'Lyon', 69002, 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
    (3, '8 Boulevard Saint-Michel', 'Marseille', 13005, 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
    (4, '27 Rue Nationale', 'Lille', 59800, 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
    (5, '3 Rue des Fleurs', 'Nice', 6000, 'emma.giraud@email.fr', '0656789012', 'Emma Giraud')
]
# Données à insérer

prestations = [
    (1, 15, 'Petit-déjeuner'),
    (2, 30, 'Navette aéroport'),
    (3, 0, 'Wi-Fi gratuit'),
    (4, 50, 'Spa et bien-être'),
    (5, 20, 'Parking sécurisé')
]

types_chambres = [
    (1, 'Simple', 80),
    (2, 'Double', 120)
]

chambres = [
    (1, 201, 2, 0, 1, 1),
    (2, 502, 5, 1, 1, 2),
    (3, 305, 3, 0, 2, 1),
    (4, 410, 4, 0, 2, 2),
    (5, 104, 1, 1, 2, 2),
    (6, 202, 2, 0, 1, 1),
    (7, 307, 3, 1, 1, 2),
    (8, 101, 1, 0, 1, 1)
]

reservations = [
    # Client 1 (Jean Dupont)
    (1, '2025-06-15', '2025-06-18', 1),
    # Client 2 (Marie Leroy)
    (2, '2025-07-01', '2025-07-05', 2),
    (7, '2025-11-12', '2025-11-14', 2),
    (10, '2026-02-01', '2026-02-05', 2),
    # Client 3 (Paul Moreau)
    (3, '2025-08-10', '2025-08-14', 3),
    # Client 4 (Lucie Martin)
    (4, '2025-09-05', '2025-09-07', 4),
    (9, '2026-01-15', '2026-01-18', 4),
    # Client 5 (Emma Giraud)
    (5, '2025-09-20', '2025-09-25', 5)
]

evaluations = [
    (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
    (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
    (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
    (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
    (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5)
]

# Insertion dans la base
cursor.executemany('INSERT INTO Prestation VALUES (?, ?, ?)', prestations)
cursor.executemany('INSERT INTO TypeChambre VALUES (?, ?, ?)', types_chambres)
cursor.executemany('INSERT INTO Chambre VALUES (?, ?, ?, ?, ?, ?)', chambres)
cursor.executemany('INSERT INTO Reservation VALUES (?, ?, ?, ?)', reservations)
cursor.executemany('INSERT INTO Evaluation VALUES (?, ?, ?, ?, ?)', evaluations)


cursor.executemany('INSERT INTO Hotel VALUES (?, ?, ?, ?)', hotels)
cursor.executemany('INSERT INTO Client VALUES (?, ?, ?, ?, ?, ?, ?)', clients)

conn.commit()
conn.close()
