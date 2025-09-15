-- Add p_description column to project table
ALTER TABLE project 
ADD COLUMN p_description TEXT DEFAULT NULL AFTER p_name,
ADD COLUMN p_location VARCHAR(255) DEFAULT NULL AFTER p_description;

-- Update existing rows with empty values for the new columns
UPDATE project SET p_description = '' WHERE p_description IS NULL;
UPDATE project SET p_location = '' WHERE p_location IS NULL;
