import os

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a_secret_key')
    KOBOLD_AI_URL = os.environ.get('KOBOLD_AI_URL', 'http://127.0.0.1:5000')
    CLAUDE_AI_API_KEY = os.environ.get('CLAUDE_AI_API_KEY', None)
    CLAUDE_AI_WAIT_DURATION = int(os.environ.get('CLAUDE_AI_WAIT_DURATION', 4 * 60 * 60)) # Default to 4 hours in seconds
