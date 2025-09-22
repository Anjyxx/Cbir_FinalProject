-- Migration: Add Project Unit Management Support
-- This migration adds support for project site plans and house unit identification

-- Add site plan columns to project table
ALTER TABLE project 
ADD COLUMN site_plan_image VARCHAR(255) DEFAULT NULL AFTER address,
ADD COLUMN site_plan_width INT DEFAULT 0 AFTER site_plan_image,
ADD COLUMN site_plan_height INT DEFAULT 0 AFTER site_plan_width;

-- Add unit identification columns to house table
ALTER TABLE house 
ADD COLUMN unit_number VARCHAR(50) DEFAULT NULL AFTER view_count,
ADD COLUMN unit_x_position INT DEFAULT 0 AFTER unit_number,
ADD COLUMN unit_y_position INT DEFAULT 0 AFTER unit_x_position,
ADD COLUMN unit_brand VARCHAR(100) DEFAULT NULL AFTER unit_y_position;
