-- Add FULLTEXT index for house_type table
-- First drop existing index if it exists
DROP INDEX IF EXISTS `idx_house_type_search` ON `house_type`;

-- Add FULLTEXT index for t_name and t_description (if it exists)
-- MySQL will ignore the non-existent column with IF NOT EXISTS
ALTER TABLE `house_type`
ADD FULLTEXT INDEX `idx_house_type_search` (`t_name`, `t_description`)
WITH PARSER ngram
COMMENT 'Full-text index for house type search with ngram parser';

-- For older MySQL versions that don't support IF NOT EXISTS for columns
-- We'll use a stored procedure to handle this conditionally
DELIMITER //
CREATE PROCEDURE AddHouseTypeFTSIndex()
BEGIN
    DECLARE CONTINUE HANDLER FOR 1061 BEGIN END; -- Error 1061 is 'duplicate key name'
    ALTER TABLE `house_type`
    ADD FULLTEXT INDEX `idx_house_type_search` (`t_name`, `t_description`)
    WITH PARSER ngram
    COMMENT 'Full-text index for house type search with ngram parser';
END //
DELIMITER ;

-- Execute the procedure
CALL AddHouseTypeFTSIndex();

-- Clean up
DROP PROCEDURE IF EXISTS AddHouseTypeFTSIndex;

-- Also add FULLTEXT index for project table if not exists
DROP INDEX IF EXISTS `idx_project_search` ON `project`;

ALTER TABLE `project`
ADD FULLTEXT INDEX `idx_project_search` (`p_name`, `p_description`)
WITH PARSER ngram
COMMENT 'Full-text index for project search with ngram parser';

-- Add FULLTEXT index for house table if not exists
DROP INDEX IF EXISTS `idx_house_search` ON `house`;

ALTER TABLE `house`
ADD FULLTEXT INDEX `idx_house_search` (`h_title`, `h_description`)
WITH PARSER ngram
COMMENT 'Full-text index for house search with ngram parser';
