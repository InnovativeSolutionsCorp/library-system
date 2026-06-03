SET NOCOUNT ON;

INSERT INTO dbo.Players (FirstName, LastName, Country, DOB, Ranking)
VALUES
('Roger','Federer','SUI','1981-08-08',1),
('Rafael','Nadal','ESP','1986-06-03',2),
('Novak','Djokovic','SRB','1987-05-22',3),
('Serena','Williams','USA','1981-09-26',4),
('Naomi','Osaka','JPN','1997-10-16',5),
('Carlos','Alcaraz','ESP','2003-05-05',6);

-- Insert sample matches (using identity PlayerId starting at 1)
INSERT INTO dbo.Matches (Player1Id, Player2Id, WinnerId, Score, Tournament, MatchDate, DurationMinutes, Surface)
VALUES
(1,2,1,'6-4,6-4','Wimbledon', '2023-07-10', 120, 'Grass'),
(1,3,3,'4-6,7-5,6-3','Australian Open','2024-01-20',180,'Hard'),
(2,3,2,'7-6,6-7,7-5','Roland Garros','2023-06-05',150,'Clay'),
(4,5,4,'6-3,6-4','US Open','2022-09-10',95,'Hard'),
(5,6,6,'6-2,3-6,7-6','Miami Open','2024-03-25',145,'Hard'),
(3,1,3,'6-1,6-2','Queen''s Club','2022-06-18',85,'Grass'),
(6,2,6,'6-4,6-4','Madrid Open','2024-05-02',110,'Clay'),
(1,6,1,'6-4,6-7,7-6','US Open','2024-09-01',200,'Hard');
