# AI Feedback System for Vocal Analysis

This document describes the AI-powered feedback system that provides personalized vocal coaching advice based on singing analysis results.

## Overview

The AI feedback system uses OpenAI's GPT-4 to generate comprehensive, personalized feedback for singers. It analyzes pitch accuracy, breath support, and diction clarity scores to provide actionable advice, specific exercises, and improvement plans.

## Features

### 🎯 **Personalized Feedback**
- Analyzes individual performance scores
- Provides targeted advice for specific issues
- Adapts feedback based on performance level

### 📋 **Structured Feedback Sections**
1. **Overall Assessment** - Summary of strengths and areas for improvement
2. **Pitch Analysis** - Specific pitch issues and exercises
3. **Breath Support Analysis** - Breathing techniques and exercises
4. **Diction & Articulation** - Clarity and pronunciation advice
5. **Practice Plan** - Daily exercises and weekly goals
6. **Encouragement** - Motivation and realistic improvement timeline

### 🏋️ **Actionable Exercises**
- Specific vocal exercises for each area
- Practice recommendations
- Progress tracking tips

### 🔄 **Fallback System**
- Works even when AI is unavailable
- Provides basic feedback based on scores
- Ensures system reliability

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set OpenAI API Key
```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

### 3. Test the System
```bash
python test_ai_feedback.py
```

## API Endpoints

### POST `/analyze`
Analyze singing performance with optional AI feedback.

**Parameters:**
- `file`: Audio file (required)
- `reference`: Comma-separated reference notes (optional)
- `include_ai_feedback`: Boolean flag for AI feedback (optional, default: false)

**Example:**
```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@your_audio.wav" \
  -F "reference=C4,D4,E4,F4" \
  -F "include_ai_feedback=true"
```

### POST `/ai-feedback`
Get AI coaching feedback based on analysis scores.

**Parameters:**
- `pitch_score`: Pitch accuracy score (0-10)
- `breath_score`: Breath support score (0-10)
- `diction_score`: Diction clarity score (0-10)
- `total_score`: Overall performance score
- `audio_context`: Additional context (optional)

**Example:**
```bash
curl -X POST "http://localhost:8000/ai-feedback" \
  -F "pitch_score=6" \
  -F "breath_score=4" \
  -F "diction_score=7" \
  -F "total_score=5.8" \
  -F "audio_context=Warm-up exercise"
```

## Usage Examples

### Python Integration

```python
from gpt_advice import get_comprehensive_feedback

# Get analysis results from your analyzer
analysis_results = {
    "pitch_score": 6,
    "breath_score": 4,
    "diction_score": 7,
    "total_score": 5.8
}

# Generate AI feedback
ai_feedback = get_comprehensive_feedback(
    analysis_results, 
    audio_context="Vocal warm-up exercise"
)

# Access structured feedback
overall_assessment = ai_feedback["ai_feedback"]["overall_assessment"]
pitch_advice = ai_feedback["ai_feedback"]["pitch_analysis"]
exercises = ai_feedback["recommended_exercises"]
priorities = ai_feedback["improvement_priorities"]
```

### Frontend Integration

```javascript
// Upload audio and get analysis with AI feedback
const formData = new FormData();
formData.append('file', audioFile);
formData.append('include_ai_feedback', 'true');

const response = await fetch('/analyze', {
    method: 'POST',
    body: formData
});

const result = await response.json();

// Display AI feedback
if (result.ai_feedback) {
    displayFeedback(result.ai_feedback);
    displayExercises(result.recommended_exercises);
    displayPriorities(result.improvement_priorities);
}
```

## Response Structure

### Success Response
```json
{
  "ai_feedback": {
    "overall_assessment": "Your performance shows good potential...",
    "pitch_analysis": "Your pitch accuracy needs work...",
    "breath_analysis": "Breath support is inconsistent...",
    "diction_analysis": "Diction is generally clear...",
    "practice_plan": "Practice daily for 15-30 minutes...",
    "encouragement": "Keep practicing consistently...",
    "full_response": "Complete AI response..."
  },
  "analysis_results": {
    "pitch_score": 6,
    "breath_score": 4,
    "diction_score": 7,
    "total_score": 5.8
  },
  "recommended_exercises": [
    "Practice lip trills for 5 minutes daily",
    "Use a tuner to match pitch accuracy"
  ],
  "improvement_priorities": [
    "Improve Breath (current: 4/10)",
    "Improve Pitch (current: 6/10)"
  ]
}
```

### Error Response
```json
{
  "error": "Failed to generate AI feedback: API key not found",
  "fallback_feedback": {
    "overall_assessment": "Your overall performance shows room for improvement...",
    "pitch_analysis": "Pitch accuracy: 6/10. Practice with a tuner...",
    "breath_analysis": "Breath support: 4/10. Work on diaphragmatic breathing...",
    "diction_analysis": "Diction clarity: 7/10. Practice vowel shaping...",
    "practice_plan": "Practice daily for 15-30 minutes...",
    "encouragement": "Consistent practice will lead to improvement..."
  }
}
```

## Customization

### Modify AI Prompts
Edit the `_create_analysis_prompt` method in `gpt_advice.py` to customize the AI's instructions and feedback structure.

### Adjust Scoring Thresholds
Modify the `_get_improvement_priorities` method to change how priorities are determined based on scores.

### Add New Feedback Categories
Extend the feedback structure to include additional categories like rhythm, dynamics, or style.

## Troubleshooting

### Common Issues

1. **"OpenAI API error"**
   - Check your API key is set correctly
   - Verify you have sufficient API credits
   - Ensure internet connectivity

2. **"No content received from OpenAI API"**
   - The API response was empty
   - Check API rate limits
   - Try again with a simpler prompt

3. **Fallback feedback appears**
   - AI service is unavailable
   - Check API key and connectivity
   - System will continue working with basic feedback

### Testing

Run the test script to verify everything works:
```bash
python test_ai_feedback.py
```

## Cost Considerations

- Each AI feedback request uses OpenAI API tokens
- GPT-4 is more expensive but provides better quality feedback
- Consider using GPT-3.5-turbo for cost optimization
- Monitor API usage in your OpenAI dashboard

## Security Notes

- Never expose your API key in client-side code
- Use environment variables for API keys
- Consider rate limiting for production use
- Validate all input data before sending to AI

## Future Enhancements

- [ ] Voice-specific feedback (soprano, alto, tenor, bass)
- [ ] Genre-specific advice (classical, pop, jazz, etc.)
- [ ] Progress tracking over time
- [ ] Integration with practice apps
- [ ] Multi-language support
- [ ] Custom exercise libraries 