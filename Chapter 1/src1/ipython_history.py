import sqlite3
from IPython.utils.path import get_ipython_dir
import pprint
import os

def print_history(file):
    with sqlite3.connect(file) as con:
        c = con.cursor()
        c.execute("SELECT count(source_raw) as csr,\
                  source_raw FROM history\
                  GROUP BY source_raw\
                  ORDER BY csr")
        result = c.fetchall()
        pprint.pprint(result)
        c.close()

hist_file = '%s/profile_default/history.sqlite' % get_ipython_dir()

if os.path.exists(hist_file):
    print_history(hist_file)
else:
    print("%s doesn't exist" % hist_file)

