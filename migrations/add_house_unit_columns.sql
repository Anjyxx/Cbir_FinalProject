-- Add unit identification columns to house table
ALTER TABLE house 
ADD COLUMN unit_number VARCHAR(50) DEFAULT NULL AFTER view_count,
ADD COLUMN unit_x_position INT DEFAULT NULL AFTER unit_number,
ADD COLUMN unit_y_position INT DEFAULT NULL AFTER unit_x_position,
ADD COLUMN unit_brand VARCHAR(100) DEFAULT NULL AFTER unit_y_position;

-- Update existing rows with default values for the new columns
UPDATE house SET unit_x_position = 0 WHERE unit_x_position IS NULL;
UPDATE house SET unit_y_position = 0 WHERE unit_y_position IS NULL;


