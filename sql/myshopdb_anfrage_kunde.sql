USE myshopdb;

(SELECT
	kunden.kunden_id,
    CONCAT (kunden.nachname, ' ', kunden.vorname) AS Kunde,
    verkauf.verkauf_id,
    artikel.name,
	verkauf_artikel.verkauf_menge,
    verkauf_artikel.verkaufspreis,
    verkauf_artikel.rabatt_pct,
    ROUND((verkauf_artikel.verkaufspreis*(1-IFNULL(verkauf_artikel.rabatt_pct,0)/100)), 2)*verkauf_menge AS summe,
    verkauf.verkauf_datum
FROM kunden
JOIN verkauf ON verkauf.kunden_id=kunden.kunden_id
JOIN verkauf_artikel ON verkauf_artikel.verkauf_id=verkauf.verkauf_id
JOIN artikel ON artikel.artikel_id=verkauf_artikel.artikel_id
WHERE kunden.kunden_id=11)
UNION ALL
(SELECT
	NULL AS kunden_id,
    'TOTAL:' AS Kunde,
    NULL AS verkauf_id,
    NULL AS name,
	SUM(verkauf_artikel.verkauf_menge) AS verkauf_menge,
    NULL AS verkaufspreis,
    NULL AS rabatt_pct,
    ROUND(SUM(verkauf_artikel.verkaufspreis*(1-IFNULL(verkauf_artikel.rabatt_pct,0)/100)), 2)*verkauf_menge AS summe,
    NULL AS datum
FROM kunden
JOIN verkauf ON verkauf.kunden_id=kunden.kunden_id
JOIN verkauf_artikel ON verkauf_artikel.verkauf_id=verkauf.verkauf_id
JOIN artikel ON artikel.artikel_id=verkauf_artikel.artikel_id
WHERE kunden.kunden_id=11)


