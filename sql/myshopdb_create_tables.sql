CREATE DATABASE IF NOT EXISTS myshopdb;
DROP TABLE IF EXISTS verkauf_artikel;
DROP TABLE IF EXISTS verkauf;
DROP TABLE IF EXISTS artikel;
DROP TABLE IF EXISTS kunden;
DROP TABLE IF EXISTS lieferanten ;
USE myshopdb;

CREATE TABLE IF NOT EXISTS kunden (
    kunden_id INT AUTO_INCREMENT PRIMARY KEY,
    vorname VARCHAR(50) NOT NULL,
    nachname VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    telefon VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS lieferanten (
    lieferant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    kontaktperson VARCHAR(100),
    telefon VARCHAR(20),
    email VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS artikel (
    artikel_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    preis DECIMAL(10,2) NOT NULL,
    lagerbestand INT DEFAULT 0,
    lieferant_id INT,
    FOREIGN KEY (lieferant_id) REFERENCES lieferanten(lieferant_id)
);

CREATE TABLE IF NOT EXISTS verkauf (
    verkauf_id INT AUTO_INCREMENT PRIMARY KEY,
    kunden_id INT,
    datum DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kunden_id) REFERENCES kunden(kunden_id)
);

CREATE TABLE IF NOT EXISTS verkauf_artikel (
    verkauf_id INT,
    artikel_id INT,
    menge INT DEFAULT 1,
    PRIMARY KEY (verkauf_id, artikel_id),
    FOREIGN KEY (verkauf_id) REFERENCES verkauf(verkauf_id),
    FOREIGN KEY (artikel_id) REFERENCES artikel(artikel_id)
);

CREATE TABLE IF NOT EXISTS einkauf (
  einkauf_id   INT AUTO_INCREMENT PRIMARY KEY,
  lieferant_id INT NOT NULL,
  datum        DATETIME DEFAULT CURRENT_TIMESTAMP,
  rechnung_nr  VARCHAR(50),
  bemerkung    VARCHAR(255),
  FOREIGN KEY (lieferant_id) REFERENCES lieferanten(lieferant_id)
);

-- позиції закупки (БАГАТО товарів на одну закупку)
CREATE TABLE IF NOT EXISTS einkauf_artikel (
  einkauf_id    INT NOT NULL,
  artikel_id    INT NOT NULL,
  menge         INT NOT NULL CHECK (menge > 0),
  einkaufspreis DECIMAL(10,2) NOT NULL,   -- ціна закупки за одиницю на дату закупки
  PRIMARY KEY (einkauf_id, artikel_id),
  FOREIGN KEY (einkauf_id) REFERENCES einkauf(einkauf_id),
  FOREIGN KEY (artikel_id) REFERENCES artikel(artikel_id)
);

CREATE INDEX IF NOT EXISTS idx_ea_artikel ON einkauf_artikel(artikel_id);
CREATE INDEX IF NOT EXISTS idx_e_datum   ON einkauf(datum);