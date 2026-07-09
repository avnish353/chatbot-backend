from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')

STOP_WORDS = {
    "a", "an", "the", "is", "are", "am", "was", "were",
    "my", "your", "our", "their",
    "to", "for", "of", "in", "on", "at", "with",
    "and", "or", "but",
    "can", "could", "would", "should",
    "please"
}

def preprocess(text):
    if not isinstance(text, str):
        text = str(text)

    tokens = tokenizer.tokenize(text.lower())

    # Remove stop words
    tokens = [word for word in tokens if word not in STOP_WORDS]

    return " ".join(tokens)
