-- Add is_available column to houses table
ALTER TABLE houses ADD COLUMN IF NOT EXISTS is_available BOOLEAN DEFAULT TRUE;

-- Add is_available column to projects table
ALTER TABLE projects ADD COLUMN IF NOT EXISTS is_available BOOLEAN DEFAULT TRUE;

-- Add is_available column to house_types table
ALTER TABLE house_types ADD COLUMN IF NOT EXISTS is_available BOOLEAN DEFAULT TRUE;

-- Add is_available column to house_features table
ALTER TABLE house_features ADD COLUMN IF NOT EXISTS is_available BOOLEAN DEFAULT TRUE;

-- Update existing records to be available by default
UPDATE houses SET is_available = TRUE WHERE is_available IS NULL;
UPDATE projects SET is_available = TRUE WHERE is_available IS NULL;
UPDATE house_types SET is_available = TRUE WHERE is_available IS NULL;
UPDATE house_features SET is_available = TRUE WHERE is_available IS NULL;
