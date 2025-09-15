import re
import jieba
import logging
import string
import unicodedata
from difflib import get_close_matches
from typing import List, Dict, Optional, Tuple, Set, Union, Any
from collections import defaultdict, Counter
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants for search relevance scoring
TITLE_WEIGHT = 5.0
DESCRIPTION_WEIGHT = 3.0
FEATURES_WEIGHT = 2.0
PROJECT_WEIGHT = 2.5
TYPE_WEIGHT = 2.0

# Common Thai stop words (add more as needed)
THAI_STOP_WORDS = {
    'และ', 'กับ', 'หรือ', 'แต่', 'ที่', 'ใน', 'ของ', 'ให้', 'ได้', 'ไป', 'มา', 'เป็น', 'คือ', 'ว่า', 'ๆ', 'นี้', 'นั้น', 'นั่น', 'นี่',
    'เขา', 'เธอ', 'ผม', 'ดิฉัน', 'คุณ', 'ท่าน', 'พวกเรา', 'พวกเขา', 'พวกเธอ', 'ผม', 'ฉัน', 'เรา', 'คุณ', 'ท่าน', 'เขา', 'เธอ', 'มัน', 'พวกเขา',
    'ซึ่ง', 'ว่า', 'ที่', 'จะ', 'ได้', 'ให้', 'แล้ว', 'ก็', 'เมื่อ', 'แต่', 'เพราะ', 'ว่า', 'เพื่อ', 'โดย', 'ตาม', 'อย่าง', 'เช่น', 'คือ',
    'ครับ', 'ค่ะ', 'คะ', 'จ้ะ', 'จ้า', 'นะ', 'น่ะ', 'นะคะ', 'นะครับ', 'จ๊ะ', 'จ๋า', 'สิ', 'ซิ', 'ซี', 'ดอก', 'เหรอ', 'หรือ', 'หรอก', 'หรือเปล่า'
}

# Common search operators
SEARCH_OPERATORS = {
    'AND', 'OR', 'NOT', 'AND NOT', 'OR NOT',
    '&&', '||', '!', '(', ')', '"',
    '>', '<', '>=', '<=', '=', '!=',
    'TO', '~', '*', '?'
}

