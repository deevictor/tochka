  DROP TABLE IF EXISTS SetDeltas;
  CREATE TEMP TABLE SetDeltas(
    StartID INTEGER,
    SetSize INTEGER,
    SetDelta NUMERIC(5, 2),
    PRIMARY KEY (StartID, SetSize)
  );
DO $$
  DECLARE
    threshold NUMERIC(5, 2) := {threshold};
    max_set_size INTEGER := (SELECT COUNT(*) FROM trades_stockprice WHERE company_id={company_id});
    set_size INTEGER := 1; --initial set size

  BEGIN
    LOOP
    EXIT WHEN EXISTS (
      SELECT *
      FROM SetDeltas
      WHERE ABS(SetDelta) >= threshold
      ) OR set_size = max_set_size;
      WITH Deltas AS (
        SELECT id,
          {val_type} - LEAD({val_type}) OVER (ORDER BY id) AS delta
        FROM trades_stockprice
        WHERE company_id = 1
      )
      INSERT INTO SetDeltas
        SELECT id,
               set_size,
               SUM(delta) OVER (
                 ORDER BY id
                 RANGE BETWEEN CURRENT ROW AND set_size-1 FOLLOWING
                 )
        FROM Deltas;
    set_size := set_size+1;
    END LOOP;
  END
$$;
SELECT *
FROM SetDeltas
WHERE ABS(setdelta) >= {threshold};
