from retrievable.scorers.api import ScorerDirichlet


def test_dirichlet():

    query_vector = {1: 1, 2: 2}
    document_vector = {1: 4, 2: 4, 3: 4}
    doc_length = 12
    term_count = 10000
    col_prob = {1: 0.001, 2: 0.002}
    params = {'mu': 1000}

    scorer = ScorerDirichlet()
    score = scorer.score(query_vector, document_vector, doc_length,
                         term_count, col_prob, params)
    assert score == -5.188698232884008