class SearchQuery:
    """Class to represent a parsed search query with advanced features."""
    
    def __init__(self, original_query: str):
        self.original_query = original_query
        self.terms = []
        self.filters = {}
        self.required_terms = set()
        self.excluded_terms = set()
        self.phrases = []
        self.fuzzy_terms = []
        self.sort_by = None
        self.sort_order = 'DESC'
        self.limit = None
        self.offset = 0
        
        self._parse_query()
    
    def _parse_query(self) -> None:
        """Parse the search query into its components."""
        if not self.original_query:
            return
            
        # Handle special search operators
        self._extract_filters()
        self._extract_phrases()
        self._extract_required_terms()
        self._extract_excluded_terms()
        self._extract_sorting()
        self._extract_pagination()
        
        # Tokenize the remaining query
        self._tokenize_query()
    
    def _extract_filters(self) -> None:
        """Extract field filters from the query (e.g., price:1000000-2000000)."""
        filter_patterns = {
            'price': r'price:([\d,]+(?:-|to)[\d,]*)',
            'bedrooms': r'bedrooms:(\d+(?:\+|-\d+)?)',
            'bathrooms': r'bathrooms:(\d+(?:\.\d+)?(?:\+|-\d+)?)',
            'area': r'area:([\d,]+(?:-|to)[\d,]*)',
            'type': r'type:([\w\s]+)',
            'project': r'project:([\w\s]+)',
            'feature': r'feature:([\w\s]+)',
            'date': r'date:(\d{4}-\d{2}-\d{2}(?:,|to|\s+to\s+)\d{4}-\d{2}-\d{2}|today|yesterday|this_week|last_week|this_month|last_month|this_year|last_year)'
        }
        
        for field, pattern in filter_patterns.items():
            matches = list(re.finditer(pattern, self.original_query, re.IGNORECASE))
            for match in matches:
                self.filters[field] = match.group(1).strip()
                # Remove the filter from the original query
                self.original_query = self.original_query.replace(match.group(0), '').strip()
    
    def _extract_phrases(self) -> None:
        """Extract quoted phrases from the query."""
        phrase_matches = list(re.finditer(r'"([^"]+)"', self.original_query))
        for match in phrase_matches:
            self.phrases.append(match.group(1))
            # Remove the phrase from the original query
            self.original_query = self.original_query.replace(match.group(0), '').strip()
    
    def _extract_required_terms(self) -> None:
        """Extract required terms (prefixed with +)."""
        required_matches = list(re.finditer(r'\+([\w\p{Thai}]+)', self.original_query))
        for match in required_matches:
            self.required_terms.add(match.group(1).lower())
            # Remove the + prefix from the original query
            self.original_query = self.original_query.replace(match.group(0), '').strip()
    
    def _extract_excluded_terms(self) -> None:
        """Extract excluded terms (prefixed with -)."""
        excluded_matches = list(re.finditer(r'-([\w\p{Thai}]+)', self.original_query))
        for match in excluded_matches:
            self.excluded_terms.add(match.group(1).lower())
            # Remove the - prefix from the original query
            self.original_query = self.original_query.replace(match.group(0), '').strip()
    
    def _extract_sorting(self) -> None:
        """Extract sorting preferences from the query."""
        sort_match = re.search(r'sort:(\w+)(?::(asc|desc))?', self.original_query, re.IGNORECASE)
        if sort_match:
            self.sort_by = sort_match.group(1).lower()
            if sort_match.group(2):
                self.sort_order = sort_match.group(2).upper()
            # Remove the sort directive from the original query
            self.original_query = self.original_query.replace(sort_match.group(0), '').strip()
    
    def _extract_pagination(self) -> None:
        """Extract pagination parameters from the query."""
        # Handle limit
        limit_match = re.search(r'limit:(\d+)', self.original_query, re.IGNORECASE)
        if limit_match:
            self.limit = int(limit_match.group(1))
            self.original_query = self.original_query.replace(limit_match.group(0), '').strip()
        
        # Handle offset
        offset_match = re.search(r'offset:(\d+)', self.original_query, re.IGNORECASE)
        if offset_match:
            self.offset = int(offset_match.group(1))
            self.original_query = self.original_query.replace(offset_match.group(0), '').strip()
    
    def _tokenize_query(self) -> None:
        """Tokenize the remaining query into search terms."""
        if not self.original_query:
            return
        
        # Remove extra whitespace and normalize
        query = ' '.join(self.original_query.split())
        
        # Tokenize using jieba for Thai language support
        # Note: You might need to load a custom dictionary for better tokenization
        tokens = jieba.cut(query, cut_all=False)
        
        # Process tokens
        for token in tokens:
            token = token.strip()
            if not token or token in THAI_STOP_WORDS or token in SEARCH_OPERATORS:
                continue
                
            # Check for fuzzy terms (suffix ~)
            if token.endswith('~'):
                self.fuzzy_terms.append(token[:-1])
            else:
                self.terms.append(token)
    
    def build_where_clause(self) -> Tuple[str, List[Any]]:
        """Build the SQL WHERE clause based on the parsed query."""
        conditions = []
        params = []
        
        # Handle full-text search terms
        if self.terms or self.phrases or self.required_terms or self.excluded_terms or self.fuzzy_terms:
            fulltext_conditions = []
            
            # Add regular terms
            if self.terms:
                term_conditions = []
                for term in self.terms:
                    term_conditions.append("(h.h_title LIKE %s OR h.h_description LIKE %s OR h.h_features LIKE %s)")
                    params.extend([f"%{term}%"] * 3)
                fulltext_conditions.append(f"({' OR '.join(term_conditions)})")
            
            # Add phrases
            for phrase in self.phrases:
                fulltext_conditions.append("(h.h_title LIKE %s OR h.h_description LIKE %s OR h.h_features LIKE %s)")
                params.extend([f"%{phrase}%"] * 3)
            
            # Add required terms
            for term in self.required_terms:
                fulltext_conditions.append("(h.h_title LIKE %s OR h.h_description LIKE %s OR h.h_features LIKE %s)")
                params.extend([f"%{term}%"] * 3)
            
            # Add fuzzy terms
            for term in self.fuzzy_terms:
                # For fuzzy search, we'll use LIKE with wildcards
                # In a production environment, consider using MySQL's SOUNDEX or a dedicated search engine
                fulltext_conditions.append("(h.h_title LIKE %s OR h.h_description LIKE %s OR h.h_features LIKE %s)")
                params.extend([f"%{term}%"] * 3)
            
            # Add excluded terms
            if self.excluded_terms:
                excluded_conditions = []
                for term in self.excluded_terms:
                    excluded_conditions.append("(h.h_title NOT LIKE %s AND h.h_description NOT LIKE %s AND h.h_features NOT LIKE %s)")
                    params.extend([f"%{term}%"] * 3)
                fulltext_conditions.append(f"({' AND '.join(excluded_conditions)})")
            
            if fulltext_conditions:
                conditions.append(f"({' AND '.join(fulltext_conditions)})")
        
        # Handle filters
        for field, value in self.filters.items():
            if field == 'price':
                if '-' in value or 'to' in value.lower():
                    # Handle price range
                    if '-' in value:
                        min_price, max_price = value.split('-')
                    else:
                        min_price, max_price = value.lower().split('to')
                    
                    min_price = min_price.strip().replace(',', '')
                    max_price = max_price.strip().replace(',', '')
                    
                    conditions.append("(h.price BETWEEN %s AND %s)")
                    params.extend([min_price, max_price])
                else:
                    # Exact price
                    price = value.replace(',', '')
                    conditions.append("(h.price = %s)")
                    params.append(price)
            
            elif field == 'bedrooms':
                if value.endswith('+'):
                    # At least X bedrooms
                    min_bedrooms = int(value[:-1])
                    conditions.append("(h.bedrooms >= %s)")
                    params.append(min_bedrooms)
                elif '-' in value:
                    # Bedroom range (e.g., 2-3)
                    min_bed, max_bed = map(int, value.split('-'))
                    conditions.append("(h.bedrooms BETWEEN %s AND %s)")
                    params.extend([min_bed, max_bed])
                else:
                    # Exact number of bedrooms
                    conditions.append("(h.bedrooms = %s)")
                    params.append(int(value))
            
            elif field == 'bathrooms':
                if value.endswith('+'):
                    # At least X bathrooms
                    min_bath = float(value[:-1])
                    conditions.append("(h.bathrooms >= %s)")
                    params.append(min_bath)
                elif '-' in value:
                    # Bathroom range (e.g., 2-3)
                    min_bath, max_bath = map(float, value.split('-'))
                    conditions.append("(h.bathrooms BETWEEN %s AND %s)")
                    params.extend([min_bath, max_bath])
                else:
                    # Exact number of bathrooms
                    conditions.append("(h.bathrooms = %s)")
                    params.append(float(value))
            
            elif field == 'area':
                if '-' in value or 'to' in value.lower():
                    # Handle area range
                    if '-' in value:
                        min_area, max_area = value.split('-')
                    else:
                        min_area, max_area = value.lower().split('to')
                    
                    min_area = min_area.strip().replace(',', '')
                    max_area = max_area.strip().replace(',', '')
                    
                    conditions.append("(h.living_area BETWEEN %s AND %s)")
                    params.extend([min_area, max_area])
                else:
                    # Exact area
                    area = value.replace(',', '')
                    conditions.append("(h.living_area = %s)")
                    params.append(area)
            
            elif field == 'type':
                conditions.append("(t.t_name LIKE %s)")
                params.append(f"%{value}%")
            
            elif field == 'project':
                conditions.append("(p.p_name LIKE %s)")
                params.append(f"%{value}%")
            
            elif field == 'feature':
                conditions.append("(EXISTS (SELECT 1 FROM house_features hf JOIN house_has_features hhf ON hf.f_id = hhf.feature_id WHERE h.h_id = hhf.house_id AND hf.f_name LIKE %s))")
                params.append(f"%{value}%")
            
            elif field == 'date':
                today = datetime.now().date()
                
                if value.lower() == 'today':
                    conditions.append("(DATE(h.created_at) = %s)")
                    params.append(today)
                elif value.lower() == 'yesterday':
                    yesterday = today - timedelta(days=1)
                    conditions.append("(DATE(h.created_at) = %s)")
                    params.append(yesterday)
                elif value.lower() == 'this_week':
                    start_of_week = today - timedelta(days=today.weekday())
                    conditions.append("(DATE(h.created_at) >= %s)")
                    params.append(start_of_week)
                elif value.lower() == 'last_week':
                    end_of_last_week = today - timedelta(days=today.weekday() + 1)
                    start_of_last_week = end_of_last_week - timedelta(days=6)
                    conditions.append("(DATE(h.created_at) BETWEEN %s AND %s)")
                    params.extend([start_of_last_week, end_of_last_week])
                elif value.lower() == 'this_month':
                    start_of_month = today.replace(day=1)
                    conditions.append("(DATE(h.created_at) >= %s)")
                    params.append(start_of_month)
                elif value.lower() == 'last_month':
                    first_day_of_current_month = today.replace(day=1)
                    last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
                    first_day_of_last_month = last_day_of_last_month.replace(day=1)
                    conditions.append("(DATE(h.created_at) BETWEEN %s AND %s)")
                    params.extend([first_day_of_last_month, last_day_of_last_month])
                elif value.lower() == 'this_year':
                    start_of_year = today.replace(month=1, day=1)
                    conditions.append("(DATE(h.created_at) >= %s)")
                    params.append(start_of_year)
                elif value.lower() == 'last_year':
                    last_year = today.year - 1
                    start_of_last_year = today.replace(year=last_year, month=1, day=1)
                    end_of_last_year = today.replace(year=last_year, month=12, day=31)
                    conditions.append("(DATE(h.created_at) BETWEEN %s AND %s)")
                    params.extend([start_of_last_year, end_of_last_year])
                elif ',' in value or 'to' in value.lower():
                    # Date range
                    if ',' in value:
                        start_date_str, end_date_str = value.split(',')
                    else:
                        start_date_str, end_date_str = value.lower().split('to')
                    
                    start_date = datetime.strptime(start_date_str.strip(), '%Y-%m-%d').date()
                    end_date = datetime.strptime(end_date_str.strip(), '%Y-%m-%d').date()
                    
                    conditions.append("(DATE(h.created_at) BETWEEN %s AND %s)")
                    params.extend([start_date, end_date])
                else:
                    # Single date
                    try:
                        date_obj = datetime.strptime(value.strip(), '%Y-%m-%d').date()
                        conditions.append("(DATE(h.created_at) = %s)")
                        params.append(date_obj)
                    except ValueError:
                        logger.warning(f"Invalid date format: {value}")
        
        # Build the final WHERE clause
        where_clause = " AND ".join(conditions) if conditions else "1=1"
        return where_clause, params
    
    def build_order_by_clause(self) -> str:
        """Build the ORDER BY clause based on sorting preferences."""
        if not self.sort_by:
            # Default sorting by relevance if there's a search query
            if self.terms or self.phrases or self.required_terms or self.fuzzy_terms:
                return """
                    ORDER BY 
                        CASE 
                            WHEN h.h_title LIKE %s THEN 30
                            WHEN h.h_description LIKE %s THEN 20
                            WHEN h.h_features LIKE %s THEN 10
                            ELSE 0
                        END DESC,
                        h.created_at DESC
                """
            # Default sorting by creation date
            return "ORDER BY h.created_at DESC"
        
        # Handle custom sorting
        sort_field = self.sort_by.lower()
        sort_order = self.sort_order.upper() if self.sort_order in ('ASC', 'DESC') else 'DESC'
        
        field_mapping = {
            'price': 'h.price',
            'date': 'h.created_at',
            'bedrooms': 'h.bedrooms',
            'bathrooms': 'h.bathrooms',
            'area': 'h.living_area',
            'title': 'h.h_title',
            'relevance': 'relevance',
            'popularity': 'h.view_count',
            'newest': 'h.created_at',
            'oldest': 'h.created_at',
            'random': 'RAND()'
        }
        
        sort_field = field_mapping.get(sort_field, 'h.created_at')
        
        # Special handling for random sorting
        if sort_field == 'RAND()':
            return f"ORDER BY RAND()"
        
        return f"ORDER BY {sort_field} {sort_order}"
    
    def build_limit_clause(self) -> str:
        """Build the LIMIT clause based on pagination preferences."""
        if self.limit is not None:
            return f"LIMIT {self.offset}, {self.limit}"
        return ""

