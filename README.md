# Multi-Agent Trip RAG

A budget-aware AI trip planning assistant powered by Google Gemini.

## Features
- **Smart Group Trip Planning**: Custom itineraries based on starting point, destination, duration, and group size.
- **Budget Intelligence**: Automatically calculates and breaks down expenses per person and for the group.
- **Custom Preferences**: Supports constraints like travel mode, dietary preferences, accommodation type, etc.

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/PRB18/Multi_agent_Trip_RAG.git
   cd Multi_agent_Trip_RAG
   ```

2. **Install dependencies:**
   ```bash
   python -m pip install google-genai python-dotenv
   ```

3. **Configure Environment:**
   Copy `.env.example` to `.env` and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

4. **Run the script:**
   ```bash
   python single_agent.py
   ```
