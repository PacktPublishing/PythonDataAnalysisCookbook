# first line: 272
    def download(self, *args, **kwargs):
        """ Caches the pandas.io.wb.download() results.

        :returns: The result of the query from cache or the WWW.
        """
        return wb.download(*args, **kwargs)
