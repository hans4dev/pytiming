import datetime
import unittest

from timing import Timestack, Timespan


class TestTimestack(unittest.TestCase):
    def test_empty(self):
        stack = Timestack()

        self.assertEqual([], stack)
        self.assertEqual(0, len(stack))
        self.assertEqual(True, stack.is_empty())
        self.assertEqual(datetime.timedelta(), stack.duration())
        self.assertEqual([], stack.span())
        self.assertEqual([], stack.gaps())

    def test_append(self):
        stack = Timestack()
        start = datetime.datetime.now()
        span = Timespan(start, end=(start + datetime.timedelta(minutes=10)))

        stack.append(span)

        self.assertEqual([span], stack.list())
        self.assertEqual(1, len(stack))
        self.assertEqual(False, stack.is_empty())
        self.assertEqual(span.duration(), stack.duration())
        self.assertEqual([], stack.gaps(), 'should not have gaps')

    def test_duration(self):
        stack = Timestack()
        start = datetime.datetime.now()
        span = Timespan(start, start + datetime.timedelta(minutes=10))

        stack.append(span)

        self.assertEqual(stack.duration(), span.duration())

    def test_duration_multi(self):
        stack = Timestack()
        start = datetime.datetime.now()
        end = start + datetime.timedelta(minutes=10)

        stack.append(Timespan(start, end))
        stack.append(Timespan(end, end + datetime.timedelta(minutes=10)))

        self.assertEqual(datetime.timedelta(minutes=10 * 2), stack.duration())

    def test_span_multi(self):
        stack = Timestack()
        start = datetime.datetime.now()
        middle = start + datetime.timedelta(minutes=10)
        end = start + datetime.timedelta(minutes=20)

        stack.append(Timespan(start, middle))
        stack.append(Timespan(middle, end))

        self.assertEqual(Timespan(start, end), stack.span())

    def test_span_gaps(self):
        stack = Timestack()
        before = Timespan(datetime.datetime.now(), duration=datetime.timedelta(minutes=10))
        pause = Timespan(before.end, duration=datetime.timedelta(minutes=5))
        after = Timespan(pause.end, duration=datetime.timedelta(minutes=15))
        gaps = Timestack()

        stack.append(before)
        gaps.append(pause)
        stack.append(after)

        self.assertEqual(gaps, stack.gaps())
        self.assertEqual(Timespan(before.start, after.end), stack.span())
        self.assertEqual(before.duration() + after.duration(), stack.duration())
        self.assertGreater(stack.span().duration(), stack.duration(), 'span duration should be greater than stack duration')
        self.assertEqual(stack.span().duration(), stack.duration() + stack.gaps().duration(), 'span duration should be equal (stack+gap) duration')
        self.assertEqual(Timespan(before.start, duration=stack.duration()), stack.span_top())

    def test_str_empty(self):
        stack = Timestack()

        self.assertEqual("[]", stack.__str__())

    def test_str_single(self):
        stack = Timestack()
        span = Timespan()
        stack.append(span)

        self.assertEqual(str([span]), stack.__str__())

if __name__ == '__main__':
    unittest.main()
