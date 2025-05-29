-- Création de la base de données
CREATE DATABASE IF NOT EXISTS projet_hotel;
USE projet_hotel;

-- Table Hotel
CREATE TABLE Hotel (
    Id_Hotel INT AUTO_INCREMENT PRIMARY KEY,
    Ville VARCHAR(100),
    Pays VARCHAR(100),
    Code_postal INT
);

-- Table Type_Chambre
CREATE TABLE Type_Chambre (
    Id_Type INT AUTO_INCREMENT PRIMARY KEY,
    Type VARCHAR(50),
    Tarif DECIMAL(10,2)
);

-- Table Chambre
CREATE TABLE Chambre (
    Id_Chambre INT AUTO_INCREMENT PRIMARY KEY,
    Numero INT,
    Etage INT,
    Fumeur BOOLEAN,
    Id_Hotel INT,
    Id_Type INT,
    FOREIGN KEY (Id_Hotel) REFERENCES Hotel(Id_Hotel),
    FOREIGN KEY (Id_Type) REFERENCES Type_Chambre(Id_Type)
);

-- Table Client
CREATE TABLE Client (
    Id_Client INT AUTO_INCREMENT PRIMARY KEY,
    Adresse VARCHAR(255),
    Ville VARCHAR(100),
    Code_postal INT,
    Email VARCHAR(100),
    Telephone VARCHAR(20),
    Nom_complet VARCHAR(100)
);

-- Table Prestation
CREATE TABLE Prestation (
    Id_Prestation INT AUTO_INCREMENT PRIMARY KEY,
    Prix DECIMAL(10,2),
    Description TEXT
);

-- Table Reservation
CREATE TABLE Reservation (
    Id_Reservation INT AUTO_INCREMENT PRIMARY KEY,
    Date_arrivee DATE,
    Date_depart DATE,
    Id_Client INT,
    FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client)
);

-- Table Evaluation
CREATE TABLE Evaluation (
    Id_Evaluation INT AUTO_INCREMENT PRIMARY KEY,
    Date_eval DATE,
    Note INT,
    Commentaire TEXT,
    Id_Client INT,
    FOREIGN KEY (Id_Client) REFERENCES Client(Id_Client)
);

-- Table de liaison Reservation_Chambre
CREATE TABLE Reservation_Chambre (
    Id_Reservation INT,
    Id_Chambre INT,
    PRIMARY KEY (Id_Reservation, Id_Chambre),
    FOREIGN KEY (Id_Reservation) REFERENCES Reservation(Id_Reservation),
    FOREIGN KEY (Id_Chambre) REFERENCES Chambre(Id_Chambre)
);

-- Table de liaison Reservation_Prestation
CREATE TABLE Reservation_Prestation (
    Id_Reservation INT,
    Id_Prestation INT,
    PRIMARY KEY (Id_Reservation, Id_Prestation),
    FOREIGN KEY (Id_Reservation) REFERENCES Reservation(Id_Reservation),
    FOREIGN KEY (Id_Prestation) REFERENCES Prestation(Id_Prestation)
);