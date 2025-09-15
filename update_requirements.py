#!/usr/bin/env python3
"""
Script to update requirements.txt by removing search-related dependencies.
"""

def clean_requirements():
    """Remove search-related dependencies from requirements files."""
    requirements_files = ['requirements.txt', 'requirements-search.txt']
    search_related = [
        'whoosh', 'rank-bm25', 'nltk', 'gensim', 'scikit-learn', 'scipy',
        'numpy', 'pandas', 'python-Levenshtein', 'fuzzywuzzy', 'spacy',
        'en_core_web_sm', 'pytorch', 'transformers', 'sentence-transformers',
        'faiss-cpu', 'hnswlib', 'annoy', 'nmslib', 'pysparnn', 'scann',
        'elasticsearch', 'opensearch-py', 'pysolr', 'xapian', 'pylucene',
        'jina', 'milvus', 'qdrant-client', 'weaviate-client', 'pinecone-client',
        'chromadb', 'txtai', 'fasttext', 'flair', 'sentencepiece', 'tokenizers'
    ]
    
    for req_file in requirements_files:
        try:
            with open(req_file, 'r') as f:
                lines = f.readlines()
            
            # Filter out search-related packages
            cleaned_lines = [
                line for line in lines 
                if not any(pkg.lower() in line.lower() for pkg in search_related)
            ]
            
            with open(req_file, 'w') as f:
                f.writelines(cleaned_lines)
                
            print(f"Cleaned {req_file}")
            
        except FileNotFoundError:
            print(f"{req_file} not found, skipping...")
        except Exception as e:
            print(f"Error processing {req_file}: {e}")

if __name__ == "__main__":
    clean_requirements()
