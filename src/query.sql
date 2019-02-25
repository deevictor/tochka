DROP TABLE IF EXISTS #GroupDeltas;
GO

DECLARE @Threshold DECIMAL(5,2) = 19.2,
        @MaxGroupSize INT = (SELECT COUNT(*) FROM FOO),
        @GroupSize INT = 2, -- Initial Group Size
        @SQL VARCHAR(1000);

CREATE TABLE #GroupDeltas
    (
        StartID INT,
        GroupSize INT,
        GroupDelta DECIMAL(9,2),
        PRIMARY KEY (StartID, GroupSize)
    );

WHILE @GroupSize <= @MaxGroupSize
BEGIN
    SET @SQL = '
                ;WITH DeltasFromNext
                AS
                    (
                        SELECT  ID,
                                LEAD(Value) OVER(ORDER BY ID ASC) - Value AS Delta
                        FROM    FOO
                    )
                    SELECT  ID,
                            ' + CAST(@GroupSize AS VARCHAR(5)) +',
                            SUM(Delta)
                            OVER (  ORDER BY ID
                                    ROWS BETWEEN
                                    CURRENT ROW AND
                                    ' + CAST(@GroupSize - 2 AS VARCHAR(5))
                                    + ' FOLLOWING)
                    FROM DeltasFromNext;
    '
    INSERT INTO #GroupDeltas
    EXECUTE (@SQL);
    IF EXISTS   (
                    SELECT  NULL
                    FROM    #GroupDeltas
                    WHERE   ABS(GroupDelta) >= @Threshold
                )
    BREAK;
    SET @GroupSize += 1
END
SELECT  *
FROM    #GroupDeltas
WHERE   ABS(GroupDelta) >= @Threshold
ORDER BY GroupSize, StartID;