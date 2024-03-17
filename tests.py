# SLIT -- a Stack Language Intended for Training
# SLIT tests
# Pedro B. <pedrobuitragons@gmail.com>

from __future__ import annotations

import unittest
from slit.main import run_program

class TestMath(unittest.TestCase):
    def test(self: TestMath) -> None:
        self.assertEqual(
            run_program('tests/math.slit'), 0
        )

if __name__ == '__main__':
    unittest.main()
