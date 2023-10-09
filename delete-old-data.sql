DELETE from measurement where id not in (
SELECT "id" FROM (
    SELECT "id",
           ROW_NUMBER() OVER (PARTITION BY "nodeId" ORDER BY timestamp DESC) AS row_num
    FROM measurement
) ranked
WHERE row_num <= 20000);
