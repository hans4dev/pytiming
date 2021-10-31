from unittest import TestCase

from timing import Timespan


class TestTimespan(TestCase):

    def test_str(self):
        span = Timespan()

        self.assertEqual(span.__str__(), f"{str(span.start)} - {str(span.end)} ({str(span.duration())})")