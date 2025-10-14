-- Create database
CREATE DATABASE IF NOT EXISTS myshopdb;
DROP TABLE IF EXISTS verkauf_artikel;
DROP TABLE IF EXISTS lieferanten ;

DROP TABLE IF EXISTS verkauf;
DROP TABLE IF EXISTS artikel;
DROP TABLE IF EXISTS kunden;
USE myshopdb;

-- 1️⃣ Tabelle: kunden (покупці)
CREATE TABLE IF NOT EXISTS kunden (
    kunden_id INT AUTO_INCREMENT PRIMARY KEY,
    vorname VARCHAR(50) NOT NULL,
    nachname VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    telefon VARCHAR(20)
);

-- 2️⃣ Tabelle: lieferanten (постачальники)
CREATE TABLE IF NOT EXISTS lieferanten (
    lieferant_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    kontaktperson VARCHAR(100),
    telefon VARCHAR(20),
    email VARCHAR(100)
);

-- 3️⃣ Tabelle: artikel (товари)
CREATE TABLE IF NOT EXISTS artikel (
    artikel_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    preis DECIMAL(10,2) NOT NULL,
    lagerbestand INT DEFAULT 0,
    lieferant_id INT,
    FOREIGN KEY (lieferant_id) REFERENCES lieferanten(lieferant_id)
);

-- 4️⃣ Tabelle: verkauf (продаж)
CREATE TABLE IF NOT EXISTS verkauf (
    verkauf_id INT AUTO_INCREMENT PRIMARY KEY,
    kunden_id INT,
    datum DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kunden_id) REFERENCES kunden(kunden_id)
);

-- 5️⃣ Tabelle: verkauf_artikel (зв’язок продажів і товарів)
CREATE TABLE IF NOT EXISTS verkauf_artikel (
    verkauf_id INT,
    artikel_id INT,
    menge INT DEFAULT 1,
    PRIMARY KEY (verkauf_id, artikel_id),
    FOREIGN KEY (verkauf_id) REFERENCES verkauf(verkauf_id),
    FOREIGN KEY (artikel_id) REFERENCES artikel(artikel_id)
);