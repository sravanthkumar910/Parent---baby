# matcher.py
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# =========================
# NLTK SETUP
# =========================
def find_best_match(df, text):
    return 0, None
    
nltk.download("punkt", quiet=True)
nltk.download("stopwords", quiet=True)

STOP_WORDS = set(stopwords.words("english"))
STEMMER = PorterStemmer()

# =========================
# TEXT PREPROCESSING
# =========================
def preprocess(text: str) -> set:
    """
    Convert text to a set of stemmed tokens
    """
    if not text:
        return set()

    text = str(text).lower()
    tokens = word_tokenize(text)
    tokens = [t for t in tokens if t.isalnum()]
    tokens = [t for t in tokens if t not in STOP_WORDS]
    tokens = [STEMMER.stem(t) for t in tokens]
    return set(tokens)


# =========================
# SIMILARITY SCORE
# =========================
def jaccard_similarity(a: set, b: set) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


# =========================
# MAIN MATCHER
# =========================
def find_best_match(df, user_question: str):
    """
    Returns:
      (best_score, best_row)
    """

    query_tokens = preprocess(user_question)

    if not query_tokens:
        return 0.0, None

    best_score = 0.0
    best_row = None

    # Decide which processed column exists
    if "processed_input" in df.columns:
        processed_col = "processed_input"
    elif "processed_activity" in df.columns:
        processed_col = "processed_activity"
    else:
        raise ValueError("❌ No processed text column found in model")

    for _, row in df.iterrows():
        row_tokens = row.get(processed_col)

        if not isinstance(row_tokens, set):
            continue

        score = jaccard_similarity(query_tokens, row_tokens)

        if score > best_score:
            best_score = score
            best_row = row

    return best_score, best_row

