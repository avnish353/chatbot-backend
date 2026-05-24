from nltk.tokenize import RegexpTokenizer

# Create tokenizer (splits on words, ignores punctuation)
tokenizer = RegexpTokenizer(r'\w+')

def preprocess(text):
    """
    Preprocess text for NLP:
    - Lowercase
    - Tokenize using RegexpTokenizer (no external data needed)
    """
    if not isinstance(text, str):
        text = str(text)
    tokens = tokenizer.tokenize(text.lower())
    return " ".join(tokens)