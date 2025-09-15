-- Add FULLTEXT indexes for search functionality

-- For house table
ALTER TABLE house 
ADD FULLTEXT INDEX `idx_house_title_desc` (h_title, h_description);

-- For project table
ALTER TABLE project 
ADD FULLTEXT INDEX `idx_project_name_desc` (p_name, `description`);

-- For house_type table
ALTER TABLE house_type 
ADD FULLTEXT INDEX `idx_type_name_desc` (t_name, t_description);
