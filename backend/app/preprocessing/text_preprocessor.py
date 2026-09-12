"""
Text preprocessing pipeline.

Must remain consistent with the preprocessing used when the RNN/LSTM/GRU
models were trained (see notebooks/). Any drift here will silently break
inference quality because the tokenizers were fit on text produced by
this exact pipeline.

Pipeline:
    1. Lowercase
    2. Remove mentions / URLs / non-alphanumeric characters
    3. Split into words
    4. Remove English stopwords
    5. Snowball (Porter2) English stemming
    6. Reconstruct into a single cleaned string
"""
import re
import logging

logger = logging.getLogger(__name__)

# Matches @mentions, http(s):// urls, and any non-alphanumeric run.
CLEAN_PATTERN = re.compile(r"@\S+|https?:\S+|http?:\S|[^A-Za-z0-9]+")

_stopwords = None
_stemmer = None
_nltk_ready = False


def _ensure_nltk():
    """Lazily download/load NLTK resources exactly once."""
    global _stopwords, _stemmer, _nltk_ready
    if _nltk_ready:
        return

    import nltk
    from nltk.corpus import stopwords
    from nltk.stem import SnowballStemmer

    try:
        stopwords.words("english")
    except LookupError:
        logger.info("Downloading NLTK 'stopwords' corpus...")
        nltk.download("stopwords", quiet=True)

    _stopwords = set(stopwords.words("english"))
    _stemmer = SnowballStemmer("english")
    _nltk_ready = True


def clean_text(text: str) -> str:
    """
    Apply the full preprocessing pipeline to a single raw text string
    and return the cleaned, stemmed, stopword-free string.
    """
    _ensure_nltk()

    text = text.lower()
    text = CLEAN_PATTERN.sub(" ", text)

    tokens = text.split()
    tokens = [t for t in tokens if t not in _stopwords and len(t) > 0]
    tokens = [_stemmer.stem(t) for t in tokens]

    return " ".join(tokens)
