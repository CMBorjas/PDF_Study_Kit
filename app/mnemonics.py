import requests

def generate_mnemonic(keyword, context=""):
    """
    Calls the local Ollama API to generate a mnemonic for a given keyword.
    Falls back to a simple heuristic if the API is unavailable.
    """
    url = "http://localhost:11434/api/generate"
    prompt = f"Create a short, memorable, and slightly absurd mnemonic to remember the term '{keyword}'. Context: {context}\nProvide only the mnemonic."
    
    payload = {
        "model": "dolphin-llama3",
        "prompt": prompt,
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
    except Exception as e:
        pass # Fallback below
        
    # Fallback heuristic
    return f"[{keyword[0].upper()}...] - (Local AI API unavailable)"

def generate_mnemonics_for_chapter(chapter):
    """
    Generates mnemonics for the keywords in a chapter.
    """
    mnemonics = {}
    for keyword in chapter.get("keywords", []):
        # Taking just the first 50 chars of content for context
        context = " ".join(chapter.get("content", []))[:50]
        mnemonics[keyword] = generate_mnemonic(keyword, context)
        
    return mnemonics