def preprocess_search_term(term: str) -> str:
    """
    Preprocess search terms by removing special characters and normalizing.
    """
    # Remove special characters except spaces, letters, and numbers
    term = re.sub(r'[^\w\s]', '', term, flags=re.UNICODE)
    # Normalize spaces and convert to lowercase
    return ' '.join(term.lower().split())

def get_fuzzy_matches(term: str, word_list: List[str], n: int = 3, cutoff: float = 0.6) -> List[str]:
    """
    Get fuzzy matches for a term from a list of words.
    
    Args:
        term: The search term
        word_list: List of words to match against
        n: Maximum number of matches to return
        cutoff: Similarity threshold (0-1)
        
    Returns:
        List of matching words
    """
    if not term or not word_list:
        return []
    
    # Try to find close matches
    matches = get_close_matches(
        term.lower(),
        [word.lower() for word in word_list],
        n=n,
        cutoff=cutoff
    )
    
    return matches

def expand_search_terms(term: str, all_terms: List[str]) -> str:
    """
    Expand search terms with fuzzy matches.
    
    Args:
        term: The original search term
        all_terms: List of all possible terms to match against
        
    Returns:
        A string with OR conditions for fuzzy matches
    """
    if not term or not all_terms:
        return term
    
    # Get fuzzy matches
    fuzzy_matches = get_fuzzy_matches(term, all_terms)
    
    if not fuzzy_matches:
        return term
    
    # Create a search string with OR conditions
    all_terms = [term] + fuzzy_matches
    return ' | '.join(f'"{t}"' for t in all_terms if t)

