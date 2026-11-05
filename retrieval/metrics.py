"""Pair metrics; exact score ties never count as correct switches."""


def score_query(candidates, scores, query):
    target = candidates.index(query['target'])
    other = max(score for i, score in enumerate(scores) if i != target)
    margin = scores[target] - other
    order = sorted(range(len(scores)), key=lambda i: -scores[i])
    return {**query, 'ranking': [{'image': candidates[i], 'score': scores[i]} for i in order],
            'target_margin': margin, 'correct': margin > 0, 'tie': margin == 0}


def score_pair(queries):
    if len(queries) != 2 or queries[0]['target'] == queries[1]['target']:
        raise ValueError('A relation-switch pair requires two different targets')
    no_ties = not any(q['tie'] for q in queries)
    return {'queries': queries,
            'choice_changed': no_ties and queries[0]['ranking'][0]['image'] != queries[1]['ranking'][0]['image'],
            'both_correct': all(q['correct'] for q in queries)}


def summarize(rows):
    return {'pairs': len(rows), 'queries': 2 * len(rows),
            'query_correct': sum(q['correct'] for r in rows for q in r['queries']),
            'both_correct': sum(r['both_correct'] for r in rows),
            'switched_wrong': sum(r['choice_changed'] and not r['both_correct'] for r in rows),
            'same_choice': sum(not r['choice_changed'] and not any(q['tie'] for q in r['queries']) for r in rows),
            'pairs_with_ties': sum(any(q['tie'] for q in r['queries']) for r in rows)}
