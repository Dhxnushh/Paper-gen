"""
Configuration file for the research paper generation system.
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")

# Model Configuration
# Using Google's Gemini models (available in AI Studio)
# Generator: Gemini 2.5 Flash for high-quality and fast content generation
GENERATOR_MODEL = "gemini-2.5-flash"
# Evaluator: Gemini 2.5 Flash-Lite for fast evaluation
EVALUATOR_MODEL = "gemini-2.5-flash-lite"

# Scoring Configuration
SCORE_THRESHOLD = 32  # Out of 40 (4 criteria × 10 points each)
MAX_ITERATIONS = 5  # Maximum number of revision attempts

# Evaluation Criteria
EVALUATION_CRITERIA = {
    "relevance": "How relevant is the content to the section topic?",
    "coherence": "How well-structured and logically flowing is the content?",
    "factuality": "How accurate and well-supported are the claims?",
    "readability": "How clear and accessible is the writing?"
}
