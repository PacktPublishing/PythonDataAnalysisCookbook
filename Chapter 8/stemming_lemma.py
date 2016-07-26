from nltk.corpus import brown
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import ch8util
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import pickle
import dautil as dl


stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

print('stem(analyses)', stemmer.stem('analyses'))
print('lemmatize(analyses)', lemmatizer.lemmatize('analyses'))
print()

sw = set(stopwords.words())
texts = []

fids = brown.fileids(categories='news')

for fid in fids:
    texts.append(" ".join(ch8util.filter(fid, lemmatizer, sw)))

vectorizer = TfidfVectorizer()
matrix = vectorizer.fit_transform(texts)

with open('tfidf.pkl', 'wb') as pkl:
    pickle.dump(matrix, pkl)

sums = np.array(matrix.sum(axis=0)).ravel()

ranks = [(word, val) for word, val in
         zip(vectorizer.get_feature_names(), sums)]

df = pd.DataFrame(ranks, columns=["term", "tfidf"])
df.to_pickle('tfidf_df.pkl')
df = df.sort(['tfidf'])
dl.options.set_pd_options()
print(df)
