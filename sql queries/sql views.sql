
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
LIMIT 25;

/*Albums in refresh order*/
CREATE VIEW Music_Refresh_Album AS
SELECT *
FROM Music_Albums
ORDER BY isnull(Album_Id) DESC,
    isnull(Album_Name) DESC,
    isnull(Release_Date) DESC,
    isnull(Total_Tracks) DESC,
    TimeStamp
LIMIT 500;

/*Tracks in refresh order*/
CREATE VIEW Music_Refresh_Track AS
(SELECT a.Track_Id, a.Track_Name, a.Track_Duration_ms, a.Timestamp, a.ISRC, CASE WHEN b.DateTime IS NOT NULL THEN 1 ELSE 0 END AS Played
FROM Music_Tracks as a
LEFT JOIN Music_Track_Listens as b
ON a.Track_Id = b.Track_Id
WHERE CAST(a.Timestamp as date) < CURDATE() - 7 OR a.Track_Name IS NULL)
UNION
(SELECT d.Track_Id, c.Track_Name, c.Track_Duration_ms, c.Timestamp, c.ISRC, 1 as Played
FROM Music_Tracks as c
RIGHT JOIN Music_Track_Listens as d
ON c.Track_Id = d.Track_Id
WHERE c.Track_Id IS NULL)
ORDER BY isnull(Track_Name) DESC,
isnull(Track_Duration_ms) DESC,
isnull(ISRC) DESC,
Played DESC,
Timestamp
LIMIT 2500;

/*Summarise each id for total listens*/
CREATE VIEW Music_Track_Plays AS
SELECT 
	Track_Id,
    SUM(Plays) as Plays
FROM `Music_Track_Listens`
GROUP BY Track_Id
ORDER BY Plays DESC;

/*Combined data to use in a dashboard*/
CREATE VIEW Music_Dashboard AS
	SELECT t.*, 
		l.DateTime, l.Plays, l.Skips, l.Source,
		al.Album_Name, al.Release_Date, al.Total_Tracks, al.Album_Type, al.Label,
		ar.Artist_Name, ar.Artist_Popularity, ar.Total_Followers
	FROM `Music_Tracks` AS t
	INNER JOIN `Music_Track_Listens` as l
		ON t.Track_Id = l.Track_Id
	LEFT JOIN `Music_Album_Track_Mapping` as alt
		ON t.Track_Id = alt.Track_Id
	LEFT JOIN `Music_Albums` as al
		ON alt.Album_Id = al.Album_Id
	LEFT JOIN `Music_Artist_Track_Mapping` as art
		ON t.Track_Id = art.Track_Id
	LEFT JOIN `Music_Artists` as ar
		ON art.Artist_Id = ar.Artist_Id;

