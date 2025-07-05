#!/usr/bin/env python3
"""
Simple runner script for Grade 6 Science content population.
This script can be run directly with: python scripts/run_grade6_science_population.py
"""

import os
import sys
import django

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pentora_platform.settings')
django.setup()

# Import and run the population script
from scripts.populate_grade6_science_comprehensive import create_grade6_science_content

if __name__ == '__main__':
    print("🚀 Starting Grade 6 Science content population...")
    success = create_grade6_science_content()
    
    if success:
        print("\n✅ Grade 6 Science content population completed successfully!")
        print("\n📊 Summary:")
        print("- 5 comprehensive science topics created")
        print("- Detailed study notes for each topic")
        print("- 150+ real-life quiz questions based on GES curriculum")
        print("- All content aligned with Ghana Education Service standards")
        print("\n🎯 Topics covered:")
        print("1. Living Things and Their Environment (30 questions)")
        print("2. Human Body and Health (30 questions)")
        print("3. Matter and Materials (30 questions)")
        print("4. Forces and Energy (basic questions)")
        print("5. Earth and Space Science (basic questions)")
        print("\n🔗 You can now access Grade 6 Science content in the learning platform!")
    else:
        print("\n❌ Grade 6 Science content population failed!")
        print("Please check the error messages above and try again.")
