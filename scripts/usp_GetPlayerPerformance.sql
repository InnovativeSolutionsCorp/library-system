IF OBJECT_ID('dbo.usp_GetPlayerPerformance','P') IS NOT NULL
  DROP PROCEDURE dbo.usp_GetPlayerPerformance;
GO

CREATE PROCEDURE dbo.usp_GetPlayerPerformance
 @PlayerId INT,
 @StartDate DATETIME2 = NULL,
 @EndDate DATETIME2 = NULL,
 @Surface NVARCHAR(50) = NULL,
 @TopOpponents INT = 5
AS
BEGIN
 SET NOCOUNT ON;
 BEGIN TRY
  CREATE TABLE #MatchesFiltered (
   MatchId int, Player1Id int, Player2Id int, WinnerId int, Score nvarchar(50),
   Tournament nvarchar(200), MatchDate datetime2, DurationMinutes int, Surface nvarchar(50),
   Player1Name nvarchar(201), Player2Name nvarchar(201)
  );

  DECLARE @sql nvarchar(max) = N'
   SELECT m.MatchId,m.Player1Id,m.Player2Id,m.WinnerId,m.Score,m.Tournament,m.MatchDate,m.DurationMinutes,m.Surface,
   p1.FirstName + '' '' + p1.LastName AS Player1Name,
   p2.FirstName + '' '' + p2.LastName AS Player2Name
   FROM dbo.Matches m
   JOIN dbo.Players p1 ON p1.PlayerId = m.Player1Id
   JOIN dbo.Players p2 ON p2.PlayerId = m.Player2Id
   WHERE (m.Player1Id = @PlayerId OR m.Player2Id = @PlayerId)
  ';

  IF @StartDate IS NOT NULL SET @sql += ' AND m.MatchDate >= @StartDate';
  IF @EndDate IS NOT NULL SET @sql += ' AND m.MatchDate <= @EndDate';
  IF @Surface IS NOT NULL SET @sql += ' AND m.Surface = @Surface';

  DECLARE @params nvarchar(500) = N'@PlayerId int,@StartDate datetime2,@EndDate datetime2,@Surface nvarchar(50)';

  INSERT INTO #MatchesFiltered
  EXEC sp_executesql @sql,@params,@PlayerId=@PlayerId,@StartDate=@StartDate,@EndDate=@EndDate,@Surface=@Surface;

  -- Summary metrics
  SELECT COUNT(*) AS TotalMatches,
    SUM(CASE WHEN WinnerId = @PlayerId THEN 1 ELSE 0 END) AS Wins,
    SUM(CASE WHEN WinnerId IS NOT NULL AND WinnerId <> @PlayerId THEN 1 ELSE 0 END) AS Losses,
    CASE WHEN COUNT(*)=0 THEN 0 ELSE 1.0 * SUM(CASE WHEN WinnerId = @PlayerId THEN 1 ELSE 0 END)/COUNT(*) END AS WinPercentage,
    AVG(DurationMinutes) AS AvgDuration
  FROM #MatchesFiltered;

  -- Recent matches (top 10)
  SELECT TOP 10 *
  FROM #MatchesFiltered
  ORDER BY MatchDate DESC;

  -- Performance by surface
  SELECT Surface,
    COUNT(*) AS Matches,
    SUM(CASE WHEN WinnerId = @PlayerId THEN 1 ELSE 0 END) AS Wins,
    1.0 * SUM(CASE WHEN WinnerId = @PlayerId THEN 1 ELSE 0 END)/COUNT(*) AS WinPct
  FROM #MatchesFiltered
  GROUP BY Surface
  ORDER BY Matches DESC;

  -- Top opponents head-to-head
  ;WITH Opps AS (
   SELECT CASE WHEN Player1Id = @PlayerId THEN Player2Id ELSE Player1Id END AS OpponentId,
     COUNT(*) AS Matches, SUM(CASE WHEN WinnerId = @PlayerId THEN 1 ELSE 0 END) AS Wins
   FROM #MatchesFiltered
   GROUP BY CASE WHEN Player1Id = @PlayerId THEN Player2Id ELSE Player1Id END
  )
  SELECT TOP (@TopOpponents) o.OpponentId, p.FirstName + ' ' + p.LastName as OpponentName, o.Matches, o.Wins,
    1.0*o.Wins/o.Matches AS WinPct
  FROM Opps o JOIN dbo.Players p ON p.PlayerId = o.OpponentId
  ORDER BY o.Matches DESC, o.Wins DESC;

  DROP TABLE #MatchesFiltered;
 END TRY
 BEGIN CATCH
  SELECT ERROR_NUMBER() AS ErrorNumber, ERROR_MESSAGE() AS ErrorMessage;
 END CATCH
END
