import unittest
import os
import sys
import json
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, mysql
from search_utils import SearchQuery, preprocess_search_term, THAI_STOP_WORDS

class TestSearchFunctionality(unittest.TestCase):    
    def setUp(self):
        """Set up test client and configure app for testing."""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        
        # Create a test database connection
        self.connection = mysql.connection
        self.cursor = self.connection.cursor()
        
        # Create test data
        self.setup_test_data()
    
    def tearDown(self):
        """Clean up after tests."""
        self.cleanup_test_data()
        self.cursor.close()
    
    def setup_test_data(self):
        """Set up test data in the database."""
        try:
            # Create test project
            self.cursor.execute("""
                INSERT INTO project (p_name, p_location, p_description, created_at)
                VALUES (%s, %s, %s, %s)
            """, ("Test Project", "Bangkok", "A test project", datetime.now()))
            self.project_id = self.cursor.lastrowid
            
            # Create test house type
            self.cursor.execute("""
                INSERT INTO house_type (t_name, t_description, created_at)
                VALUES (%s, %s, %s)
            """, ("Test Type", "A test house type", datetime.now()))
            self.house_type_id = self.cursor.lastrowid
            
            # Create test house
            self.cursor.execute("""
                INSERT INTO house 
                (h_title, h_description, h_features, price, bedrooms, bathrooms, 
                 living_area, p_id, t_id, created_at, view_count)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                "Luxury Test Villa", 
                "A beautiful test villa with great features and a modern design",
                "Swimming Pool,Garden,Modern Kitchen",
                10000000,  # 10M THB
                4,         # 4 bedrooms
                3.5,       # 3.5 bathrooms
                250,       # 250 sqm
                self.project_id,
                self.house_type_id,
                datetime.now(),
                10  # View count
            ))
            self.house_id = self.cursor.lastrowid
            
            # Create test feature
            self.cursor.execute("""
                INSERT INTO house_features (f_name, f_description, created_at)
                VALUES (%s, %s, %s)
            """, ("Swimming Pool", "Private swimming pool with jacuzzi", datetime.now()))
            self.feature_id = self.cursor.lastrowid
            
            # Link feature to house
            self.cursor.execute("""
                INSERT INTO house_has_features (house_id, feature_id, created_at)
                VALUES (%s, %s, %s)
            """, (self.house_id, self.feature_id, datetime.now()))
            
            # Create a view for the house
            self.cursor.execute("""
                INSERT INTO house_views (house_id, ip_address, user_agent, created_at)
                VALUES (%s, %s, %s, %s)
            """, (self.house_id, "127.0.0.1", "test-agent", datetime.now()))
            
            # Commit the test data
            self.connection.commit()
            
        except Exception as e:
            print(f"Error setting up test data: {e}")
            self.connection.rollback()
            raise
    
    def cleanup_test_data(self):
        """Clean up test data from the database."""
        try:
            # Clean up in reverse order of creation to respect foreign key constraints
            self.cursor.execute("DELETE FROM house_views WHERE house_id = %s", (self.house_id,))
            self.cursor.execute("DELETE FROM house_has_features WHERE house_id = %s", (self.house_id,))
            self.cursor.execute("DELETE FROM house_has_features WHERE feature_id = %s", (self.feature_id,))
            self.cursor.execute("DELETE FROM house WHERE h_id = %s", (self.house_id,))
            self.cursor.execute("DELETE FROM house_features WHERE f_id = %s", (self.feature_id,))
            self.cursor.execute("DELETE FROM house_type WHERE t_id = %s", (self.house_type_id,))
            self.cursor.execute("DELETE FROM project WHERE p_id = %s", (self.project_id,))
            
            # Clean up search logs
            self.cursor.execute("TRUNCATE TABLE search_logs")
            self.cursor.execute("TRUNCATE TABLE search_suggestions")
            
            self.connection.commit()
        except Exception as e:
            print(f"Error cleaning up test data: {e}")
            self.connection.rollback()
    
    def test_preprocess_search_term(self):
        """Test search term preprocessing."""
        # Test basic preprocessing
        self.assertEqual(preprocess_search_term("  Test  Term  "), "test term")
        
        # Test special character removal
        self.assertEqual(preprocess_search_term("Test-Term!@#"), "testterm")
        
        # Test Thai language support
        self.assertEqual(preprocess_search_term("บ้าน"), "บ้าน")
        
        # Test stop word removal
        self.assertEqual(preprocess_search_term("this is a test"), "test")
    
    def test_search_query_basic(self):
        """Test basic search query functionality."""
        # Test basic search
        query = SearchQuery("luxury villa")
        where_clause, params = query.build_where_clause()
        
        self.assertIn("h_title LIKE %s", where_clause)
        self.assertIn("%luxury%", params)
        self.assertIn("%villa%", params)
    
    def test_search_query_filters(self):
        """Test search with filters."""
        # Test price filter
        query = SearchQuery("villa price:5000000-15000000")
        where_clause, params = query.build_where_clause()
        self.assertIn("h.price BETWEEN %s AND %s", where_clause)
        self.assertIn(5000000, params)
        self.assertIn(15000000, params)
        
        # Test bedroom filter
        query = SearchQuery("bedrooms:3-5")
        where_clause, params = query.build_where_clause()
        self.assertIn("h.bedrooms BETWEEN %s AND %s", where_clause)
        self.assertEqual(params, [3, 5])
    
    def test_search_query_required_terms(self):
        """Test search with required terms."""
        query = SearchQuery("+villa +pool")
        where_clause, params = query.build_where_clause()
        
        # Should have conditions for both required terms
        self.assertEqual(where_clause.count("h_title LIKE %s"), 2)
        self.assertIn("%villa%", params)
        self.assertIn("%pool%", params)
    
    def test_search_query_excluded_terms(self):
        """Test search with excluded terms."""
        query = SearchQuery("villa -condo")
        where_clause, params = query.build_where_clause()
        
        # Should have a condition to exclude condo
        self.assertIn("h_title NOT LIKE %s", where_clause)
        self.assertIn("%condo%", params)
    
    def test_search_suggestions_api(self):
        """Test the search suggestions API endpoint."""
        # Test with a query that should match our test data
        response = self.app.get('/api/search/suggest?q=luxury')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        
        # Check if our test house is in the results
        house_titles = [item['text'] for item in data if item['type'] == 'house']
        self.assertIn("Luxury Test Villa", house_titles)
    
    def test_search_relevance_scoring(self):
        """Test that search results are ordered by relevance."""
        # Create another test house that should be less relevant
        self.cursor.execute("""
            INSERT INTO house 
            (h_title, h_description, h_features, price, bedrooms, bathrooms, 
             living_area, p_id, t_id, created_at, view_count)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            "Another Villa", 
            "A standard villa with basic features",
            "Garden",
            8000000,
            3,
            2,
            180,
            self.project_id,
            self.house_type_id,
            datetime.now(),
            2  # Lower view count
        ))
        self.connection.commit()
        
        # Search for a term that appears in both houses but should rank the first higher
        query = SearchQuery("villa features")
        where_clause, params = query.build_where_clause()
        order_by = query.build_order_by_clause()
        
        # Execute the query
        sql = f"""
            SELECT h.h_id, h.h_title, h.h_description, h.h_features, 
                   h.view_count, h.created_at, p.p_name, t.t_name,
                   CASE 
                       WHEN h.h_title LIKE %s THEN 30
                       WHEN h.h_description LIKE %s THEN 20
                       WHEN h.h_features LIKE %s THEN 10
                       ELSE 0
                   END as relevance
            FROM house h
            LEFT JOIN project p ON h.p_id = p.p_id
            LEFT JOIN house_type t ON h.t_id = t.t_id
            WHERE {where_clause}
            {order_by}
            LIMIT 10
        """
        
        # Add the relevance parameters
        search_param = f"%villa%"
        params = [search_param, search_param, search_param] + params
        
        self.cursor.execute(sql, params)
        results = self.cursor.fetchall()
        
        # The first result should be our more relevant test house
        self.assertGreater(len(results), 0)
        self.assertEqual(results[0]['h_title'], "Luxury Test Villa")
    
    def test_search_analytics_logging(self):
        """Test that search queries are logged for analytics."""
        # Perform a search
        self.app.get('/api/search/suggest?q=test')
        
        # Check that the search was logged
        self.cursor.execute("""
            SELECT * FROM search_logs 
            WHERE query = 'test' 
            AND result_count > 0
        """)
        log_entry = self.cursor.fetchone()
        self.assertIsNotNone(log_entry)
        self.assertEqual(log_entry['query'], 'test')
        self.assertGreater(log_entry['result_count'], 0)

if __name__ == '__main__':
    unittest.main()
