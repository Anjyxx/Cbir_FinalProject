-- Create search logs table for tracking search queries and results
CREATE TABLE IF NOT EXISTS search_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    query VARCHAR(255) NOT NULL,
    result_count INT NOT NULL,
    user_id INT NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    referrer VARCHAR(512) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_search_logs_query (query),
    INDEX idx_search_logs_created_at (created_at),
    INDEX idx_search_logs_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create search suggestions table for caching popular searches
CREATE TABLE IF NOT EXISTS search_suggestions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    term VARCHAR(255) NOT NULL,
    type ENUM('house', 'project', 'feature') NOT NULL,
    item_id INT NOT NULL,
    popularity INT DEFAULT 1,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_term_type_item (term, type, item_id),
    INDEX idx_search_suggestions_term (term),
    INDEX idx_search_suggestions_popularity (popularity)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create search analytics table for advanced reporting
CREATE TABLE IF NOT EXISTS search_analytics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    query VARCHAR(255) NOT NULL,
    search_count INT DEFAULT 1,
    result_count_avg FLOAT NULL,
    result_count_total INT NULL,
    no_results_count INT DEFAULT 0,
    UNIQUE KEY uk_date_query (date, query(191)),
    INDEX idx_search_analytics_date (date),
    INDEX idx_search_analytics_query (query(191))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add full-text indexes for better search performance
ALTER TABLE house 
ADD FULLTEXT INDEX `idx_house_search` (`h_title`, `h_description`, `h_features`) 
WITH PARSER ngram
COMMENT 'Full-text index for house search with ngram parser for better Thai language support';

ALTER TABLE project
ADD FULLTEXT INDEX `idx_project_search` (`p_name`, `p_description`, `p_location`)
WITH PARSER ngram
COMMENT 'Full-text index for project search with ngram parser';

-- Add regular indexes for frequently searched columns
CREATE INDEX IF NOT EXISTS idx_house_title ON house(h_title);
CREATE INDEX IF NOT EXISTS idx_house_price ON house(price);
CREATE INDEX IF NOT EXISTS idx_house_bedrooms ON house(bedrooms);
CREATE INDEX IF NOT EXISTS idx_house_bathrooms ON house(bathrooms);
CREATE INDEX IF NOT EXISTS idx_house_created_at ON house(created_at);
CREATE INDEX IF NOT EXISTS idx_project_name ON project(p_name);
CREATE INDEX IF NOT EXISTS idx_project_location ON project(p_location);

-- Create a view for popular searches
CREATE OR REPLACE VIEW vw_popular_searches AS
SELECT 
    query,
    COUNT(*) as search_count,
    AVG(result_count) as avg_results,
    MAX(created_at) as last_searched
FROM search_logs
WHERE created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY query
ORDER BY search_count DESC
LIMIT 100;

-- Create a stored procedure for updating search suggestions
DELIMITER //
CREATE PROCEDURE update_search_suggestions()
BEGIN
    -- Update house suggestions
    INSERT INTO search_suggestions (term, type, item_id, popularity, last_updated)
    SELECT 
        h.h_title as term,
        'house' as type,
        h.h_id as item_id,
        COUNT(*) as popularity,
        NOW() as last_updated
    FROM house h
    JOIN house_views hv ON h.h_id = hv.house_id
    WHERE hv.created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
    GROUP BY h.h_id, h.h_title
    ON DUPLICATE KEY UPDATE 
        popularity = VALUES(popularity),
        last_updated = NOW();
    
    -- Update project suggestions
    INSERT INTO search_suggestions (term, type, item_id, popularity, last_updated)
    SELECT 
        p.p_name as term,
        'project' as type,
        p.p_id as item_id,
        COUNT(DISTINCT h.h_id) as popularity,
        NOW() as last_updated
    FROM project p
    JOIN house h ON p.p_id = h.p_id
    JOIN house_views hv ON h.h_id = hv.house_id
    WHERE hv.created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
    GROUP BY p.p_id, p.p_name
    ON DUPLICATE KEY UPDATE 
        popularity = VALUES(popularity),
        last_updated = NOW();
    
    -- Clean up old suggestions
    DELETE FROM search_suggestions 
    WHERE last_updated < DATE_SUB(NOW(), INTERVAL 90 DAY);
END //
DELIMITER ;

-- Create an event to update search suggestions daily
DELIMITER //
CREATE EVENT IF NOT EXISTS event_update_search_suggestions
ON SCHEDULE EVERY 1 DAY
STARTS TIMESTAMP(CURRENT_DATE, '03:00:00')
DO
BEGIN
    CALL update_search_suggestions();
END //
DELIMITER ;

-- Create a function to calculate search relevance score
DELIMITER //
CREATE FUNCTION calculate_relevance(
    p_title_match BOOLEAN,
    p_description_match BOOLEAN,
    p_features_match BOOLEAN,
    p_view_count INT,
    p_created_at DATETIME
) RETURNS FLOAT
DETERMINISTIC
BEGIN
    DECLARE v_relevance FLOAT DEFAULT 0.0;
    DECLARE v_days_old INT;
    
    -- Base relevance based on match type
    IF p_title_match THEN
        SET v_relevance = v_relevance + 10.0;
    END IF;
    
    IF p_description_match THEN
        SET v_relevance = v_relevance + 5.0;
    END IF;
    
    IF p_features_match THEN
        SET v_relevance = v_relevance + 3.0;
    END IF;
    
    -- Boost by view count (logarithmic scale)
    IF p_view_count > 0 THEN
        SET v_relevance = v_relevance + LEAST(LOG2(p_view_count + 1), 5.0);
    END IF;
    
    -- Age decay (reduce relevance for older listings)
    SET v_days_old = DATEDIFF(NOW(), p_created_at);
    IF v_days_old > 0 THEN
        SET v_relevance = v_relevance * EXP(-0.1 * v_days_old / 30);  -- Half-life of 30 days
    END IF;
    
    RETURN v_relevance;
END //
DELIMITER ;

-- Create a view for search analytics dashboard
CREATE OR REPLACE VIEW vw_search_analytics AS
SELECT 
    DATE(created_at) as search_date,
    COUNT(*) as total_searches,
    COUNT(DISTINCT query) as unique_queries,
    AVG(result_count) as avg_results_per_search,
    SUM(CASE WHEN result_count = 0 THEN 1 ELSE 0 END) as no_result_searches,
    COUNT(DISTINCT user_id) as unique_users
FROM search_logs
WHERE created_at > DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(created_at)
ORDER BY search_date DESC;
