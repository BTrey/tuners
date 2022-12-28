import logging

class RedactingFilter(logging.Filter):
    def __init__(self, patterns=None):
        self._patterns=patterns if patterns is not None else set()

    def filter(self, record):
        for pattern in self._patterns:
            record.msg=record.msg.replace(pattern, "***")
        return True 
    
    def add_pattern(self, pattern):
        self._patterns.add(pattern)

    def remove_pattern(self, pattern):
        self._patterns.remove(pattern)


class LogManager(object):
    def __init__(self, console_log_level=logging.WARNING, log_file='debug.log', pw_filter=set()):
        self.log=logging.getLogger()
        self.log.setLevel(logging.DEBUG)

        FORMAT="%(asctime)-15s %(thread)-8s %(levelname)-8s %(message)s"
        self._formatter=logging.Formatter(FORMAT)
        self._log_filter = RedactingFilter(pw_filter) 
        self.log.addFilter(self._log_filter)
        currentHandlers=map(str, self.log.handlers)

        indx=next((i for i, name in enumerate(currentHandlers) if 'StreamHandler' in name), -1) 

        if indx == -1: 
            # defaults to stderr 
            consoleHandler=logging.StreamHandler()
            consoleHandler.setLevel(console_log_level)
            consoleHandler.setFormatter(self._formatter)
            self.log.addHandler(consoleHandler)
        else:
            consoleHandler=self.log.handlers[indx]
            consoleHandler.setLevel(console_log_level)

        if 'FileHandler' not in ' '.join(currentHandlers): 
            fileHandler=logging.FileHandler(log_file)
            fileHandler.setLevel(logging.DEBUG)
            fileHandler.setFormatter(self._formatter)
            self.log.addHandler(fileHandler)


    def add_text_logger(self, device):
        devfile= str(device) + '.log'
        fileHandler=logging.FileHandler(devfile)
        fileHandler.setLevel(logging.DEBUG)
        fileHandler.setFormatter(self._formatter)
        self.devlog = self.log.getLogger('device')
        self.devlog.addHandler(fileHandler)

    def add_pattern(self, pattern):
        self._log_filter.add_pattern(pattern)

    def remove_pattern(self, pattern):
        self._log_filter.remove_pattern(pattern)
