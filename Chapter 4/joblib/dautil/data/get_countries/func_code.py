# first line: 265
    def get_countries(self, *args, **kwargs):
        """ Caches the pandas.io.wb.get_countries() results.

        :returns: The result of the query from cache or the WWW.
        """
        return wb.get_countries(*args, **kwargs)
