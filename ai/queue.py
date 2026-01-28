class PriorityQueue:
    _data: list[tuple[int, object]]

    def __init__(self):
        self._data = []
    
    def put(self, element: tuple[int, object]):
        self._data.append(element)
        def key(e: tuple[int, object]):
            return e[0]
        self._data.sort(key=key, reverse=True)
    
    def get(self):
        return self._data.pop()