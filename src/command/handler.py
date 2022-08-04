import typing as T


class Handler(T.Protocol):  # more like 'commandler' haha
    def __call__(self, *args: str): ...
