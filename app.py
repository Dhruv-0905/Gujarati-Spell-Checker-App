# --- app.py: Complete Gujarati Spell Checker Web App ---

import streamlit as st
import pickle
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer

# Import the main logic function from your other file
from spell_checker_logic import spell_check

# --- Module 1: Page Configuration (A small addition for a nicer look) ---
st.set_page_config(
    page_title="Gujarati Spell Checker",
    page_icon="✍️",
    layout="centered"
)

# --- Module 2: Backend - Caching and Loading ---

@st.cache_resource
def load_all_models():
    """Loads all Keras models and returns them as a dictionary."""
    print("--- Loading Keras models... (This should only print once) ---")
    models = {
        'noun': load_model('noun_model.keras'),
        'verb': load_model('verb_model.keras'),
        'adjective': load_model('adjective_model.keras')
    }
    return models

@st.cache_resource
def load_lexicon_and_tokenizer():
    """Loads the lexicon file and creates a tokenizer."""
    print("--- Loading lexicon and creating tokenizer... (This should only print once) ---")
    with open('gujarati_lexicon.pkl', 'rb') as f:
        lexicon = pickle.load(f)
    
    tokenizer = Tokenizer(num_words=200, char_level=True)
    tokenizer.fit_on_texts(list(lexicon))
    
    return lexicon, tokenizer

# --- Load all assets using the cached functions ---
with st.spinner("Loading models and data... Please wait."):
    models = load_all_models()
    lexicon, tokenizer = load_lexicon_and_tokenizer()

st.title("✍️ Gujarati Spell Checker")
st.info("All models and data loaded successfully!")


# --- Module 3: Frontend User Interface ---

st.markdown("---")
st.header("Check a Word")

# 1. Text input for the user to enter a word
user_word = st.text_input("Enter a Gujarati word:")

# 2. Dropdown menu (selectbox) for the part of speech
pos_options = ["noun", "verb", "adjective"]
user_pos = st.selectbox("Select the Part of Speech:", pos_options)

# 3. Button to trigger the spell check
check_button = st.button("Check Spelling")


# --- Module 4: Integration and Displaying Results ---

# This block will run only when the user clicks the button
if check_button:
    # First, validate that the user has entered a word
    if not user_word.strip():
        st.warning("Please enter a word to check.")
    else:
        # Show a spinner while the model is working
        with st.spinner("Analyzing word..."):
            # Call the main spell_check function from our logic file
            result = spell_check(user_word, user_pos, lexicon, tokenizer, models)
        
        # Display the results based on the output dictionary
        if result['correct']:
            st.success(f"The word **'{result['word']}'** is spelled correctly!")
        else:
            st.error(f"The word **'{result['word']}'** appears to be misspelled.")
            if result['suggestions']:
                st.write("Did you mean:")
                # Use columns for a cleaner layout of suggestions
                cols = st.columns(3)
                for i, suggestion in enumerate(result['suggestions'][:6]): # Show top 6
                    cols[i % 3].info(suggestion)
            else:
                st.warning("No suggestions found.")

