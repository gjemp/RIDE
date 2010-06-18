import os
import time
import unittest

from robot.utils.asserts import assert_true, assert_false, assert_not_none, \
    assert_equals, fail, assert_none
from robotide.namespace import Namespace
from robotide.robotapi import TestCaseFile



DATAPATH = os.path.join(os.path.abspath(os.path.split(__file__)[0]),
                        '..', 'resources', 'robotdata')
TESTCASEFILE_WITH_EVERYTHING = os.path.normpath(os.path.join(DATAPATH, 'testsuite',
                                                   'everything.html'))

class TestNamespacePerformance(unittest.TestCase):
    def test_keyword_find_performance(self):
        ns = Namespace()
        everything_tcf = TestCaseFile(source=TESTCASEFILE_WITH_EVERYTHING)
        start_time = time.time()
        for i in range(1000):
            ns.is_user_keyword(everything_tcf, 'hevonen %s' % i)
        end_time = time.time() - start_time
        assert_true(end_time < 0.5, 'Checking 1000 kws took too long: %ds.' % end_time)