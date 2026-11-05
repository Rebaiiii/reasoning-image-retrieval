import unittest
from retrieval.metrics import score_query, score_pair, summarize
from retrieval.evaluate import validate_cases


class EvaluationTests(unittest.TestCase):
    def pair(self, first, second):
        return score_pair([score_query(['a', 'b'], first, {'target': 'a'}),
                           score_query(['a', 'b'], second, {'target': 'b'})])

    def test_opposing_queries_both_correct(self):
        pair = self.pair([0.8, 0.2], [0.1, 0.9])
        self.assertTrue(pair['both_correct'])
        self.assertTrue(pair['choice_changed'])

    def test_same_winner_is_only_one_correct_answer(self):
        summary = summarize([self.pair([0.8, 0.2], [0.7, 0.3])])
        self.assertEqual(summary['query_correct'], 1)
        self.assertEqual(summary['same_choice'], 1)
        self.assertEqual(summary['both_correct'], 0)

    def test_tie_is_not_a_correct_switch(self):
        summary = summarize([self.pair([0.5, 0.5], [0.1, 0.9])])
        self.assertEqual(summary['pairs_with_ties'], 1)
        self.assertEqual(summary['both_correct'], 0)
        self.assertEqual(summary['same_choice'], 0)

    def test_switching_can_be_wrong(self):
        summary = summarize([self.pair([0.2, 0.8], [0.9, 0.1])])
        self.assertEqual(summary['switched_wrong'], 1)
        self.assertEqual(summary['query_correct'], 0)

    def test_missing_image_rejected(self):
        case = {'id': 'test', 'images': ['a', 'missing'],
                'queries': [{'target': 'a'}, {'target': 'missing'}]}
        with self.assertRaises(ValueError):
            validate_cases([case], ['a', 'b'], 'pairs')

    def test_same_target_rejected(self):
        case = {'id': 'test', 'images': ['a', 'b'],
                'queries': [{'target': 'a'}, {'target': 'a'}]}
        with self.assertRaises(ValueError):
            validate_cases([case], ['a', 'b'], 'pairs')


if __name__ == '__main__':
    unittest.main()
