/*INSERT des entités*/

INSERT INTO db_usine.centre (num_centre, nom_centre, adresse_centre) VALUES
(NULL, '3Dechets','10 rue des poubelles'),
(NULL, 'Dechet2000','25 Avenue des chateaux'),
(NULL, 'FourTout','2 rue sous le pont');

INSERT INTO db_usine.vehicule (num_vehicule, poid_max, date_achat) VALUES
(NULL, 100, '2022-10-10'),
(NULL, 150, '2023-08-1'),
(NULL, 75, '2024-1-20');

INSERT INTO db_usine.usine (num_usine, nom_usine, adresse_usine) VALUES
(NULL, 'TriTout', '26 rue des champs'),
(NULL, 'BruleTout', '10 rue de rang'),
(NULL, 'CompactTout', '14 rue des pierres');

INSERT INTO db_usine.produit (num_produit, libelle_produit) VALUES
(NULL, 'Plastique'),
(NULL, 'Carton'),
(NULL, 'Bois');

/*INSERT des associations*/

INSERT INTO db_usine.contient (num_centre, num_produit, nb_benne) VALUES
(1, 1, 6),
(1, 3, 2),
(2, 2, 4),
(2, 3, 3),
(3, 1, 2),
(3, 2, 1);

INSERT INTO db_usine.passe (num_centre, num_vehicule, JMA, ordre) VALUES
(1, 1, '2022-10-23', 1),
(3, 1, '2022-10-23', 2),
(2, 1, '2022-10-23', 3),
(3, 2, '2024-11-07', 1),
(1, 2, '2024-11-07', 2),
(1, 1, '2023-1-03', 1),
(2, 1, '2023-1-03', 2);

INSERT INTO db_usine.decharge (num_vehicule, num_usine, num_produit, JMA, quantite) VALUES
(2, 1, 3, '2024-11-07', '14kg'),
(2, 1, 1, '2024-11-07', '10kg'),
(1, 3, 2, '2023-1-03', '50kg'),
(1, 3, 1, '2022-10-23', '59kg');