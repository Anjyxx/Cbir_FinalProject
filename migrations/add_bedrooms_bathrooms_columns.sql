-- Add bedrooms and bathrooms columns to house table if they don't exist
ALTER TABLE house 
ADD COLUMN IF NOT EXISTS bedrooms INT DEFAULT 0,
ADD COLUMN IF NOT EXISTS bathrooms INT DEFAULT 0,
ADD COLUMN IF NOT EXISTS living_area DECIMAL(10,2) DEFAULT 0.00;

-- Update existing rows with default values if needed
UPDATE house SET bedrooms = 0 WHERE bedrooms IS NULL;
UPDATE house SET bathrooms = 0 WHERE bathrooms IS NULL;
UPDATE house SET living_area = 0.00 WHERE living_area IS NULL;

-- Add indexes for better search performance
CREATE INDEX IF NOT EXISTS idx_house_bedrooms ON house(bedrooms);
CREATE INDEX IF NOT EXISTS idx_house_bathrooms ON house(bathrooms);
CREATE INDEX IF NOT EXISTS idx_house_living_area ON house(living_area);
