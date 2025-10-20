USE myshopdb;

CREATE USER 'dashboard'@'%' IDENTIFIED BY 'StrongReadOnlyPass!';
GRANT SELECT ON myshopdb.* TO 'dashboard'@'%';
FLUSH PRIVILEGES;
