def analyze_audio(filename: str, _file_bytes: bytes) -> tuple[str, int]:
    """
    Mock detection logic based on filename hash.
    Returns (verdict, confidence_percentage).
    """
    lower_name = filename.lower()
    suspicious_keywords = ['fake', 'synth', 'ai', 'bot', 'gpt']
    is_suspicious = any(kw in lower_name for kw in suspicious_keywords)
    
    # Calculate a simple hash
    hash_val = 0
    for char in filename:
        hash_val = (hash_val << 5) - hash_val + ord(char)
        hash_val &= 0xFFFFFFFF

    is_deepfake = is_suspicious or (hash_val % 2 == 0)
    confidence = 88 + (hash_val % 11)
    
    verdict = "deepfake" if is_deepfake else "genuine"
    return verdict, confidence
