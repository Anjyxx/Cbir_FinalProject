-- Migration: Add image embeddings table for CBIR functionality
-- Created: 2025-01-27

-- Create table for storing image embeddings
CREATE TABLE `image_embeddings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `image_id` int(11) NOT NULL,
  `house_id` int(11) NOT NULL,
  `image_url` varchar(255) NOT NULL,
  `embedding` LONGBLOB NOT NULL,
  `embedding_type` enum('visual','style') NOT NULL DEFAULT 'visual',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `idx_house_id` (`house_id`),
  KEY `idx_image_id` (`image_id`),
  KEY `idx_embedding_type` (`embedding_type`),
  FOREIGN KEY (`house_id`) REFERENCES `house`(`h_id`) ON DELETE CASCADE,
  FOREIGN KEY (`image_id`) REFERENCES `house_images`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Add index for faster similarity searches
CREATE INDEX `idx_embedding_search` ON `image_embeddings` (`embedding_type`, `house_id`);
