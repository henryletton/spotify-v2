/*Table for track listens*/
CREATE TABLE Music_Track_Listens (
	Track_Id TEXT,
	Track_Name TEXT,
	DateTime TIMESTAMP,
	Plays INT,
	Skips INT,
	Source TEXT,
	PRIMARY KEY (Track_Id(30),DateTime)
)

/*Table to store track information*/
CREATE TABLE Music_Tracks (
	Track_Id TEXT,
	Track_Name TEXT,
	ISRC TEXT,
	Danceability FLOAT,
	Energy FLOAT,
	Loudness FLOAT,
	Speechiness FLOAT,
	Acousticness FLOAT,
	Instrumentalness FLOAT,
	Liveness FLOAT,
	Valence FLOAT,
	Tempo FLOAT,
	Time_Signature INT,
	Track_Duration_ms FLOAT,
	Explicit TEXT,
	Explicit_Track BOOL,
	Track_Number INT,
	Disc_Number INT,
	/*Key_Name TEXT,*/
	`Key` INT,
	/*Mode_Name TEXT,*/
	`Mode` INT,
	Track_Popularity INT,
	Removed_Track INT,
	Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (Track_Id(30))
)

/*Table for artist information*/
CREATE TABLE Music_Artists (
	Artist_Id TEXT,
	Artist_Name VARCHAR(255),
	Artist_Popularity INT,
	Total_Followers INT,
	Removed_Artist INT,
	Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (Artist_Id(30))
)

/*Table for album information*/
CREATE TABLE Music_Albums (
	Album_Id TEXT,
	Album_Name TEXT,
	UPC TEXT,
	Release_Date DATE,
	Total_Tracks INT,
	Album_Type TEXT,
	Label TEXT,
	Removed_Album INT,
	Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY (Album_Id(30))
)

/*Tables for mappings*/
CREATE TABLE Music_Artist_Track_Mapping (
	Artist_Id TEXT,
	Track_Id TEXT,
	PRIMARY KEY (Artist_Id(30),Track_Id(30))
)

CREATE TABLE Music_Artist_Album_Mapping (
	Artist_Id TEXT,
	Album_Id TEXT,
	PRIMARY KEY (Artist_Id(30),Album_Id(30))
)

CREATE TABLE Music_Album_Track_Mapping (
	Album_Id TEXT,
	Track_Id TEXT,
	PRIMARY KEY (Album_Id(30),Track_Id(30))
)

/*Table for genres*/
CREATE TABLE Music_Genres (
	Id TEXT,
	Genre TEXT,
	Type TEXT,
	PRIMARY KEY (Id(30),Genre(50),Type(10))
)

/*Table for process log, not specific to this project*/
CREATE TABLE Event_Log (
	Event_Key INT AUTO_INCREMENT PRIMARY KEY,
	Project TEXT,
	Process TEXT,
	Details TEXT,
	Event_Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)

