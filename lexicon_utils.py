import os
import pickle
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

# --- Configuration ---
VOCAB_SIZE = 200
MAX_LEN = 20
BATCH_SIZE = 256 # You can adjust this based on your hardware

def create_initial_lexicon():
    """Extracts all unique words from the project's Excel files."""
    base_dir = 'morphdata'
    files_and_columns = {
        'morph_segmentation.xlsx': 'Word',
        'morph_tagging_noun.xlsx': 'Word',
        'morph_tagging_verb.xlsx': 'Verb Form',
        'morph_tagging_adjective.xls': 'Word'
    }
    all_words = set()
    for filename, column_name in files_and_columns.items():
        file_path = os.path.join(base_dir, filename)
        if os.path.exists(file_path):
            engine = 'openpyxl' if filename.endswith('.xlsx') else 'xlrd'
            df = pd.read_excel(file_path, engine=engine)
            if column_name in df.columns:
                words = df[column_name].dropna().astype(str).tolist()
                all_words.update(words)
    return all_words

def create_smart_lexicon(base_lexicon, segmentation_model, tokenizer):
    """Enriches the lexicon with root words using a segmentation model."""
    base_words = list(base_lexicon)
    
    # Convert all words to padded sequences for batch prediction
    seqs = tokenizer.texts_to_sequences(base_words)
    X = pad_sequences(seqs, maxlen=MAX_LEN)
    
    # Make predictions in batches for efficiency
    all_preds = segmentation_model.predict(X, batch_size=BATCH_SIZE, verbose=1)
    
    # Decode roots from predictions
    roots = set()
    for i, word in enumerate(base_words):
        p = all_preds[i].flatten()
        root = ""
        for j, char in enumerate(word[:MAX_LEN]):
            root += char
            if p[j] > 0.5:
                break
        roots.add(root)
        
    # Return the combined set of full words and root words
    return base_lexicon.union(roots)

# --- This is the main execution block ---
# It runs only when you execute this file directly: python lexicon_utils.py
if __name__ == "__main__":
    print("--- Starting Smart Lexicon Creation ---")
    
    # Step 1: Create the initial lexicon from files
    initial_lexicon = create_initial_lexicon()
    print(f"Found {len(initial_lexicon)} unique words in datasets.")
    
    # Step 2: Load the segmentation model
    seg_model = load_model('segmentation_model.keras')
    print("Segmentation model loaded.")
    
    # Step 3: Create and fit a tokenizer
    tok = Tokenizer(num_words=VOCAB_SIZE, char_level=True)
    tok.fit_on_texts(list(initial_lexicon))
    print("Tokenizer prepared.")
    
    # Step 4: Create the smart lexicon using batch processing
    smart_lexicon = create_smart_lexicon(initial_lexicon, seg_model, tok)
    print(f"Smart lexicon created with {len(smart_lexicon)} total entries.")
    
    # Step 5: Save the final lexicon to a file
    with open('gujarati_lexicon.pkl', 'wb') as f:
        pickle.dump(smart_lexicon, f)
        
    print("\nSUCCESS: 'gujarati_lexicon.pkl' has been created and saved.")

