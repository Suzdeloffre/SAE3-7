DROP TABLE IF EXISTS passe;
DROP TABLE IF EXISTS decharge;
DROP TABLE IF EXISTS benne;
DROP TABLE IF EXISTS produit;
DROP TABLE IF EXISTS usine;
DROP TABLE IF EXISTS vehicule;
DROP TABLE IF EXISTS centre;
DROP TABLE IF EXISTS marque;
DROP TABLE IF EXISTS type_vehicule;

CREATE TABLE type_vehicule(
    num_type INT AUTO_INCREMENT,
    libelle_type VARCHAR(25),
    PRIMARY KEY (num_type)
);

CREATE TABLE marque(
    num_marque INT AUTO_INCREMENT,
    libelle_marque VARCHAR(25),
    PRIMARY KEY (num_marque)
);

CREATE TABLE centre(
   num_centre INT AUTO_INCREMENT,
   nom_centre VARCHAR(50),
   adresse_centre VARCHAR(50),
   PRIMARY KEY(num_centre)
);

CREATE TABLE vehicule(
   num_vehicule INT AUTO_INCREMENT,
   poid_max DECIMAL(15,2),
   date_achat DATE,
   num_type INT,
   num_marque INT,
   PRIMARY KEY(num_vehicule, num_marque, num_type),
   FOREIGN KEY(num_type) REFERENCES type_vehicule(num_type),
   FOREIGN KEY(num_marque) REFERENCES marque(num_marque)
);

CREATE TABLE usine(
   num_usine INT AUTO_INCREMENT,
   nom_usine VARCHAR(50),
   adresse_usine VARCHAR(50),
   PRIMARY KEY(num_usine)
);

CREATE TABLE produit(
   num_produit INT AUTO_INCREMENT,
   libelle_produit VARCHAR(50),
   PRIMARY KEY(num_produit)
);

CREATE TABLE benne
(
   id_benne INT AUTO_INCREMENT,
   nb_benne INT,
   volume INT,
   num_centre INT,
   num_produit INT,
   PRIMARY KEY(id_benne),
   FOREIGN KEY(num_centre) REFERENCES centre(num_centre),
   FOREIGN KEY(num_produit) REFERENCES produit(num_produit)
);

CREATE TABLE decharge(
   num_vehicule INT,
   num_usine INT,
   num_produit INT,
   JMA DATE,
   quantite VARCHAR(50),
   PRIMARY KEY(num_vehicule, num_usine, num_produit, JMA),
   FOREIGN KEY(num_vehicule) REFERENCES vehicule(num_vehicule),
   FOREIGN KEY(num_usine) REFERENCES usine(num_usine),
   FOREIGN KEY(num_produit) REFERENCES produit(num_produit)
);

CREATE TABLE passe(
   num_centre INT,
   num_vehicule INT,
   JMA DATE,
   ordre INT,
   PRIMARY KEY(num_centre, num_vehicule, JMA),
   FOREIGN KEY(num_centre) REFERENCES centre(num_centre),
   FOREIGN KEY(num_vehicule) REFERENCES vehicule(num_vehicule)
);

/*INSERT des entités*/

INSERT INTO type_vehicule(num_type, libelle_type) VALUES
(NULL, 'fourgon moyen'),
(NULL, 'camion'),
(NULL, 'poids lourd');

INSERT INTO marque(num_marque, libelle_marque) VALUES
(NULL,'Renault'),
(NULL, 'Volkswagen'),
(NULL, 'Ford');


INSERT INTO centre (num_centre, nom_centre, adresse_centre) VALUES
(NULL, '3Dechets','10 rue des poubelles'),
(NULL, 'Dechet2000','25 Avenue des chateaux'),
(NULL, 'FourTout','2 rue sous le pont');

INSERT INTO vehicule (num_vehicule, poid_max, date_achat) VALUES
(NULL, 100, '2022-10-10'),
(NULL, 150, '2023-08-1'),
(NULL, 75, '2024-1-20');

INSERT INTO usine (num_usine, nom_usine, adresse_usine) VALUES
(NULL, 'TriTout', '26 rue des champs'),
(NULL, 'BruleTout', '10 rue de rang'),
(NULL, 'CompactTout', '14 rue des pierres');

INSERT INTO produit (num_produit, libelle_produit) VALUES
(NULL, 'Plastique'),
(NULL, 'Carton'),
(NULL, 'Bois');

/*INSERT des associations*/

INSERT INTO benne (id_benne, nb_benne, volume, num_centre, num_produit) VALUES
(null, 6, 60, 1, 1),
(null, 2, 20, 1, 3),
(null, 4, 40, 2, 2),
(null, 3, 30, 2, 3),
(null, 2, 120, 3, 1),
(null, 1, 100, 3, 2);

INSERT INTO passe (num_centre, num_vehicule, JMA, ordre) VALUES
(1, 1, '2022-10-23', 1),
(3, 1, '2022-10-23', 2),
(2, 1, '2022-10-23', 3),
(3, 2, '2024-11-07', 1),
(1, 2, '2024-11-07', 2),
(1, 1, '2023-1-03', 1),
(2, 1, '2023-1-03', 2);

INSERT INTO decharge (num_vehicule, num_usine, num_produit, JMA, quantite) VALUES
(2, 1, 3, '2024-11-07', '14kg'),
(2, 1, 1, '2024-11-07', '10kg'),
(1, 3, 2, '2023-1-03', '50kg'),
(1, 3, 1, '2022-10-23', '59kg');

/* Affiche tous les centres qui on comme produit le 'Plastique' */
SELECT centre.num_centre, centre.nom_centre, benne.nb_benne, produit.libelle_produit FROM centre
JOIN benne ON centre.num_centre = benne.num_centre
JOIN produit ON produit.num_produit = benne.num_produit
WHERE libelle_produit='Plastique';

/* Affiche la date ou chaque véhicule a fait une tounée */
SELECT DISTINCT vehicule.num_vehicule, passe.JMA FROM vehicule
JOIN passe ON vehicule.num_vehicule = passe.num_vehicule;

/* Affiche l ordre des centres dans lesquels un véhicule est allé lors de ça tournée ainsi que la date */
SELECT vehicule.num_vehicule, passe.JMA, passe.ordre, centre.nom_centre FROM vehicule
JOIN passe ON vehicule.num_vehicule = passe.num_vehicule
JOIN centre ON passe.num_centre = centre.num_centre
ORDER BY passe.num_vehicule, passe.JMA, passe.ordre;

/* Affiche le nombre de produit qu a déchargé un véhicule dans une usine a chaque tournée */
SELECT decharge.JMA, vehicule.num_vehicule, usine.nom_usine, COUNT(decharge.num_produit) AS nombre_type_produit_decharge FROM usine
JOIN decharge ON usine.num_usine = decharge.num_usine
JOIN vehicule ON decharge.num_vehicule = vehicule.num_vehicule
GROUP BY decharge.JMA, decharge.num_vehicule, usine.nom_usine
ORDER BY decharge.JMA;
