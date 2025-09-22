#!/usr/bin/env python3
from cbir_search import should_exclude_image

# Test problematic filenames
test_files = [
    '1755518128_site_plan.png',
    '1755602325_LINE_ALBUM____12_2.png', 
    '1755597292_637569092158834293-House1_plan.png',
    '1755597642_image_1.png'
]

for filename in test_files:
    excluded = should_exclude_image(filename)
    print(f"{filename}: {'EXCLUDED' if excluded else 'INCLUDED'}")
