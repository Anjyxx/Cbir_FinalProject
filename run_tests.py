#!/usr/bin/env python3
"""
Run the test suite for the search functionality.

This script discovers and runs all tests in the tests/ directory.
"""
import os
import sys
import unittest
from pathlib import Path

def run_tests():
    """Run all tests in the tests directory."""
    # Add the project root to the Python path
    project_root = str(Path(__file__).parent.absolute())
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    
    # Discover and run tests
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    
    # Run the tests
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Exit with non-zero code if tests failed
    sys.exit(not result.wasSuccessful())

if __name__ == '__main__':
    run_tests()
