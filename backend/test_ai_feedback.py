#!/usr/bin/env python3
"""
Test script for the AI feedback system
"""

import os
import sys
from gpt_advice import get_comprehensive_feedback

def test_ai_feedback():
    """
    Test the AI feedback system with sample analysis results
    """
    
    # Sample analysis results (you can modify these to test different scenarios)
    sample_analysis = {
        "pitch_score": 6,
        "breath_score": 4,
        "diction_score": 7,
        "total_score": 5.8,
        "pitch_feedback": "Moderate drift. Practice with a tuner and sustained vowels.",
        "breath_feedback": "Work on long phrases and diaphragmatic support (lip trills, hissing).",
        "diction_feedback": "Diction okay. Could improve final consonant clarity."
    }
    
    print("🎤 Testing AI Feedback System")
    print("=" * 50)
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable not set!")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return False
    
    try:
        print("📊 Sample Analysis Results:")
        print(f"  Pitch Score: {sample_analysis['pitch_score']}/10")
        print(f"  Breath Score: {sample_analysis['breath_score']}/10")
        print(f"  Diction Score: {sample_analysis['diction_score']}/10")
        print(f"  Total Score: {sample_analysis['total_score']}/10")
        print()
        
        print("🤖 Generating AI Feedback...")
        ai_feedback = get_comprehensive_feedback(
            sample_analysis, 
            audio_context="Test performance - vocal warm-up exercise"
        )
        
        if "error" in ai_feedback:
            print(f"❌ Error: {ai_feedback['error']}")
            return False
        
        print("✅ AI Feedback Generated Successfully!")
        print()
        
        # Display structured feedback
        ai_data = ai_feedback.get("ai_feedback", {})
        
        print("📋 OVERALL ASSESSMENT:")
        print(ai_data.get("overall_assessment", "No assessment available"))
        print()
        
        print("🎵 PITCH ANALYSIS:")
        print(ai_data.get("pitch_analysis", "No pitch analysis available"))
        print()
        
        print("💨 BREATH SUPPORT ANALYSIS:")
        print(ai_data.get("breath_analysis", "No breath analysis available"))
        print()
        
        print("🗣️ DICTION & ARTICULATION:")
        print(ai_data.get("diction_analysis", "No diction analysis available"))
        print()
        
        print("📅 PRACTICE PLAN:")
        print(ai_data.get("practice_plan", "No practice plan available"))
        print()
        
        print("💪 ENCOURAGEMENT:")
        print(ai_data.get("encouragement", "No encouragement available"))
        print()
        
        print("🎯 IMPROVEMENT PRIORITIES:")
        priorities = ai_feedback.get("improvement_priorities", [])
        for priority in priorities:
            print(f"  • {priority}")
        print()
        
        print("🏋️ RECOMMENDED EXERCISES:")
        exercises = ai_feedback.get("recommended_exercises", [])
        for i, exercise in enumerate(exercises, 1):
            print(f"  {i}. {exercise}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        return False

def test_fallback_feedback():
    """
    Test the fallback feedback system (when AI is unavailable)
    """
    print("\n🔄 Testing Fallback Feedback System")
    print("=" * 50)
    
    # Temporarily remove API key to test fallback
    original_key = os.getenv("OPENAI_API_KEY")
    os.environ["OPENAI_API_KEY"] = ""
    
    try:
        sample_analysis = {
            "pitch_score": 5,
            "breath_score": 3,
            "diction_score": 6,
            "total_score": 4.7
        }
        
        ai_feedback = get_comprehensive_feedback(sample_analysis)
        
        if "fallback_feedback" in ai_feedback:
            print("✅ Fallback feedback working correctly!")
            fallback = ai_feedback["fallback_feedback"]
            print(f"Overall Assessment: {fallback['overall_assessment']}")
        else:
            print("❌ Fallback feedback not working")
            
    except Exception as e:
        print(f"❌ Fallback test failed: {str(e)}")
    finally:
        # Restore original API key
        if original_key:
            os.environ["OPENAI_API_KEY"] = original_key

if __name__ == "__main__":
    print("🎤 Vocal Analysis AI Feedback Test")
    print("=" * 50)
    
    # Test main AI feedback
    success = test_ai_feedback()
    
    # Test fallback feedback
    test_fallback_feedback()
    
    if success:
        print("\n✅ All tests completed successfully!")
        print("\n🚀 Your AI feedback system is ready to use!")
        print("\nTo use in your application:")
        print("1. Set OPENAI_API_KEY environment variable")
        print("2. Call get_comprehensive_feedback() with analysis results")
        print("3. Display the structured feedback to users")
    else:
        print("\n❌ Some tests failed. Please check your setup.")
        sys.exit(1) 