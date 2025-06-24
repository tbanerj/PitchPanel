# AI Feedback Setup Guide

## Issue: API Key Problem

The AI feedback is not working because of an incorrect or missing OpenAI API key.

## How to Fix:

### 1. Get a Valid OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/account/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (it should start with `sk-`)

### 2. Set the API Key

**Option A: Set for current session only**
```bash
export OPENAI_API_KEY="sk-your-actual-api-key-here"
```

**Option B: Set permanently (recommended)**
```bash
# Add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
echo 'export OPENAI_API_KEY="sk-your-actual-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### 3. Test the Setup

```bash
cd backend
python test_ai_feedback.py
```

You should see: "✅ All tests completed successfully!"

### 4. Start the Backend

```bash
cd backend
uvicorn main:app --reload
```

### 5. Start the Frontend

```bash
cd frontend
npm run dev
```

## Troubleshooting

### If you still get API key errors:

1. **Check the key format**: Should start with `sk-`
2. **Verify the key**: Test it in the OpenAI playground
3. **Check billing**: Ensure your OpenAI account has credits
4. **Restart terminal**: After setting the environment variable

### If the frontend doesn't work:

1. **Check browser console** for errors
2. **Verify backend is running** on http://localhost:8000
3. **Check CORS** - backend should allow frontend origin

### Common Error Messages:

- `"OPENAI_API_KEY environment variable is not set"` → Set the environment variable
- `"Invalid API key format"` → Key should start with `sk-`
- `"Invalid OpenAI API key"` → Get a new key from OpenAI
- `"API quota exceeded"` → Add billing to your OpenAI account

## Alternative: Use Without AI Feedback

If you can't get the API key working, the app will still work for basic analysis:

1. **Uncheck** "Include AI Coaching Feedback" in the frontend
2. **Upload and analyze** your audio file
3. **Get basic scores** and feedback without AI coaching

The AI feedback is optional - the core vocal analysis will work without it!

## Need Help?

1. Check the browser console for frontend errors
2. Check the terminal running the backend for server errors
3. Verify your OpenAI API key is valid and has credits 