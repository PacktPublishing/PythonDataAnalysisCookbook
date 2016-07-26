from nltk.tag.stanford import NERTagger
import dautil as dl
import os
from zipfile import ZipFile
from nltk.corpus import brown

def download_ner():
    url = 'http://nlp.stanford.edu/software/stanford-ner-2015-04-20.zip'
    dir = os.path.join(dl.data.get_data_dir(), 'ner')

    if not os.path.exists(dir):
        os.mkdir(dir)

    fname = 'stanford-ner-2015-04-20.zip'
    out = os.path.join(dir, fname)

    if not dl.conf.file_exists(out):
        dl.data.download(url, out)

        with ZipFile(out) as nerzip:
            nerzip.extractall(path=dir)

    return os.path.join(dir, fname.replace('.zip', ''))


dir = download_ner()
st = NERTagger(os.path.join(dir, 'classifiers',
                            'english.all.3class.distsim.crf.ser.gz'),
               os.path.join(dir, 'stanford-ner.jar'))
fid = brown.fileids(categories='news')[0]
printer = dl.log_api.Printer(nelems=9)

tagged = [pair for pair in dl.collect.flatten(st.tag(brown.words(fid)))
          if pair[1] != 'O']
printer.print(tagged)
