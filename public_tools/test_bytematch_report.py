import copy
import unittest
from validate_bytematch_report import validate


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.metadata = {'source_path': 'src/game/a.c', 'complete': False}
        self.project = {'units': [{'name': 'game/a', 'metadata': self.metadata}]}
        self.report = {'version': 2, 'measures': {'total_code': '16', 'total_data': '4'},
                       'units': [{'name': 'game/a', 'metadata': copy.deepcopy(self.metadata), 'measures': {},
                                  'functions': [{'name': 'native_a', 'size': '16', 'metadata': {}}]}]}

    def test_standard_report(self):
        self.assertTrue(validate(self.report, self.project, 20)['publicSchemaPassed'])

    def test_instruction_rich_diff_rejected(self):
        self.report['units'][0]['functions'][0]['instructions'] = [{'code': 'original instruction'}]
        with self.assertRaises(ValueError):
            validate(self.report, self.project, 20)

    def test_partial_denominator_rejected(self):
        with self.assertRaises(ValueError):
            validate(self.report, self.project, 40)

    def test_completion_cannot_be_promoted(self):
        self.report['units'][0]['metadata']['complete'] = True
        with self.assertRaises(ValueError):
            validate(self.report, self.project, 20)

    def test_escaping_source_rejected(self):
        self.report['units'][0]['metadata']['source_path'] = '../inputs/game.nds'
        with self.assertRaises(ValueError):
            validate(self.report, self.project, 20)


if __name__ == '__main__':
    unittest.main()
