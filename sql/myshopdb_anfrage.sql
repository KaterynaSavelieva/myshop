USE myshopdb;
SELECT * FROM lieferanten;
SELECT * FROM kunden;
SELECT * FROM artikel;
SELECT * FROM verkauf;
SELECT * FROM verkauf_artikel;
SELECT * FROM einkauf;
SELECT * FROM einkauf_artikel;

SELECT artikel_id, name, lagerbestand FROM artikel ORDER BY artikel_id;