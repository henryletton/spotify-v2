
/*Artists in refresh order
Only those we have listened to*/
CREATE VIEW Music_Refresh_Artist AS
SELECT x.*
FROM (
    SELECT 
    	a.Artist_Id, b.*, c.Artist_Name, c.Artist_Popularity, c.Total_Followers, c.TimeStamp,
    	ROW_NUMBER() OVER(PARTITION BY c.Artist_Id ORDER BY b.Track_Id) as row_num
    FROM Music_Artist_Track_Mapping as a
    LEFT JOIN Music_Track_Listens as b
    ON a.Track_Id = b.Track_Id
    LEFT JOIN Music_Artists as c
    ON a.Artist_Id = c.Artist_Id
    WHERE b.Track_Id IS NOT NULL
		AND a.Artist_Id IS NOT NULL
    ORDER BY isnull(c.Artist_Id) DESC,
		isnull(c.Artist_Name) DESC,
		isnull(c.Artist_Popularity) DESC,
		isnull(c.Total_Followers) DESC,
		c.TimeStamp
) as x
WHERE x.row_num = 1
LIMIT 100

/*Albums in refresh order*/
CREATE VIEW Music_Refresh_Album AS
SELECT *
FROM Music_Albums
ORDER BY isnull(Album_Id) DESC,
    isnull(Album_Name) DESC,
    isnull(Release_Date) DESC,
    isnull(Total_Tracks) DESC,
    TimeStamp
LIMIT 100

/*Tracks in refresh order*/
CREATE VIEW Music_Refresh_Track AS
(SELECT a.Track_Id, a.Track_Name, a.Track_Duration_ms, a.Timestamp
FROM Music_Tracks as a
LEFT JOIN Music_Track_Listens as b
ON a.Track_Id = b.Track_Id)
UNION
(SELECT c.Track_Id, c.Track_Name, c.Track_Duration_ms, c.Timestamp
FROM Music_Tracks as c
RIGHT JOIN Music_Track_Listens as d
ON c.Track_Id = d.Track_Id
WHERE c.Track_Id IS NULL)
ORDER BY isnull(Track_Name) DESC,
isnull(Track_Duration_ms) DESC,
isnull(Timestamp) DESC,
Timestamp
LIMIT 100

/*Summarise each id for total listens*/
CREATE VIEW Music_Track_Plays AS
SELECT 
	Track_Id,
    SUM(Plays) as Plays
FROM `Music_Track_Listens`
GROUP BY Track_Id
ORDER BY Plays DESC;

