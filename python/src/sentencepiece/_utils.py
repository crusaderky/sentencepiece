import re
import sys
import os


def add_snake_case(cls):
    """Add snake_cased method from CamelCased method."""

    snake_map = {}
    for k, v in cls.__dict__.items():
        if re.match(r"^[A-Z]+", k):
            snake = (
                re.sub(r"(?<!^)(?=[A-Z])", "_", k).lower().replace("n_best", "nbest")
            )
            snake_map[snake] = v
    for k, v in snake_map.items():
        setattr(cls, k, v)


def batchnize(cls, name):
    """Enable batch requests for the method cls.name."""
    func = getattr(cls, name, None)

    def _func(v, n):
        if isinstance(n, int) and (n < 0 or n >= v.piece_size()):
            raise IndexError("piece id is out of range.")
        return func(v, n)

    def _batched_func(self, arg):
        if isinstance(arg, list):
            return [_func(self, n) for n in arg]
        else:
            return _func(self, arg)

    setattr(cls, name, _batched_func)


class LogStream:
    """Context manager that redirects stderr globally to a file stream."""

    def __init__(self, ostream=None):
        self.ostream = ostream

    def __enter__(self):
        if self.ostream is None:
            return
        self.orig_stream_fileno = sys.stderr.fileno()
        self.orig_stream_dup = os.dup(self.orig_stream_fileno)
        os.dup2(self.ostream.fileno(), self.orig_stream_fileno)

    def __exit__(self, type, value, traceback):
        if self.ostream is None:
            return
        os.close(self.orig_stream_fileno)
        os.dup2(self.orig_stream_dup, self.orig_stream_fileno)
        os.close(self.orig_stream_dup)
        self.ostream.close()
