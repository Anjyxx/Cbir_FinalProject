-- Drop search-related indexes
DROP INDEX IF EXISTS `idx_house_search` ON house;
DROP INDEX IF EXISTS `idx_project_search` ON project;
DROP INDEX IF EXISTS `idx_type_search` ON house_type;
DROP INDEX IF EXISTS `idx_feature_search` ON house_features;

-- Drop any search-related tables if they exist
-- Note: Add any search-specific tables here if they exist
-- DROP TABLE IF EXISTS search_index;

-- Drop any search-related views if they exist
-- DROP VIEW IF EXISTS vw_search_results;

-- Drop any search-related stored procedures if they exist
-- DROP PROCEDURE IF EXISTS sp_search_houses;
