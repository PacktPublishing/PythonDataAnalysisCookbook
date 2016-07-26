import dautil as dl
import csv
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


LOGGER = dl.log_api.conf_logger('download_html')
DRIVER = webdriver.PhantomJS()
NAP_SECONDS = 10


def write_text(fname):
    elems = []

    try:
        DRIVER.get(dl.web.path2url(fname))

        elems = WebDriverWait(DRIVER, NAP_SECONDS).until(
            EC.presence_of_all_elements_located((By.XPATH, '//p'))
        )

        LOGGER.info('Elems', elems)

        with open(fname.replace('.html', '_phantomjs.html'), 'w') as pjs_file:
            LOGGER.warning('Writing to %s', pjs_file.name)
            pjs_file.write(DRIVER.page_source)

    except Exception:
        LOGGER.error("Error processing HTML", exc_info=True)

    new_name = fname.replace('html', 'txt')

    if not os.path.exists(new_name):
        with open(new_name, 'w') as txt_file:
            LOGGER.warning('Writing to %s', txt_file.name)

            lines = [e.text for e in elems]
            LOGGER.info('lines', lines)
            txt_file.write(' \n'.join(lines))


def main():
    filedir = os.path.join(dl.data.get_data_dir(), 'edition.cnn.com')

    with open('saved_urls.csv') as csvfile:
        reader = csv.reader(csvfile)

        for line in reader:
            timestamp, count, basename, url = line
            fname = '_'.join([count, basename])
            fname = os.path.join(filedir, fname)

            if not os.path.exists(fname):
                dl.data.download(url, fname)

            write_text(fname)

if __name__ == '__main__':
    DRIVER.implicitly_wait(NAP_SECONDS)
    main()
    DRIVER.quit()
