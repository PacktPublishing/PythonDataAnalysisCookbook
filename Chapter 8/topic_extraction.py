from sklearn.decomposition import NMF
import ch8util

terms = ch8util.load_terms()
tfidf = ch8util.load_tfidf()


nmf = NMF(n_components=44, random_state=51).fit(tfidf)

for topic_idx, topic in enumerate(nmf.components_):
    label = '{}: '.format(topic_idx)
    print(label, " ".join([terms[i] for i in topic.argsort()[:-9:-1]]))
