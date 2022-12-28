class Context(object):
    def __init__(self):
        self.host = 'localhost'
        self.user = 'tuners'
        self.password = 'tuners'
        self.dbname = 'tuners'
        self.connector = None
        self.cursor = None
        self.tunes = ['.flac', '.mp3']
        self.log = None

    def __str__(self):
        # return ; .join([, .join([x, getattr(self, x)]) for x in vars(self)])
        return str(vars(self))
