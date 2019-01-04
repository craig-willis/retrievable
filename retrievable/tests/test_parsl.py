from unittest import mock
from retrievable.core.parsl import run_queries
from retrievable.core.query import list_from_xml
from .mock_pyndri import MockIndex, MockQueryEnv
import pyndri


def test_run_queries():
    with mock.patch('pyndri.Index') as mock_index:
        with mock.patch('pyndri.QueryEnvironment') as mock_qenv:
            mock_index.return_value = MockIndex()
            mock_qenv.return_value = MockQueryEnv()
            index = pyndri.Index('/index/path')

            token2id, id2token, id2df = index.get_dictionary()
            total_terms = index.total_terms()
            id2tf = index.get_term_frequencies()

            queries = list_from_xml('retrievable/tests/test_queries.yaml',
                                    token2id, id2tf, total_terms)

            (num, text, qv, cp) = queries[0]
            assert num == '51'
            assert text == 'airbus subsidies'
            assert qv == {6146: 1, 3313: 1}
            assert cp == {6146: 1086/76148180, 3313: 2608/76148180}

            output = run_queries('/index/path', 'retrievable.scorers.api',
                                 'ScorerDirichlet', {'mu': 1000}, queries[0])

            res = output.result()

            assert len(res) == 2
