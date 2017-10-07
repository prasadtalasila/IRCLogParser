import unittest
import sys
sys.path.insert(0,"../../../")
import lib.slack.util as util
import commands
import subprocess

class UtilTest(unittest.TestCase):

    def setUp(self):
        self.nicks = ['BluesKaj', 'Peace-', 'LordOfTime', 'TheLordOfTime', 'benonsoftware', 'Benny', 'Guest43293', 'rdieter_work', 'rdieter', 'jjesse-home_', 'jjesse-home', 'rdieter1', 'Mamarok', 'Mamarok_', 'G4MBY', 'PaulW2U', 'jussi', 'shadeslayer', 'Tm_T', 'yofel', 'ScottK', 'Quintasan', 'mikhas', 'ubottu', 'Noskcaj', 'Riddell', 'Tonio_', 'Tonio_aw', 'yofel_', 'Quintasan_']
        self.expected_nicks = self.nicks

    def tearDown(self):
        self.nicks = None
        self.expected_nicks = None

    def test_save_to_disk(self):
        util.save_to_disk(self.nicks,"data/nicksTest")
        status, output = commands.getstatusoutput('cmp data/nicks data/nicksTest')
        subprocess.Popen(['rm', 'data/nicksTest'])
        assert status == 0, "Failure to load from disk."


    def test_load_from_disk(self):
        nicks = util.load_from_disk("data/nicks")
        assert nicks == self.expected_nicks, "Failure to load from disk."




if __name__ == '__main__':
    unittest.main()
