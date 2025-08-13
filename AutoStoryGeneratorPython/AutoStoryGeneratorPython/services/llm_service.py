import requests
from ..config.config import Config

def send_prompt_to_kobold(prompt: str) -> str:
    """
    Sends a prompt to the Kobold AI API and returns the generated text.
    """
    url = f"{Config.KOBOLD_AI_URL}/api/v1/generate"
    payload = {
        'prompt': prompt,
        'max_context_length': 6000, # As per user spec
        'max_length': 500, # A reasonable default, can be adjusted
        'rep_pen': 1.1,
        'temperature': 0.7,
        'top_p': 0.9,
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        result = response.json()
        return result['results'][0]['text']
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Kobold AI: {e}")
        return f"Error: Could not connect to Kobold AI at {url}. Please ensure it is running."
    except (KeyError, IndexError) as e:
        print(f"Error parsing Kobold AI response: {e}")
        return "Error: Received an unexpected response format from Kobold AI."


def send_prompt_to_claude(prompt: str) -> str:
    """
    Sends a prompt to the Claude AI API and returns the generated text.
    NOTE: This is a placeholder and requires a valid API key and correct API endpoint/payload format.
    """
    if not Config.CLAUDE_AI_API_KEY:
        return "Error: Claude AI API key is not set in the configuration."

    # This is a hypothetical endpoint and payload structure.
    # The actual implementation will depend on the official Claude API documentation.
    url = "https://api.anthropic.com/v1/messages" # Example URL
    headers = {
        "x-api-key": Config.CLAUDE_AI_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    payload = {
        "model": "claude-3-opus-20240229", # Example model
        "max_tokens": 1024, # A reasonable default
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        # Parse response based on actual API spec
        return response.json().get('content', [{}])[0].get('text', "Error: Could not parse Claude response.")
    except requests.exceptions.RequestException as e:
        print(f"Error communicating with Claude AI: {e}")
        return "Error: Could not connect to the Claude AI API."
    except (KeyError, IndexError) as e:
        print(f"Error parsing Claude AI response: {e}")
        return "Error: Received an unexpected response format from Claude AI."

def generate_text(prompt: str, llm_choice: str = 'kobold') -> str:
    """
    Generates text using the selected LLM.
    """
    if llm_choice.lower() == 'kobold':
        return send_prompt_to_kobold(prompt)
    elif llm_choice.lower() == 'claude':
        return send_prompt_to_claude(prompt)
    else:
        return "Error: Invalid LLM choice specified."
