
class Testable:
    def __init__(self, subject):
        self.subject = subject

    def _assertr(self, r, other, desc):
        if r != True:
            raise AssertionError(f'{repr(self.subject)}; expected: {desc} {repr(other)}')
        return r

    def __eq__(self, other):
        r = self.subject.__eq__(other)
        return self._assertr(r, other, '==')

    def __ne__(self, other):
        r = self.subject.__ne__(other)
        return self._assertr(r, other, '!=')

    def __gt__(self, other):
        r = self.subject.__gt__(other)
        return self._assertr(r, other, '>')

    def __ge__(self, other):
        r = self.subject.__ge__(other)
        return self._assertr(r, other, '>=')

    def __lt__(self, other):
        r = self.subject.__lt__(other)
        return self._assertr(r, other, '<')

    def __le__(self, other):
        r = self.subject.__le__(other)
        return self._assertr(r, other, '<=')


_TEST_SUBJECT = None


def test_subject(subject):
    global _TEST_SUBJECT
    _TEST_SUBJECT = subject


def test(*args, **kwargs):
    return Testable(_TEST_SUBJECT(*args, **kwargs))
