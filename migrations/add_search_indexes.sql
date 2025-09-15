-- Drop existing indexes if they exist
DROP INDEX IF EXISTS `idx_house_search` ON house;
DROP INDEX IF EXISTS `idx_project_search` ON project;
DROP INDEX IF EXISTS `idx_type_search` ON house_type;
DROP INDEX IF EXISTS `idx_feature_search` ON house_features;
DROP INDEX IF EXISTS `idx_house_price` ON house;
DROP INDEX IF EXISTS `idx_house_living_area` ON house;

-- Create composite and individual column indexes for better query performance
-- House table indexes
CREATE INDEX idx_house_title ON house(h_title);
CREATE INDEX idx_house_bedrooms ON house(bedrooms);
CREATE INDEX idx_house_bathrooms ON house(bathrooms);
CREATE INDEX idx_house_living_area ON house(living_area);
CREATE INDEX idx_house_price ON house(price);
CREATE INDEX idx_house_created_at ON house(created_at);

-- Project table indexes
CREATE INDEX idx_project_name ON project(p_name);
CREATE INDEX idx_project_location ON project(p_location);

-- House type indexes
CREATE INDEX idx_house_type_name ON house_type(t_name);

-- House features indexes
CREATE INDEX idx_feature_name ON house_features(f_name);

-- Create composite indexes for common query patterns
CREATE INDEX idx_house_type_project ON house(t_id, p_id);
CREATE INDEX idx_house_price_range ON house(price, living_area, bedrooms);

-- Create full-text indexes with proper column weights
ALTER TABLE house 
ADD FULLTEXT INDEX `idx_house_search` (`h_title`(255), `h_description`(255), `h_features`(255)) 
WITH PARSER ngram
COMMENT 'Full-text index for house search with ngram parser for better Thai language support';

ALTER TABLE project
ADD FULLTEXT INDEX `idx_project_search` (`p_name`(255), `p_description`(255), `p_location`(255))
WITH PARSER ngram
COMMENT 'Full-text index for project search with ngram parser';

-- Add indexes for join operations
CREATE INDEX idx_house_type_id ON house(t_id);
CREATE INDEX idx_house_project_id ON house(p_id);

-- Add index for search suggestions
CREATE INDEX idx_suggestions ON house(h_title, p_id, (1=1)) COMMENT 'Index for search suggestions';

-- Analyze tables to update index statistics
ANALYZE TABLE house, project, house_type, house_features;
