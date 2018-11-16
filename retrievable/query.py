import xmltodict
from collections import Counter


def list_from_xml(path, token2id, id2tf, total_terms):
    with open(path) as fd:
        doc = xmltodict.parse(fd.read())

    queries = []
    for query in doc['parameters']['query']:
        num = query['number']
        text = query['text']
        terms = text.split()
        qv = Counter()
        cp = {}
        for term in terms:
            token_id = token2id[term]
            qv[token_id] += 1
            cp[token_id] = id2tf[token_id]/total_terms

        queries.append((num, text, qv, cp))

    return queries
