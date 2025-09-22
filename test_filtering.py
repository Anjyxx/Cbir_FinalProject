#!/usr/bin/env python3
"""
Test the improved image filtering logic
"""

import sys
sys.stdout.reconfigure(line_buffering=True)

from cbir_search import should_exclude_image

def test_filtering():
    print("🧪 Testing Image Filtering Logic")
    print("=" * 50)
    
    # Test cases - images that should be excluded
    exclude_cases = [
        '1755518128_site_plan.png',
        '1755519688_site_plan.png',
        '1755597292_637569092158834293-House1_plan.png',
        '1755602325_LINE_ALBUM____12_2.png',
        '1755602435_LINE_ALBUM____7_1.png',
        '1755602451_LINE_ALBUM____3_1.png',
        '1755602451_LINE_ALBUM____6_2.png',
        'site_plan_1755526737.png',
        'siteplan_eOyKpVt4LUvowItdfuQ7PUQDm3fPr1DsHqI1lW9Q_1758520862.webp',
        'siteplan_image_1758518485.png',
        'baan_1_1755517021.png',
        'baan_2_l_1755519621.png',
        'inside_1_1755519621.png',
        'inside_2_1755519621.png',
        '637569091994375841-House1_cover2.png',
        'SALE_3_1.png',
        'baan_4s_type_a_2_1755591984.png'
    ]
    
    # Test cases - images that should be included
    include_cases = [
        '100051498_163247088548284_6174265717089632256_n.jpg_1755597611.png',
        '1755593318_image_1.png',
        '1755593318_image_2.png',
        '1755597642_image_1.png',
        '1755597642_image_2.png',
        '20250528_160409_LA_VILLA_KALASIN.jpg',
        'Baanthai_Buriram.jpg',
        'casa_maliwan.jpg',
        'pexels-photo-106399.jpeg'
    ]
    
    print("❌ Testing images that should be EXCLUDED:")
    excluded_count = 0
    for filename in exclude_cases:
        should_exclude = should_exclude_image(filename)
        status = "✅ EXCLUDED" if should_exclude else "❌ NOT EXCLUDED"
        print(f"  {status}: {filename}")
        if should_exclude:
            excluded_count += 1
    
    print(f"\n📊 Excluded {excluded_count}/{len(exclude_cases)} images that should be excluded")
    
    print("\n✅ Testing images that should be INCLUDED:")
    included_count = 0
    for filename in include_cases:
        should_exclude = should_exclude_image(filename)
        status = "✅ INCLUDED" if not should_exclude else "❌ INCORRECTLY EXCLUDED"
        print(f"  {status}: {filename}")
        if not should_exclude:
            included_count += 1
    
    print(f"\n📊 Included {included_count}/{len(include_cases)} images that should be included")
    
    print(f"\n🎯 Overall Score: {excluded_count + included_count}/{len(exclude_cases) + len(include_cases)} correct")
    
    if excluded_count == len(exclude_cases) and included_count == len(include_cases):
        print("🎉 All filtering tests passed!")
        return True
    else:
        print("⚠️  Some filtering tests failed. Need to improve the logic.")
        return False

if __name__ == "__main__":
    test_filtering()