def parse_advanced_operators(term: str) -> List[dict]:
    """
    Parse advanced search operators from the search term.
    
    Supported operators:
    - AND: "house AND garden" (both terms must be present)
    - OR: "house OR apartment" (either term can be present)
    - NOT: "house -garden" or "house NOT garden" (exclude term)
    - "exact phrase": "luxury apartment" (exact phrase match)
    
    Args:
        term: The search term to parse
        
    Returns:
        List of dictionaries with 'term' and 'operator' keys
    """
    if not term:
        return []
    
    # Initialize variables
    tokens = []
    current_token = ''
    in_quotes = False
    i = 0
    
    while i < len(term):
        char = term[i]
        
        # Handle quoted phrases
        if char == '"':
            if in_quotes:
                # End of quoted phrase
                if current_token:
                    tokens.append({
                        'term': current_token,
                        'operator': 'PHRASE'
                    })
                    current_token = ''
                in_quotes = False
            else:
                # Start of quoted phrase
                if current_token.strip():
                    # Add any text before the quote as a separate token
                    tokens.append({
                        'term': current_token.strip(),
                        'operator': 'AND'  # Default to AND
                    })
                    current_token = ''
                in_quotes = True
            i += 1
            continue
            
        # Handle operators
        if not in_quotes:
            # Check for NOT operator (- or NOT)
            if (char == '-' and (i == 0 or term[i-1].isspace())) or \
               (char.upper() == 'N' and term[i:i+4].upper() == 'NOT '):
                if current_token.strip():
                    tokens.append({
                        'term': current_token.strip(),
                        'operator': 'AND'  # Default to AND
                    })
                    current_token = ''
                
                # Skip the operator
                if char == '-':
                    i += 1
                    # Skip whitespace after -
                    while i < len(term) and term[i].isspace():
                        i += 1
                    # Get the term to exclude
                    not_term = ''
                    while i < len(term) and not term[i].isspace() and term[i] != '"':
                        not_term += term[i]
                        i += 1
                    if not_term:
                        tokens.append({
                            'term': not_term,
                            'operator': 'NOT'
                        })
                    continue
                else:  # 'NOT ' case
                    i += 4  # Skip 'NOT '
                    # Skip whitespace
                    while i < len(term) and term[i].isspace():
                        i += 1
                    # Get the term to exclude
                    not_term = ''
                    while i < len(term) and not term[i].isspace() and term[i] != '"':
                        not_term += term[i]
                        i += 1
                    if not_term:
                        tokens.append({
                            'term': not_term,
                            'operator': 'NOT'
                        })
                    continue
            
            # Check for AND/OR operators (case insensitive)
            if char.upper() == 'A' and term[i:i+4].upper() == 'AND ':
                if current_token.strip():
                    tokens.append({
                        'term': current_token.strip(),
                        'operator': 'AND'
                    })
                    current_token = ''
                i += 4  # Skip 'AND '
                continue
                
            if char.upper() == 'O' and term[i:i+3].upper() == 'OR ':
                if current_token.strip():
                    tokens.append({
                        'term': current_token.strip(),
                        'operator': 'OR'
                    })
                    current_token = ''
                i += 3  # Skip 'OR '
                continue
        
        # Add character to current token
        current_token += char
        i += 1
    
    # Add the last token if exists
    if current_token.strip():
        tokens.append({
            'term': current_token.strip(),
            'operator': 'AND'  # Default to AND
        })
    
    return tokens

