USE myshopdb;

DROP TABLE IF EXISTS verkauf_artikel;
DROP TABLE IF EXISTS einkauf_artikel;
DROP TABLE IF EXISTS artikel_lieferant;
DROP TABLE IF EXISTS verkauf;
DROP TABLE IF EXISTS einkauf;
DROP TABLE IF EXISTS artikel;
DROP TABLE IF EXISTS kunden;
DROP TABLE IF EXISTS lieferanten;

CREATE TABLE kunden (
    kunden_id INT AUTO_INCREMENT PRIMARY KEY,
    vorname VARCHAR(50) NOT NULL,
    nachname VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,  
    telefon VARCHAR(20)
);

CREATE TABLE lieferanten (
    lieferant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    kontaktperson VARCHAR(100),
    telefon VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE artikel (
    artikel_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    preis DECIMAL(10,2) NOT NULL,  -- роздрібна ціна
    lagerbestand INT DEFAULT 0
);

CREATE TABLE artikel_lieferant (
    lieferant_id INT NOT NULL,
    artikel_id INT NOT NULL,
    einkaufspreis DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (lieferant_id, artikel_id),
    FOREIGN KEY (lieferant_id) REFERENCES lieferanten(lieferant_id),
    FOREIGN KEY (artikel_id) REFERENCES artikel(artikel_id)
);

CREATE TABLE einkauf (
    einkauf_id INT AUTO_INCREMENT PRIMARY KEY,
    lieferant_id INT NOT NULL,
    datum DATETIME DEFAULT CURRENT_TIMESTAMP,
    rechnung_nr VARCHAR(50),
    bemerkung VARCHAR(255),
    FOREIGN KEY (lieferant_id) REFERENCES lieferanten(lieferant_id)
);

CREATE TABLE einkauf_artikel (
    einkauf_artikel_id INT AUTO_INCREMENT PRIMARY KEY,
    einkauf_id INT NOT NULL,
    artikel_id INT NOT NULL,
    menge INT CHECK (menge > 0),
    einkaufspreis DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (einkauf_id) REFERENCES einkauf(einkauf_id),
    FOREIGN KEY (artikel_id) REFERENCES artikel(artikel_id)
);

CREATE TABLE verkauf (
    verkauf_id INT AUTO_INCREMENT PRIMARY KEY,
    kunden_id INT NOT NULL,
    datum DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kunden_id) REFERENCES kunden(kunden_id)
);

CREATE TABLE verkauf_artikel (
    verkauf_artikel_id INT AUTO_INCREMENT PRIMARY KEY,
    verkauf_id INT NOT NULL,
    artikel_id INT NOT NULL,
    menge INT CHECK (menge > 0),
    verkaufspreis DECIMAL(10,2) NOT NULL,
    rabatt_pct DECIMAL(5,2) NOT NULL DEFAULT 0,
    FOREIGN KEY (verkauf_id) REFERENCES verkauf(verkauf_id),
    FOREIGN KEY (artikel_id) REFERENCES artikel(artikel_id)
);

ALTER TABLE verkauf_artikel CHANGE menge verkauf_menge INT CHECK (verkauf_menge > 0);
ALTER TABLE einkauf_artikel CHANGE menge einkauf_menge INT CHECK (einkauf_menge > 0);
ALTER TABLE einkauf CHANGE datum einkauf_datum  DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE verkauf CHANGE datum verkauf_datum  DATETIME DEFAULT CURRENT_TIMESTAMP;