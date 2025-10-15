-- Постачальники
INSERT INTO lieferanten (lieferant_id, name, kontaktperson, telefon, email) VALUES
(1,'FruchtHof GmbH','Peter Kern','0660-100100','frucht@hof.at'),
(2,'DairyCo','Sabine Milch','0660-200200','office@dairyco.at'),
(3,'Bäckerei Groß','Anna Brot','0660-300300','bestellung@baeckerei.at'),
(4,'GetränkePartner','Roman Saft','0660-400400','sale@getraenkepartner.at'),
(5,'Süßwaren Import','Marta Kakao','0660-500500','choco@suesswaren.at');

--  Клієнти (20 шт)
INSERT INTO kunden (kunden_id, vorname, nachname, email, telefon) VALUES
(1,'Anna','Müller','anna1@example.com','0660111111'),
(2,'Lukas','Schmidt','lukas@example.com','0660222222'),
(3,'Mia','Lehner','mia@example.com','0660333333'),
(4,'Felix','Bauer','felix@example.com','0660444444'),
(5,'Lea','Hofer','lea@example.com','0660555555'),
(6,'Paul','Wagner','paul@example.com','0660666666'),
(7,'Sofia','Haas','sofia@example.com','0660777777'),
(8,'Jonas','Fischer','jonas@example.com','0660888888'),
(9,'Emilia','Moser','emilia@example.com','0660999999'),
(10,'Max','Weber','max@example.com','0660123456'),
(11,'Clara','Klein','clara@example.com','0660123457'),
(12,'Tom','Winter','tom@example.com','0660123458'),
(13,'Nina','Lang','nina@example.com','0660123459'),
(14,'Ben','Kaiser','ben@example.com','0660123460'),
(15,'Lena','Auer','lena@example.com','0660123461'),
(16,'Erik','Gruber','erik@example.com','0660123462'),
(17,'Sarah','Pichler','sarah@example.com','0660123463'),
(18,'Jan','Huber','jan@example.com','0660123464'),
(19,'Mara','Egger','mara@example.com','0660123465'),
(20,'Leo','Wallner','leo@example.com','0660123466');

-- Товари (роздрібна ціна «verkaufspreis» на сьогодні; 
--   закупочні ціни будуть в einkauf_artikel.einkaufspreis)
INSERT INTO artikel (artikel_id, name, preis, lagerbestand, lieferant_id) VALUES
(1,'Apfel',0.99,0,1),
(2,'Banane',1.10,0,1),
(3,'Brot',2.50,0,3),
(4,'Milch 1L',1.30,0,2),
(5,'Käse 200g',3.90,0,2),
(6,'Kaffee 500g',7.50,0,5),
(7,'Tee 100g',3.20,0,5),
(8,'Zucker 1kg',1.20,0,4),
(9,'Mehl 1kg',1.00,0,3),
(10,'Saft 1L',2.20,0,4),
(11,'Schokolade 100g',2.80,0,5),
(12,'Eier 10St',2.40,0,2);

-- Закупки (шапки) – старт 2025-09-01 і далі
INSERT INTO einkauf (einkauf_id, lieferant_id, datum, rechnung_nr, bemerkung) VALUES
(1,1,'2025-09-01 10:00:00','R-2025-001','Erstbelieferung Obst'),
(2,2,'2025-09-10 09:30:00','R-2025-002','Milchprodukte'),
(3,3,'2025-09-20 08:45:00','R-2025-003','Backwaren & Mehl'),
(4,4,'2025-10-05 11:10:00','R-2025-004','Getränke & Zucker'),
(5,5,'2025-10-12 13:20:00','R-2025-005','Kaffee/Tee/Schoko');

-- Позиції закупок (менеджимо маржу ~10–50%: продажна ціна в artikel.preis вища за einkaufspreis)
INSERT INTO einkauf_artikel (einkauf_id, artikel_id, menge, einkaufspreis) VALUES
-- EK#1 (FruchtHof)
(1,1,150,0.65),   -- Apfel
(1,2,150,0.75),   -- Banane
-- EK#2 (DairyCo)
(2,4,200,0.95),   -- Milch
(2,5,120,2.80),   -- Käse
(2,12,120,1.60),  -- Eier
-- EK#3 (Bäckerei Groß)
(3,3,180,1.80),   -- Brot
(3,9,200,0.70),   -- Mehl
-- EK#4 (GetränkePartner)
(4,8,220,0.80),   -- Zucker
(4,10,180,1.60),  -- Saft
-- EK#5 (Süßwaren Import)
(5,6,120,5.40),   -- Kaffee
(5,7,150,2.30),   -- Tee
(5,11,160,2.00);  -- Schokolade

-- Продажі (шапки) вересень–жовтень (20 шт, по 1–3 позиції кожен)
INSERT INTO verkauf (verkauf_id, kunden_id, datum) VALUES
(1,  1,'2025-09-05 12:10:00'),
(2,  3,'2025-09-06 15:45:00'),
(3,  5,'2025-09-08 10:20:00'),
(4,  2,'2025-09-10 17:05:00'),
(5,  7,'2025-09-12 09:40:00'),
(6,  9,'2025-09-15 13:15:00'),
(7, 11,'2025-09-18 18:25:00'),
(8,  6,'2025-09-20 11:55:00'),
(9,  4,'2025-09-23 16:10:00'),
(10, 8,'2025-09-25 14:05:00'),
(11,12,'2025-09-28 12:35:00'),
(12,14,'2025-10-01 10:00:00'),
(13,15,'2025-10-03 12:22:00'),
(14,16,'2025-10-05 16:45:00'),
(15,18,'2025-10-07 09:18:00'),
(16,19,'2025-10-09 19:02:00'),
(17,20,'2025-10-11 11:11:00'),
(18,10,'2025-10-12 15:33:00'),
(19,13,'2025-10-13 17:47:00'),
(20, 2,'2025-10-14 10:29:00');

-- Позиції продажів (менші кількості; усім товарам достатньо закупок, щоб не піти в мінус)
INSERT INTO verkauf_artikel (verkauf_id, artikel_id, menge) VALUES
(1, 1,3),(1, 3,1),
(2, 2,2),(2, 4,2),
(3, 5,1),(3, 1,2),
(4, 3,2),(4, 9,1),
(5, 4,2),(5, 8,2),
(6, 10,2),(6, 11,1),
(7, 6,1),(7, 7,1),(7, 5,1),
(8, 2,3),
(9, 1,2),(9, 12,1),
(10,3,1),(10,10,2),
(11,11,2),
(12,4,2),(12,8,1),
(13,6,1),(13,7,2),
(14,5,1),(14,1,2),
(15,2,2),(15,3,1),
(16,10,2),(16,8,2),
(17,11,2),(17,6,1),
(18,12,2),(18,9,2),
(19,7,1),(19,5,1),
(20,1,2),(20,3,1);

 -- Перерахунок залишків у artikel.lagerbestand
UPDATE artikel a
LEFT JOIN (
  SELECT artikel_id, SUM(menge) AS gekaufte
  FROM einkauf_artikel
  GROUP BY artikel_id
) ek ON ek.artikel_id = a.artikel_id
LEFT JOIN (
  SELECT artikel_id, SUM(menge) AS verkaufte
  FROM verkauf_artikel
  GROUP BY artikel_id
) vk ON vk.artikel_id = a.artikel_id
SET a.lagerbestand = COALESCE(ek.gekaufte,0) - COALESCE(vk.verkaufte,0);


SELECT @@SQL_SAFE_UPDATES;