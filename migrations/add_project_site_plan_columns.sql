-- Add site plan columns to project table
ALTER TABLE project 
ADD COLUMN site_plan_image VARCHAR(255) DEFAULT NULL AFTER address,
ADD COLUMN site_plan_width INT DEFAULT NULL AFTER site_plan_image,
ADD COLUMN site_plan_height INT DEFAULT NULL AFTER site_plan_width;

-- Update existing rows with default values for the new columns
UPDATE project SET site_plan_width = 0 WHERE site_plan_width IS NULL;
UPDATE project SET site_plan_height = 0 WHERE site_plan_height IS NULL;


