import importlib
import parsl
import pyndri
from collections import Counter

from parsl.app.app import python_app
from parsl.configs.local_threads import config

parsl.set_stream_logger()
parsl.load(config)


@python_app
def run_queries(index_path, scorer_module, scorer_class, params, queries=[]):
    """
    Parsl app instantiates a scorer, sets the parameters,
    runs the query, returns the result
    """

    module = importlib.import_module(scorer_module)
    class_ = getattr(module, scorer_class)
    scorer_instance = class_()

    # set parameter

    # open index. Assumes access to index_path
    index = pyndri.Index(index_path)
    term_count = index.total_terms()

    # initial retrieval
    try:
        rule = 'method:dirichlet,mu:%s' % params['mu']
        query_env = pyndri.QueryEnvironment(index, rules=(rule,))
        hits = query_env.query(queries[1], results_requested=1000)
        # hits = index.query(queries[1], rules=(rule,), results_requested=1000)

        results = []
        for doc_id, score in hits:
            docno, tokens = index.document(doc_id)
            doc_vector = Counter(tokens)
            doc_len = float(index.document_length(doc_id))

            new_score = scorer_instance.score(query_vector=queries[2],
                                              document_vector=doc_vector,
                                              doc_length=doc_len,
                                              term_count=term_count,
                                              col_prob=queries[3],
                                              params=params)

            # TODO: rescore
            results.append((queries[0], docno, new_score))
    finally:
        index.close()

    return results
