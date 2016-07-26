import feedparser as fp
import urllib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import dautil as dl
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
import os

DRIVER = webdriver.PhantomJS()
NAP_SECONDS = 10
LOGGER = dl.log_api.conf_logger('corpus')

def store_txt(url, fname, title):
    try:
        DRIVER.get(url)

        elems = WebDriverWait(DRIVER, NAP_SECONDS).until(
            EC.presence_of_all_elements_located((By.XPATH, '//p'))
        )

        with open(fname, 'w') as txt_file:
            txt_file.write(title + '\n\n')
            lines = [e.text for e in elems]
            txt_file.write(' \n'.join(lines))
    except Exception:
        LOGGER.error("Error processing HTML", exc_info=True)

def fetch_news(dir):
    base = 'http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/{}/rss.xml'

    for category in ['world', 'technology']:
        rss = fp.parse(base.format(category))

        for i, entry in enumerate(rss.entries):
            fname = '{0}_bbc_{1}.txt'.format(i, category)
            fname = os.path.join(dir, fname)

            if not dl.conf.file_exists(fname):
                store_txt(entry.link, fname, entry.title)

if __name__ == "__main__":
    dir = os.path.join(dl.data.get_data_dir(), 'bbc_news_corpus')

    if not os.path.exists(dir):
        os.mkdir(dir)

    fetch_news(dir)
    reader = CategorizedPlaintextCorpusReader(dir, r'.*bbc.*\.txt',
                                              cat_pattern=r'.*bbc_(\w+)\.txt')
    printer = dl.log_api.Printer(nelems=3)
    printer.print('Categories', reader.categories())
    printer.print('World fileids', reader.fileids(categories=['world']))
    printer.print('Technology fileids',
                  reader.fileids(categories=['technology']))