def prepare_fts_query(term: str, fields: List[str], all_terms: Optional[List[str]] = None) -> str:
    """
    Prepare a full-text search query with fuzzy matching and advanced operators.
    
    Args:
        term: The search term
        fields: List of fields to search in
        all_terms: Optional list of all possible terms for fuzzy matching
        
    Returns:
        A string for use in MATCH AGAINST clause
    """
    if not term:
        return ''
    
    # Parse the search term into tokens with operators
    tokens = parse_advanced_operators(term)
    
    # Process each token
    processed_tokens = []
    
    for token in tokens:
        token_term = token['term']
        operator = token['operator']
        
        # Skip empty terms
        if not token_term:
            continue
            
        # For phrase search, wrap in quotes and add as is
        if operator == 'PHRASE':
            processed_tokens.append(f'"{token_term}"')
            continue
        
        # For other operators, process each word in the term
        words = token_term.split()
        processed_words = []
        
        for word in words:
            # Skip very short words (MySQL full-text minimum word length is usually 4)
            if len(word) < 2:
                continue
                
            # Apply fuzzy matching if terms are provided
            if all_terms and len(word) > 2:  # Only fuzzy match longer words
                fuzzy_matches = get_fuzzy_matches(word, all_terms, n=2, cutoff=0.6)
                if fuzzy_matches:
                    # Combine original word with fuzzy matches
                    all_matches = [word] + fuzzy_matches
                    # Add each match with the appropriate operator
                    processed_words.append(f"({' '.join(f'+{m}*' for m in all_matches)})")
                    continue
            
            # Default processing for words without fuzzy matches
            processed_word = word
            
            # Add wildcard for partial matching (only for words longer than 2 chars)
            if len(word) > 2:
                processed_word = f'+{word}*'
            else:
                processed_word = f'+{word}'
                
            processed_words.append(processed_word)
        
        # Combine words in the term with the operator
        if processed_words:
            if operator == 'NOT':
                # For NOT, we need to negate each word
                processed_tokens.append(f"-({' '.join(processed_words)})")
            elif operator == 'OR':
                # For OR, we need to ensure at least one term matches
                processed_tokens.append(f"({' '.join(processed_words)})")
            else:  # AND is the default
                processed_tokens.append(' '.join(processed_words))
    
    # Combine all tokens with appropriate operators
    if not processed_tokens:
        return ''
        
    # If the first token is an OR, we need to handle it specially
    query_parts = []
    i = 0
    
    while i < len(processed_tokens):
        token = processed_tokens[i]
        
        # Handle OR tokens by combining with the next token
        if i + 1 < len(processed_tokens) and ' OR ' in processed_tokens[i+1]:
            or_tokens = [token]
            # Find all consecutive OR tokens
            while i + 1 < len(processed_tokens) and ' OR ' in processed_tokens[i+1]:
                or_tokens.append(processed_tokens[i+1].replace(' OR ', ''))
                i += 1
            # Add the combined OR condition
            query_parts.append(f"({' | '.join(or_tokens)})")
        elif token not in ['AND', 'OR']:
            query_parts.append(token)
            
        i += 1
    
    # Join all parts with spaces (AND is implicit in MySQL boolean mode)
    return ' '.join(query_parts)
