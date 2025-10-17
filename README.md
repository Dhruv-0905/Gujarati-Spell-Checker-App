Intelligent Gujarati Spell Checker
This project is a sophisticated, context-aware spell checker for the Gujarati language. Unlike traditional spell checkers that only use dictionary lookups, this application leverages deep learning models to provide grammatically intelligent suggestions. The entire system is wrapped in a user-friendly web application built with Streamlit.



✨ Features
Smart Lexicon: The dictionary was built not only from word lists but also enriched with the root forms of words, identified using a custom-trained Keras segmentation model.

Candidate Generation: Uses the Levenshtein distance algorithm to find potential corrections for misspelled words from the lexicon.

Deep Learning-Powered Ranking: The core of the project. It uses three separate Keras models (for nouns, verbs, and adjectives) to analyze the morphological structure of candidate words. Suggestions are ranked based on their grammatical plausibility, not just edit distance.

Interactive Web UI: A clean and simple user interface built with Streamlit allows for easy, interactive spell checking.

Efficient Backend: Heavy assets like the Keras models and the lexicon are loaded into memory only once using Streamlit's caching, ensuring the app is fast and responsive after the initial startup.

🛠️ Tech Stack
Backend: Python

Deep Learning: TensorFlow, Keras

Web Framework: Streamlit

Data Handling: Pandas, NumPy, Scikit-learn

Core Algorithm: Levenshtein Distance, custom-trained morphological analysis models

📂 Project Structure
The project is organized into a clean, modular structure for maintainability and deployment.

text
Gujarati_Spell_Checker_App/
│
├── adjective_model.keras          # Trained models
├── noun_model.keras
├── segmentation_model.keras
├── verb_model.keras
│
├── gujarati_lexicon.pkl           # The final "smart lexicon" data file
│
├── lexicon_utils.py               # Script to generate the smart lexicon (run once)
├── spell_checker_logic.py         # The core engine with all spell-checking functions
├── requirements.txt               # List of all Python dependencies
│
└── app.py                         # The main Streamlit web application file
🚀 Setup and Installation
Follow these steps to run the project on your local machine.

1. Clone the Repository:

bash
git clone https://github.com/YOUR_USERNAME/Gujarati_Spell_Checker_App.git
cd Gujarati_Spell_Checker_App
2. Create and Activate a Conda Environment:
It is highly recommended to use a virtual environment to manage dependencies.

bash
# Create a new environment named 'gujSpec' with Python 3.9 (or your preferred version)
conda create --name gujSpec python=3.9

# Activate the environment
conda activate gujSpec
3. Install Dependencies:
All required libraries are listed in the requirements.txt file. Install them with a single command:

bash
pip install -r requirements.txt
Note: If you encounter issues with Git LFS after cloning, run git lfs pull to download the large model files.

▶️ How to Run
Once the setup is complete, you can launch the web application.

Make sure you are in the project's root directory (Gujarati_Spell_Checker_App) and your conda environment is active.

Run the following command in your terminal:

bash
streamlit run app.py
This will automatically open a new tab in your web browser with the application running. The initial startup may take a few seconds as the models are loaded into memory for the first time.

🔬 Methodology
The spell checker operates on a three-phase pipeline:

Error Detection: The input word is first checked against the gujarati_lexicon.pkl file. If it exists, it is considered correct.

Candidate Generation: If the word is not found in the lexicon, the generate_candidates function is called. It iterates through the entire lexicon and uses the Levenshtein distance to find all words within a small edit distance (e.g., 2 edits).

Candidate Ranking: This is the intelligent core of the project. The list of candidates is passed to the rank_candidates function. This function uses the appropriate pre-trained Keras model (noun, verb, or adjective) to assign a "grammatical plausibility" score to each candidate. The candidates are then re-sorted based on this score, ensuring the most likely suggestion appears first.

🔮 Future Work
This project provides a strong foundation for several exciting extensions:

Automatic Part-of-Speech (POS) Detection: Implement a function that automatically predicts the POS of a misspelled word, removing the need for user input.

Full Sentence Checking: Expand the application to accept entire sentences, split them into words, and check each one.

Deployment: Deploy the application to a cloud service like Streamlit Community Cloud or Heroku to make it publicly accessible.
