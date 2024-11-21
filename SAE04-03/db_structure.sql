DROP TABLE IF EXISTS db_usine.passe;
DROP TABLE IF EXISTS db_usine.decharge;
DROP TABLE IF EXISTS db_usine.contient;
DROP TABLE IF EXISTS db_usine.produit;
DROP TABLE IF EXISTS db_usine.usine;
DROP TABLE IF EXISTS db_usine.vehicule;
DROP TABLE IF EXISTS db_usine.centre;

CREATE TABLE db_usine.centre(
   num_centre INT AUTO_INCREMENT,
   nom_centre VARCHAR(50),
   adresse_centre VARCHAR(50),
   PRIMARY KEY(num_centre)
);

CREATE TABLE db_usine.vehicule(
   num_vehicule INT AUTO_INCREMENT,
   poid_max DECIMAL(15,2),
   date_achat DATE,
   PRIMARY KEY(num_vehicule)
);

CREATE TABLE db_usine.usine(
   num_usine INT AUTO_INCREMENT,
   nom_usine VARCHAR(50),
   adresse_usine VARCHAR(50),
   PRIMARY KEY(num_usine)
);

CREATE TABLE db_usine.produit(
   num_produit INT AUTO_INCREMENT,
   libelle_produit VARCHAR(50),
   PRIMARY KEY(num_produit)
);

CREATE TABLE db_usine.contient(
   num_centre INT,
   num_produit INT,
   nb_benne INT,
   PRIMARY KEY(num_centre, num_produit),
   FOREIGN KEY(num_centre) REFERENCES centre(num_centre),
   FOREIGN KEY(num_produit) REFERENCES produit(num_produit)
);

CREATE TABLE db_usine.decharge(
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

CREATE TABLE db_usine.passe(
   num_centre INT,
   num_vehicule INT,
   JMA DATE,
   ordre INT,
   PRIMARY KEY(num_centre, num_vehicule, JMA),
   FOREIGN KEY(num_centre) REFERENCES centre(num_centre),
   FOREIGN KEY(num_vehicule) REFERENCES vehicule(num_vehicule)
);
