USE myshopdb;
-- шапки
CREATE INDEX IF NOT EXISTS idx_verkauf_kunde     ON verkauf(kunden_id);
CREATE INDEX IF NOT EXISTS idx_einkauf_lieferant ON einkauf(lieferant_id);

-- позиції продажу
CREATE INDEX IF NOT EXISTS idx_va_verkauf ON verkauf_artikel(verkauf_id);
CREATE INDEX IF NOT EXISTS idx_va_artikel ON verkauf_artikel(artikel_id);

-- позиції закупки
CREATE INDEX IF NOT EXISTS idx_ea_einkauf ON einkauf_artikel(einkauf_id);
CREATE INDEX IF NOT EXISTS idx_ea_artikel ON einkauf_artikel(artikel_id);

-- зв’язок товар—постачальник
CREATE INDEX IF NOT EXISTS idx_al_artikel ON artikel_lieferant(artikel_id);