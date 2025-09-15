-- Drop existing FULLTEXT indexes if they exist
DROP INDEX IF EXISTS `idx_house_search` ON `house`;
DROP INDEX IF EXISTS `idx_project_search` ON `project`;
DROP INDEX IF EXISTS `idx_house_type_search` ON `house_type`;

-- Add FULLTEXT index for house table
ALTER TABLE `house` 
ADD FULLTEXT INDEX `idx_house_search` (`h_title`, `h_description`);

-- Add FULLTEXT index for project table
ALTER TABLE `project` 
ADD FULLTEXT INDEX `idx_project_search` (`p_name`, `p_description`);

-- Add FULLTEXT index for house_type table
ALTER TABLE `house_type` 
ADD FULLTEXT INDEX `idx_house_type_search` (`t_name`, `t_description`);

-- Verify the indexes were created
SHOW INDEX FROM `house` WHERE Key_name = 'idx_house_search';
SHOW INDEX FROM `project` WHERE Key_name = 'idx_project_search';
SHOW INDEX FROM `house_type` WHERE Key_name = 'idx_house_type_search';
