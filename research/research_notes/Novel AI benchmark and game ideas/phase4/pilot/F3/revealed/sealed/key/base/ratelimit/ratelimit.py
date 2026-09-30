"""Sliding-window rate limiter driven by caller-supplied timestamps."""


class ClockError(ValueError):
    pass


class Limiter:
    def __init__(self, capacity, window):
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("capacity must be a positive int")
        if not isinstance(window, int) or window < 1:
            raise ValueError("window must be a positive int")
        self.capacity = capacity
        self.window = window
        self._events = {}
        self._now = None

    def _tick(self, t):
        if not isinstance(t, int):
            raise ValueError("time must be an int")
        if self._now is not None and t < self._now:
            raise ClockError("time went backwards")
        self._now = t

    def _prune(self, key, t):
        q = self._events.get(key)
        if q is None:
            return []
        cutoff = t - self.window
        i = 0
        while i < len(q) and q[i] <= cutoff:
            i += 1
        if i:
            del q[:i]
        if not q:
            del self._events[key]
            return []
        return q

    def allow(self, key, t):
        self._tick(t)
        q = self._prune(key, t)
        if len(q) >= self.capacity:
            return False
        self._events.setdefault(key, []).append(t)
        return True

    def remaining(self, key, t):
        self._tick(t)
        q = self._prune(key, t)
        return self.capacity - len(q)

    def retry_after(self, key, t):
        self._tick(t)
        q = self._prune(key, t)
        if len(q) < self.capacity:
            return 0
        oldest = q[len(q) - self.capacity]
        return oldest + self.window - t

    def keys(self, t):
        self._tick(t)
        live = []
        for key in list(self._events):
            if self._prune(key, t):
                live.append(key)
        return live

    def reset(self, key):
        self._events.pop(key, None)
