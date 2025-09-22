-- Add architectural style columns to house table
ALTER TABLE house 
ADD COLUMN architectural_style VARCHAR(50) DEFAULT NULL AFTER unit_brand,
ADD COLUMN style_confidence DECIMAL(5,4) DEFAULT NULL AFTER architectural_style,
ADD COLUMN style_features LONGTEXT DEFAULT NULL AFTER style_confidence;

-- Create index for faster style-based searches
CREATE INDEX idx_house_architectural_style ON house(architectural_style);
CREATE INDEX idx_house_style_confidence ON house(style_confidence);

-- Update existing rows with default values
UPDATE house SET style_confidence = 0.0 WHERE style_confidence IS NULL;


