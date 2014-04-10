import time


class StopWatch(object):
    def __init__(self, on_exited=None):
        self.on_exited = on_exited or (lambda t: None)

    def __enter__(self):
        self.start = time.clock()
        return self

    def __exit__(self, *args):
        self.end = time.clock()
        self.interval = self.end - self.start

        self.on_exited(self)

    def __str__(self):
        if hasattr(self, 'interval'):
            return '%s(start %s, end %s, interval %s)' % \
                (self.__class__.__name__, self.start, self.end, self.interval)

        return '%s(start %s)' % (self.__class__.__name__, self.start)
