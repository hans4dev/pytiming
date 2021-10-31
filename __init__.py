import datetime
from typing import List


class Timespan(object):

    def __init__(self, start: datetime.datetime = None, end: datetime.datetime = None,
                 duration: datetime.timedelta = None):
        super().__init__()
        if not start:
            self.start = datetime.datetime.now()
        else:
            self.start = start

        if end:
            self.end = end
        elif duration:
            self.end = start + duration
        else:
            self.end = self.start

    def __eq__(self, o: object) -> bool:
        """Overrides the default implementation"""
        if isinstance(o, Timespan):
            return self.start == o.start and self.end == o.end
        return False

    def __str__(self) -> str:
        return f"{self.start} - {self.end} ({self.duration()})"

    def duration(self):
        return self.end - self.start


class Timestack(List):

    def __init__(self) -> None:
        super().__init__()
        self.stack = []

    def __len__(self) -> int:
        return len(self.stack)

    def __str__(self) -> str:
        return str(self.stack)

    def is_empty(self):
        return len(self.stack) == 0

    def append(self, span: Timespan):
        self.stack.append(span)

    def duration(self):
        total = datetime.timedelta()
        for span in self.stack:
            total += span.duration()

        return total

    def span(self):
        if not len(self):
            return []

        return Timespan(self.stack[0].start, self.stack[-1].end)

    def gaps(self):
        gaps = Timestack()
        before = None
        for span in self.stack:
            if before and before.end != span.start:
                gaps.append(Timespan(before.end, span.start))
            before = span
        return gaps

    def span_top(self):
        if not len(self):
            return None

        return Timespan(self.stack[0].start, duration=self.duration())

    def list(self):
        return self.stack
