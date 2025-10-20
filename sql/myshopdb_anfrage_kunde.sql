USE myshopdb;

(SELECT
	kunden.kunden_id,
    CONCAT (kunden.nachname, ' ', kunden.vorname) AS Kunde,
    verkauf.verkauf_id,
	verkauf_artikel.menge,
    verkauf_artikel.verkaufspreis,
    verkauf_artikel.rabatt_pct,
    ROUND((verkauf_artikel.verkaufspreis*(1-IFNULL(verkauf_artikel.rabatt_pct,0)/100)), 2)*menge AS summe,
    verkauf.datum,
    artikel.name
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
	SUM(verkauf_artikel.menge) AS menge,
    NULL AS verkaufspreis,
    NULL AS rabatt_pct,
    ROUND(SUM(verkauf_artikel.verkaufspreis*(1-IFNULL(verkauf_artikel.rabatt_pct,0)/100)), 2)*menge AS summe,
    NULL AS datum,
    NULL AS name
FROM kunden
JOIN verkauf ON verkauf.kunden_id=kunden.kunden_id
JOIN verkauf_artikel ON verkauf_artikel.verkauf_id=verkauf.verkauf_id
JOIN artikel ON artikel.artikel_id=verkauf_artikel.artikel_id
WHERE kunden.kunden_id=11)


