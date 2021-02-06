/*Copy table schema*/
CREATE TABLE Music_Track_Listens_py LIKE Music_Track_Listens;

/*Add new column to existing table*/
ALTER TABLE Music_Tracks ADD Removed_Track INT AFTER Track_Popularity;
ALTER TABLE Music_Tracks ADD `Key` INT AFTER Key_Name;
ALTER TABLE Music_Tracks ADD `Mode` INT AFTER Mode_Name;
ALTER TABLE Music_Tracks ADD Explicit_Track BOOL AFTER Explicit;
ALTER TABLE Music_Tracks ADD Disc_Number INT AFTER Track_Number;
ALTER TABLE Music_Tracks ADD ISRC TEXT AFTER Track_Name;
ALTER TABLE Music_Artists ADD Removed_Artist INT AFTER Total_Followers;
ALTER TABLE Music_Albums ADD Removed_Album INT AFTER Total_Tracks;
ALTER TABLE Music_Albums ADD Album_Type TEXT AFTER Total_Tracks;
ALTER TABLE Music_Albums ADD Label TEXT AFTER Total_Tracks;
ALTER TABLE Music_Albums ADD UPC TEXT AFTER Album_Name;

