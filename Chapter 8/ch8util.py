from collections import Counter
from nltk.corpus import brown
from joblib import Memory
import dautil as dl


memory = Memory(cachedir='.')


def only_letters(word):
    for c in word:
        if not c.isalpha():
            return False

    return True


@memory.cache
def filter(fid, lemmatizer, sw):
    words = [lemmatizer.lemmatize(w.lower()) for w in brown.words(fid)
             if len(w) > 1 and w.lower() not in sw]

    # Ignore words which only occur once
    counts = Counter(words)
    rare = set([w for w, c in counts.items() if c == 1])

    filtered_words = [w for w in words if w not in rare]

    return [w for w in filtered_words if only_letters(w)]


def load_terms():
    return dl.data.from_pickle('tfidf_df.pkl')['term'].values


def load_tfidf():
    return dl.data.from_pickle('tfidf.pkl')
