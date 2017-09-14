import unittest
import pickle
import lib.util as util
import commands
import subprocess

class UtilTest(unittest.TestCase):

    @staticmethod
    def test_save_to_disk():
        nicks = ['BluesKaj', 'Peace-', 'LordOfTime', 'TheLordOfTime', 'benonsoftware', 'Benny', 'Guest43293', 'rdieter_work', 'rdieter', 'jjesse-home_', 'jjesse-home', 'rdieter1', 'Mamarok', 'Mamarok_', 'G4MBY', 'PaulW2U', 'jussi', 'shadeslayer', 'Tm_T', 'yofel', 'ScottK', 'Quintasan', 'mikhas', 'ubottu', 'Noskcaj', 'Riddell', 'Tonio_', 'Tonio_aw', 'yofel_', 'Quintasan_']
        util.save_to_disk(nicks,"data/nicksTest")
        status, output = commands.getstatusoutput('cmp data/nicks data/nicksTest')
        subprocess.Popen(['rm', 'data/nicksTest'])
        assert status == 0, "Failure to load from disk."


    @staticmethod
    def test_load_from_disk():
        expected_nicks = ['BluesKaj', 'Peace-', 'LordOfTime', 'TheLordOfTime', 'benonsoftware', 'Benny', 'Guest43293', 'rdieter_work', 'rdieter', 'jjesse-home_', 'jjesse-home', 'rdieter1', 'Mamarok', 'Mamarok_', 'G4MBY', 'PaulW2U', 'jussi', 'shadeslayer', 'Tm_T', 'yofel', 'ScottK', 'Quintasan', 'mikhas', 'ubottu', 'Noskcaj', 'Riddell', 'Tonio_', 'Tonio_aw', 'yofel_', 'Quintasan_']
        nicks = util.load_from_disk("data/nicks")
        assert nicks == expected_nicks, "Failure to load from disk."




if __name__ == '__main__':
    unittest.main()
