# Enhanced Search Functionality

This document describes the enhanced search functionality for the real estate website, including features, setup instructions, and usage examples.

## Features

### 1. Advanced Search Capabilities
- Full-text search with relevance scoring
- Fuzzy matching for typos and variations
- Support for search operators (AND, OR, NOT, quotes, etc.)
- Field-specific searching (title, description, features, etc.)
- Range filters for price, bedrooms, bathrooms, and area
- Date-based filtering

### 2. Smart Search Suggestions
- Real-time suggestions as users type
- Contextual results with additional metadata
- Popular searches and trending properties
- Personalized suggestions based on user history

### 3. Performance Optimizations
- Database indexing for faster queries
- Query caching
- Efficient pagination
- Asynchronous processing for heavy operations

### 4. Analytics and Reporting
- Search query logging
- Click-through tracking
- No-result query detection
- Popular search terms and trends

## Setup Instructions

### 1. Prerequisites
- Python 3.8+
- MySQL 8.0+
- Redis (for caching and async tasks, optional)

### 2. Install Dependencies
```bash
pip install -r requirements-search.txt
```

### 3. Database Setup
1. Create a MySQL database if you haven't already
2. Update your `.env` file with database credentials:
   ```
   MYSQL_HOST=localhost
   MYSQL_USER=your_username
   MYSQL_PASSWORD=your_password
   MYSQL_DB=your_database
   ```

### 4. Apply Database Migrations
```bash
python apply_search_migrations.py
```

### 5. Configuration
Create or update your Flask configuration in `config.py`:

```python
class Config:
    # Search configuration
    SEARCH_RESULTS_PER_PAGE = 20
    SEARCH_SUGGESTION_LIMIT = 10
    SEARCH_CACHE_TIMEOUT = 3600  # 1 hour
    
    # Enable/disable features
    ENABLE_SEARCH_ANALYTICS = True
    ENABLE_SEARCH_SUGGESTIONS = True
    ENABLE_FUZZY_SEARCH = True
    
    # Performance settings
    SEARCH_QUERY_TIMEOUT = 5  # seconds
    MAX_SEARCH_RESULTS = 1000
```

## Usage Examples

### Basic Search
```python
from search_utils import SearchQuery

# Simple search
query = SearchQuery("luxury villa")
where_clause, params = query.build_where_clause()
order_by = query.build_order_by_clause()
limit = query.build_limit_clause()

# Execute query with your database connection
sql = f"""
    SELECT h.*, p.p_name, t.t_name 
    FROM house h
    LEFT JOIN project p ON h.p_id = p.p_id
    LEFT JOIN house_type t ON h.t_id = t.t_id
    WHERE {where_clause}
    {order_by}
    {limit}
"""
cursor.execute(sql, params)
results = cursor.fetchall()
```

### Advanced Search with Filters
```python
# Search for 3-4 bedroom houses in Bangkok under 10M THB
query = SearchQuery(
    "Bangkok price:0-10000000 bedrooms:3-4 sort:price:asc"
)
```

### Search Suggestions API
```
GET /api/search/suggest?q=bang

Response:
[
  {
    "text": "Bangkok Riverside",
    "type": "project",
    "id": 123,
    "location": "Bangkok",
    "house_count": 15,
    "image_url": "/images/projects/bangkok-riverside.jpg"
  },
  {
    "text": "Modern Luxury Villa",
    "type": "house",
    "id": 456,
    "project_name": "Bangkok Riverside",
    "house_type": "Villa",
    "price": 8500000,
    "bedrooms": 4,
    "bathrooms": 3,
    "image_url": "/images/houses/villa-456.jpg"
  }
]
```

## Performance Considerations

1. **Indexing**: Ensure all relevant columns are properly indexed
2. **Query Optimization**: Use `EXPLAIN` to analyze and optimize slow queries
3. **Caching**: Implement caching for frequent search queries
4. **Pagination**: Always implement pagination to limit result sets
5. **Asynchronous Processing**: Use Celery for resource-intensive operations

## Monitoring and Maintenance

1. **Logging**: All search queries are logged to the `search_logs` table
2. **Analytics**: Use the `vw_search_analytics` view for search metrics
3. **Cleanup**: Old search logs are automatically cleaned up after 90 days

## Troubleshooting

### Common Issues
1. **Slow Search Queries**
   - Check database indexes
   - Review query execution plans
   - Consider adding query caching

2. **Inaccurate Search Results**
   - Verify full-text search configuration
   - Check for stop words that might be filtered out
   - Review relevance scoring weights

3. **Character Encoding Issues**
   - Ensure database uses UTF-8 encoding
   - Verify client connection encoding
   - Check for proper collation settings

## Future Enhancements

1. **Semantic Search**: Implement NLP for better understanding of search intent
2. **Image Search**: Enhance CBIR (Content-Based Image Retrieval) capabilities
3. **Personalization**: User-specific search results based on preferences and history
4. **Voice Search**: Support for voice-based search queries
5. **Multi-language Support**: Improved support for multiple languages

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
