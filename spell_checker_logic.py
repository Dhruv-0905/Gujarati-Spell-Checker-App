import re
import unicodedata
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from Levenshtein import distance as levenshtein_distance

# --- This file contains the logic, but doesn't load models directly ---
# Models, tokenizer, and lexicon will be passed into these functions.

def clean_and_normalize(s: str) -> str:
    """Strips any [translate:...] markup and normalizes the string to NFC."""
    # The 'r' before the string makes it a raw string, which is good practice for regex
    match = re.fullmatch(r'\[translate:(.*)\]', s)
    if match:
        s = match.group(1)
    return unicodedata.normalize('NFC', s)

def generate_candidates(word, lexicon, max_dist=2, max_candidates=10):
    """Generates a ranked list of spelling candidates for a given word."""
    cleaned_word = clean_and_normalize(word)
    if cleaned_word in lexicon:
        return [cleaned_word]
    
    candidates_with_scores = []
    min_len = len(cleaned_word) - max_dist
    max_len = len(cleaned_word) + max_dist
    
    for lexicon_word in lexicon:
        if min_len <= len(lexicon_word) <= max_len:
            dist = levenshtein_distance(cleaned_word, lexicon_word)
            if dist <= max_dist:
                candidates_with_scores.append((lexicon_word, dist))

    candidates_with_scores.sort(key=lambda x: x[1])
    return [word for word, dist in candidates_with_scores[:max_candidates]]

def rank_candidates(candidates, pos_type, tokenizer, models, max_len=20):
    """Ranks candidates using a morphological model."""
    if pos_type not in models:
        return candidates
    
    model = models[pos_type]
    ranked_candidates = []

    for word in candidates:
        seq = tokenizer.texts_to_sequences([word])
        padded_seq = pad_sequences(seq, maxlen=max_len)
        predictions = model.predict(padded_seq, verbose=0)
        score = sum(np.log(np.max(p) + 1e-9) for p in predictions)
        ranked_candidates.append((word, score))
        
    ranked_candidates.sort(key=lambda x: x[1], reverse=True)
    return [word for word, score in ranked_candidates]

def spell_check(word, pos_type, lexicon, tokenizer, models):
    """Performs a full spell check on a single word."""
    cleaned_word = clean_and_normalize(word)
    
    if cleaned_word in lexicon:
        return {'word': word, 'correct': True, 'suggestions': [cleaned_word]}
    
    initial_candidates = generate_candidates(word, lexicon)
    if not initial_candidates:
        return {'word': word, 'correct': False, 'suggestions': []}
        
    ranked_suggestions = rank_candidates(initial_candidates, pos_type, tokenizer, models)
    
    return {'word': word, 'correct': False, 'suggestions': ranked_suggestions}
