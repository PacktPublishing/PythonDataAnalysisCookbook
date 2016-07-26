# first line: 17
@memory.cache
def filter(fid, lemmatizer, sw):
    words = [lemmatizer.lemmatize(w.lower()) for w in brown.words(fid)
             if len(w) > 1 and w.lower() not in sw]

    # Ignore words which only occur once
    counts = Counter(words)
    rare = set([w for w, c in counts.items() if c == 1])

    filtered_words = [w for w in words if w not in rare]

    return [w for w in filtered_words if only_letters(w)]
