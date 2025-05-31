#!/usr/bin/env python
"""
Master script to populate all Grade 5 comprehensive content
Runs all subject-specific content creation scripts
"""

import os
import sys
import subprocess
import time

def run_script(script_name):
    """Run a Python script and handle errors"""
    print(f"\n{'='*60}")
    print(f"🚀 Running {script_name}...")
    print(f"{'='*60}")
    
    try:
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        script_path = os.path.join(script_dir, script_name)
        
        # Run the script
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, check=True)
        
        print(result.stdout)
        if result.stderr:
            print("Warnings:", result.stderr)
            
        print(f"✅ {script_name} completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running {script_name}:")
        print(f"Return code: {e.returncode}")
        print(f"Error output: {e.stderr}")
        if e.stdout:
            print(f"Standard output: {e.stdout}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error running {script_name}: {str(e)}")
        return False

def main():
    """Run all Grade 5 comprehensive content scripts"""
    print("🎓 MENTORA GRADE 5 COMPREHENSIVE CONTENT POPULATION")
    print("=" * 60)
    print("This script will populate comprehensive educational content for all Grade 5 subjects:")
    print("📚 English Language Arts")
    print("🔢 Mathematics") 
    print("🔬 Science")
    print("🌍 Social Studies")
    print("🌟 Life Skills")
    print("=" * 60)
    
    # List of scripts to run in order
    scripts = [
        'populate_grade5_english_comprehensive.py',
        'populate_grade5_mathematics_comprehensive.py',
        'populate_grade5_science_comprehensive.py',
        'populate_grade5_social_studies_comprehensive.py',
        'populate_grade5_life_skills_comprehensive.py',
        'add_more_grade5_comprehensive_content.py'
    ]
    
    successful_scripts = []
    failed_scripts = []
    
    start_time = time.time()
    
    for script in scripts:
        print(f"\n⏳ Starting {script}...")
        time.sleep(1)  # Small delay for readability
        
        if run_script(script):
            successful_scripts.append(script)
        else:
            failed_scripts.append(script)
        
        time.sleep(2)  # Pause between scripts
    
    # Summary
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\n{'='*60}")
    print("📊 CONTENT POPULATION SUMMARY")
    print(f"{'='*60}")
    print(f"⏱️  Total time: {duration:.1f} seconds")
    print(f"✅ Successful: {len(successful_scripts)}")
    print(f"❌ Failed: {len(failed_scripts)}")
    
    if successful_scripts:
        print(f"\n✅ Successfully completed scripts:")
        for script in successful_scripts:
            print(f"   • {script}")
    
    if failed_scripts:
        print(f"\n❌ Failed scripts:")
        for script in failed_scripts:
            print(f"   • {script}")
        print(f"\n💡 Please check the error messages above and fix any issues.")
    else:
        print(f"\n🎉 ALL SCRIPTS COMPLETED SUCCESSFULLY!")
        print(f"📚 Your Grade 5 content is now ready for students!")
        print(f"\n📋 What was created:")
        print(f"   • Comprehensive study notes for each topic")
        print(f"   • Interactive quiz questions with explanations")
        print(f"   • Real-world examples and practical applications")
        print(f"   • Self-explanatory content for independent learning")
        
        print(f"\n🚀 Next steps:")
        print(f"   1. Test the content by taking some quizzes")
        print(f"   2. Review study notes for completeness")
        print(f"   3. Deploy to production when ready")
        print(f"   4. Monitor student engagement and feedback")

if __name__ == '__main__':
    main()
