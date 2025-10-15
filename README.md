Projektbeschreibung – Systemarchitektur

In diesem Projekt dient der Raspberry Pi als kleiner Datenserver mit einer installierten MariaDB-Datenbank.  
Alle Verkaufsdaten (z. B. Kunden, Artikel, Verkäufe) werden auf dem Raspberry Pi gespeichert und verwaltet.  
Der Python-Code wird auf meinem Laptop in PyCharm geschrieben und ausgeführt.  
Über die IP-Adresse des Raspberry Pi (z. B. 192.168.31.237) verbindet sich das Python-Programm automatisch mit der Datenbank auf dem Raspberry Pi.  
Dadurch werden neue Datensätze eingefügt, Abfragen durchgeführt und Analysen berechnet, während die eigentliche Datenhaltung auf dem Raspberry Pi erfolgt.  
Der Quellcode wird zusätzlich auf GitHub gespeichert, um die Projektentwicklung zu dokumentieren.


💻 Systemübersicht - Das folgende Diagramm zeigt die Architektur meines Projekts:


        💻 Laptop (Python / PyCharm)
              • Entwickelt und führt Python-Skripte aus
              • Verbindet sich über IP 192.168.31.237
                │
                ▼
        
        🌐 Netzwerk (192.168.31.237)
                │
                ▼
        
        🍓 Raspberry Pi (MariaDB-Server)
              • Speichert und verwaltet Verkaufsdaten 
              • Tabellen: kunden, artikel, verkauf ... 
                │
                ▼
        
        📊 Datenauswertung und Analyse
              • Python-Skripte führen SQL-Abfragen aus
              • Ergebnisse werden lokal angezeigt


Der Python-Code läuft auf dem Laptop, während die MariaDB-Datenbank auf dem Raspberry Pi installiert ist.  
Über die Netzwerkverbindung werden Daten in die Datenbank eingefügt und später für Analysen abgerufen.  
Die Projektdateien werden zusätzlich auf GitHub gespeichert.


⚙️ Technische Umgebung
| Komponente                   | Beschreibung                                                      	                                          
| -----------------------------|----------------------------------------------------------------------------------------------
| 💻 **Entwicklungsumgebung** | PyCharm Community Edition (Windows 11) 
| 🍓 **Server**               | Raspberry Pi  mit Raspberry Pi OS (64-bit) 
| 🗄️ **Datenbank**            | MariaDB 11.3 (läuft auf Raspberry Pi) 
| 💬 **SQL-Sprache**          | Erstellung von Tabellen, Datenabfragen und Analysen mit SQL |
| 🐍 **Programmiersprache**   | Python 3.11 mit `mysql-connector-python` und `python-dotenv` 
| 🌐 **Netzwerk**             | Verbindung über IP-Adresse 192.168.31.237 |
| ☁️ **Versionsverwaltung**   | Git & GitHub Repository: [KaterynaSavelieva/myshop](https://github.com/KaterynaSavelieva/myshop)  

Diese Umgebung ermöglicht eine klare Trennung zwischen Datenhaltung (Raspberry Pi) und Datenanalyse (Laptop mit Python und SQL-Abfragen).

